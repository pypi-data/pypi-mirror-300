from typing import Annotated

from langgraph.graph.message import AnyMessage, add_messages
from typing_extensions import TypedDict


class MainState(TypedDict):
    prompt: str | None = None
    messages: Annotated[list[AnyMessage], add_messages]
    user_input: str | None = None
