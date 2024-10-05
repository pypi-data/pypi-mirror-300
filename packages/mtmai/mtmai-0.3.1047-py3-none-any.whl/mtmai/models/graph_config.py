from pydantic import BaseModel
from typing_extensions import Literal


class LlmItem(BaseModel):
    class Config:
        arbitrary_types_allowed = True

    name: str
    provider: str | None = None
    base_url: str | None = None
    api_key: str | None = None
    is_tool_use: bool | None = None
    temperature: float = 0.7
    model: str | None = None
    max_tokens: int = 8000


class GraphConfig(BaseModel):
    class Config:
        arbitrary_types_allowed = True

    llms: dict[Literal["chat", "long_context", "tool_use", "fast"], LlmItem]

    #链调用失败是自动重试的次数
    llm_retry_default: int = 3
