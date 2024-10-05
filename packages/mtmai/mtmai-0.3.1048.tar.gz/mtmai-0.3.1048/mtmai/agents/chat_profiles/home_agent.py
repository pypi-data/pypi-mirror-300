from langchain_core.messages import ChatMessage
from langchain_core.runnables import RunnableConfig
from langchain_core.tools import tool
from langgraph.graph.graph import CompiledGraph
from pydantic import BaseModel, Field

import mtmai.chainlit as cl
from mtmai.agents.chat_profiles.base_chat_agent import ChatAgentBase
from mtmai.agents.ctx import get_mtmai_ctx
from mtmai.agents.graphs.chat_graph import ChatGraph
from mtmai.chainlit import context
from mtmai.core.logging import get_logger
from mtmai.models.chat import ChatProfile

logger = get_logger()


class get_current_weather(BaseModel):
    """Get the current weather in a given location"""

    location: str = Field(..., description="The city and state, e.g. San Francisco, CA")


async def call_model_messages(
    messages: list[ChatMessage],
):
    ctx = get_mtmai_ctx()
    # llm_chat = ctx.graph_config.llms.get("chat")
    tools = [home_ui_tool]
    ai_msg = await ctx.ainvoke_model_messages(messages, tools)

    return ai_msg


@tool(parse_docstring=False, response_format="content_and_artifact")
def home_ui_tool():
    """通过调用此工具，可以展示不同的UI 面板，当用户有需要时可以调用这个函数向用户显示不同的操作面板"""
    return (
        "Operation successful",
        {
            "artifaceType": "AdminView",
            "props": {
                "title": "管理面板",
            },
        },
    )


class HomeAgent(ChatAgentBase):
    """
    首页 聊天机器人
    1: 相当于客服的功能
    """

    def __init__(
        self,
    ):
        pass

    async def __call__(self, state: dict, batchsize: int) -> dict:
        """"""
        return {}

    @classmethod
    def name(cls):
        return "HomeAgent"

    @classmethod
    def get_chat_profile(self):
        return ChatProfile(
            name="HomeAgent",
            description="助手聊天机器人",
        )

    async def chat_start(self):
        user_session = cl.user_session
        thread_id = context.session.thread_id

        graph = await ChatGraph().get_compiled_graph()
        user_session.set("graph", graph)

        thread: RunnableConfig = {
            "configurable": {
                "thread_id": thread_id,
            }
        }
        await self.run_graph(thread, {"messages": []})

    async def on_message(self, message: cl.Message):
        user_session = cl.user_session
        thread_id = context.session.thread_id

        graph: CompiledGraph = user_session.get("graph")
        if not graph:
            raise ValueError("graph 未初始化")
        thread: RunnableConfig = {
            "configurable": {
                "thread_id": thread_id,
            }
        }
        pre_state = await graph.aget_state(thread, subgraphs=True)
        await graph.aupdate_state(
            thread,
            {**pre_state.values, "user_input": message.content},
            # as_node="on_chat_message_node",
        )
        await self.run_graph(thread)

    async def run_graph(
        self,
        thread: RunnableConfig,
        inputs=None,
    ):
        user_session = cl.user_session
        graph = user_session.get("graph")
        if not graph:
            raise ValueError("graph 未初始化")

        async for event in graph.astream_events(
            inputs,
            version="v2",
            config=thread,
            subgraphs=True,
        ):
            kind = event["event"]
            node_name = event["name"]
            data = event["data"]
            if kind == "on_chat_model_end":
                output = data.get("output")
                if output:
                    chat_output = output.content
                    await cl.Message(chat_output).send()

            if kind == "on_chain_end":
                output = data.get("output")

                if node_name == "on_chat_start_node":
                    thread_ui_state = output.get("thread_ui_state")
                    if thread_ui_state:
                        await cl.set_thread_ui_state(thread_ui_state)
                if node_name == "LangGraph":
                    logger.info("中止节点")
                    if (
                        data
                        and (output := data.get("output"))
                        and (final_messages := output.get("messages"))
                    ):
                        for message in final_messages:
                            message.pretty_print()

            if kind == "on_tool_start":
                # logger.info("(@stream)工具调用开始 %s", node_name)
                await cl.Message(content="工具调用开始").send()

            if kind == "on_tool_end":
                output = data.get("output")
                logger.info("(@stream)工具调用结束 %s %s", node_name, output)
                await cl.Message(content="工具调用结束").send()
