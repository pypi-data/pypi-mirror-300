import os
from functools import lru_cache

from langchain_openai import ChatOpenAI

from mtmai.core.config import settings
from mtmai.core.logging import get_logger
from mtmai.models.graph_config import GraphConfig
from mtmai.mtlibs import yaml

logger = get_logger()


@lru_cache(maxsize=1)
def get_graph_config() -> GraphConfig:
    if not os.path.exists(settings.graph_config_path):
        raise Exception(f"未找到graph_config配置文件: {settings.graph_config_path}")
    config_dict = yaml.load_yaml_file(settings.graph_config_path) or {}

    sub = config_dict.get("mtmai_config")
    a = GraphConfig.model_validate(sub)

    return a


def get_chat_llm():
    api_key = settings.GROQ_TOKEN
    llm_config = get_graph_config().llms.get("chat")
    base_url = llm_config.base_url
    model = llm_config.model
    return ChatOpenAI(
        base_url=base_url,
        api_key=api_key,
        model=model,
        temperature=llm_config.temperature or 0.7,
        max_tokens=llm_config.max_tokens,
    )
