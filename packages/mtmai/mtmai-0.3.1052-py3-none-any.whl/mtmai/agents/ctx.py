from http import client
from multiprocessing.spawn import prepare
import os
from functools import lru_cache
from typing import Type

import httpx
import orjson
from json_repair import repair_json
from langchain_core.messages import ChatMessage
from langchain_core.prompts import SystemMessagePromptTemplate
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

from lazify import LazyProxy
from psycopg_pool import AsyncConnectionPool
from pydantic import BaseModel
from sqlalchemy import Engine
from sqlmodel import Session
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver

from mtmai.agents.graphutils import ensure_valid_llm_response_v2
from mtmai.agents.retrivers.mtmdoc import MtmDocStore
from mtmai.core.config import settings
from mtmai.core.db import get_engine
from mtmai.core.logging import get_logger
from mtmai.llm.embedding import get_default_embeddings
from mtmai.models.graph_config import GraphConfig
from mtmai.mtlibs import yaml
from mtmai.mtlibs.kv.mtmkv import MtmKvStore

logger = get_logger()

class LoggingTransport(httpx.AsyncHTTPTransport):
    async def handle_async_request(self, request):
        response = await super().handle_async_request(request)
        # 提示： 不要读取 body，因为一般 是stream，读取了会破环状态
        logger.info(f"OPENAI Response: {response.status_code}\n {request.url}\nreq:\n{str(request.content)}\n")
        return response

@lru_cache(maxsize=1)
def get_graph_config() -> GraphConfig:
    if not os.path.exists(settings.graph_config_path):
        raise Exception(f"未找到graph_config配置文件: {settings.graph_config_path}")
    config_dict = yaml.load_yaml_file(settings.graph_config_path) or {}

    sub = config_dict.get("mtmai_config")
    return GraphConfig.model_validate(sub)


class AgentContext:
    def __init__(self, db_engine: Engine):
        self.httpx_session: httpx.Client = None
        self.db: Engine = db_engine
        self.session: Session = Session(db_engine)
        embedding = get_default_embeddings()

        self.vectorstore = MtmDocStore(session=Session(db_engine), embedding=embedding)
        self.kvstore = MtmKvStore(db_engine)

        self.graph_config = get_graph_config()

    def retrive_graph_config(self):
        return self.graph_config

    def load_doc(self):
        return self.vectorstore

    async def get_llm_config(self, llm_config_name: str):
        llm_item = None
        for item in self.graph_config.llms:
            if item.id == llm_config_name:
                llm_item = item
                break
        if not llm_item:
            raise ValueError(f"未找到 {llm_config_name} 对应的 llm 配置")
        return llm_item

    async def get_llm_openai(self, llm_config_name: str):
        llm_item = await self.get_llm_config(llm_config_name)
        return ChatOpenAI(
            base_url=llm_item.base_url,
            api_key=llm_item.api_key,
            model=llm_item.model,
            temperature=llm_item.temperature or None,
            max_tokens=llm_item.max_tokens or None,
        )
    async def ainvoke_model(
        self,
        tpl: PromptTemplate,
        inputs: dict |BaseModel | None,
        *,
        tools: list[any] = None,
        structured_output: BaseModel = None,
        llm_config_name: str = "chat",
    ):
        llm_item = await self.get_llm_config(llm_config_name)

        # 使用自定义传输层创建 HTTPX 客户端
        llm_inst = ChatOpenAI(
            base_url=llm_item.base_url,
            api_key=llm_item.api_key,
            model=llm_item.model,
            temperature=llm_item.temperature or None,
            max_tokens=llm_item.max_tokens or None,
            # 使用自动以httpx 客户端 方便日志查看
            http_client=httpx.Client(transport=LoggingTransport()),
            http_async_client=httpx.AsyncClient(transport=LoggingTransport()),
        )

        if llm_item.llm_type == "llama3.1":
            # llama3.1 模型工具调用专用提示词，如果没有这些提示词，工具调用的性能会大幅下降，常常出现意外的函数名和参数
            toolPrompt = f"""
If you choose to call a function ONLY reply in the following format with no prefix or suffix:
Reminder:
- Required parameters MUST be specified
- Only call one function at a time
- Put the entire function call reply on one line
- If there is no function call available, answer the question like normal with your current knowledge and do not tell the user about function calls
- Do not choose tools outside the given list of tools
- Function names must only contain characters a-z, A-Z, and underscore (_)
"""
            if "additional_instructions" in tpl.input_variables:
                tpl=tpl.partial(additional_instructions=toolPrompt)
            else:

                tpl.messages.append(ChatPromptTemplate.from_messages([
                    ("system",toolPrompt)
                ])
            )

        messages = await tpl.ainvoke(inputs.model_dump())
        llm_chain = llm_inst
        if structured_output:
            llm_chain = llm_chain.with_structured_output(
                structured_output, include_raw=True
            )
        if tools:
            llm_chain = llm_chain.bind_tools(tools)
        llm_chain = llm_chain.with_retry(stop_after_attempt=5)

        message_to_post= messages.to_messages()

        ai_msg=await ensure_valid_llm_response_v2(llm_chain,message_to_post)
        return ai_msg


    def repair_json(self, json_like_input: str):
        """修复 ai 以非标准的json回复 的 json 字符串"""
        good_json_string = repair_json(json_like_input, skip_json_loads=True)
        return good_json_string

    def load_json_response(
        self, ai_json_resonse_text: str, model_class: Type[BaseModel]
    ) -> Type[BaseModel]:
        repaired_json = self.repair_json(ai_json_resonse_text)
        try:
            loaded_data = orjson.loads(repaired_json)
            return model_class(**loaded_data)
        except Exception as e:
            logger.error(f"Error parsing JSON: {str(e)}")
            raise ValueError(
                f"Failed to parse JSON and create {model_class.__name__} instance"
            ) from e

    async def get_db_pool(self):
        connection_kwargs = {
            "autocommit": True,
            "prepare_threshold": 0,
        }
        pool = AsyncConnectionPool(
            conninfo=settings.DATABASE_URL,
            max_size=20,
            kwargs=connection_kwargs,
        )
        await pool.open()
        return pool

    async def get_graph_checkpointer(self):
        return AsyncPostgresSaver(await mtmai_context.get_db_pool())



    async def get_graph_by_name(self, name: str):
        if name == "storm":
            from mtmai.agents.graphs.storm import StormGraph

            return StormGraph()

        if name == "home_chat":
            from mtmai.agents.graphs.chat_graph import ChatGraph

            return ChatGraph()
        return None

def get_mtmai_ctx():
    return AgentContext(
        db_engine=get_engine(),
    )

mtmai_context: AgentContext = LazyProxy(get_mtmai_ctx, enable_cache=False)


