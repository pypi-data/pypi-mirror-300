import logging
from typing import Annotated

from langchain_core.tools import tool
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from langgraph.graph import StateGraph
from langgraph.graph.graph import CompiledGraph
from langgraph.graph.message import AnyMessage, add_messages
from langgraph.prebuilt import ToolNode
from pydantic import BaseModel

from mtmai.agents.ctx import get_mtmai_ctx
from mtmai.agents.graphs.abstract_graph import AbstractGraph
from mtmai.agents.nodes.on_chat_message_node import OnChatMessageNode
from mtmai.agents.nodes.on_chat_start_node import OnChatStartNode
from mtmai.llm.llm import get_fast_llm

logger = logging.getLogger()


class HomeChatState(BaseModel):
    messages: Annotated[list[AnyMessage], add_messages]
    user_input: str | None = None


@tool(parse_docstring=False, response_format="content_and_artifact")
def coplilot_ui_tools(panel_name: str):
    """Call to control frontend coplilot ui panels"""
    return (
        "Operation successful",
        {
            "artifaceType": "AdminView",
            "props": {
                "title": "管理面板",
            },
        },
    )


def should_continue(state: HomeChatState):
    messages = state.messages

    if len(messages) > 0 and messages[-1].tool_calls:
        return "tools"
    return "on_chat_message_node"


class ChatGraph(AbstractGraph):
    def create_graph(self) -> StateGraph:
        tools = [coplilot_ui_tools]
        tool_node = ToolNode(tools)

        runnable = get_fast_llm()
        runnable = runnable.bind_tools(tools)

        wf = StateGraph(HomeChatState)
        wf.add_node("on_chat_start_node", OnChatStartNode(runnable))
        wf.add_node("on_chat_message_node", OnChatMessageNode(runnable))
        wf.add_node("tools", tool_node)

        wf.add_edge("on_chat_start_node", "on_chat_message_node")
        wf.add_conditional_edges(
            "on_chat_message_node",
            should_continue,
            {
                "tools": "tools",
                "continue": "on_chat_message_node",
            },
        )
        wf.add_edge("tools", "on_chat_message_node")
        wf.set_entry_point("on_chat_start_node")

        return wf

    async def get_compiled_graph(self) -> CompiledGraph:
        ctx = get_mtmai_ctx()
        checkpointer2 = AsyncPostgresSaver(await ctx.get_db_pool())
        wf = self.create_graph()
        return wf.compile(
            checkpointer=checkpointer2,
            # interrupt_after=["on_chat_message_node"],
            interrupt_before=["on_chat_message_node"],
            debug=True,
        )
