import logging
from typing import Annotated

from langgraph.graph import END, StateGraph
from langgraph.graph.message import AnyMessage, add_messages
from typing_extensions import TypedDict

from mtmai.agents.graphs.abstract_graph import AbstractGraph
from mtmai.agents.nodes.joke_writer_node import JokeWriterNode

logger = logging.getLogger()


class JokeState(TypedDict):
    prompt: str | None = None
    messages: Annotated[list[AnyMessage], add_messages]


class JokeGraph(AbstractGraph):
    def create_graph(self) -> StateGraph:
        wf = StateGraph(JokeState)
        wf.add_node("joke_writer", JokeWriterNode())
        wf.set_entry_point("joke_writer")
        wf.add_edge("joke_writer", END)

        return wf
