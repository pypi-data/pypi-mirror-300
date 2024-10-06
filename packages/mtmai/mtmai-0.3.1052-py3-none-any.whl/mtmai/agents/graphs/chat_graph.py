import logging

from langgraph.graph import END, StateGraph
from langgraph.graph.graph import CompiledGraph

from mtmai.agents.ctx import mtmai_context
from mtmai.agents.graphutils import (
    create_entry_node,
    create_tool_node_with_fallback,
    pop_dialog_state,
)
from mtmai.agents.nodes.article_writer_node import WriteArticleNode
from mtmai.agents.nodes.develop_node import DevelopNode, route_develop_mode
from mtmai.agents.nodes.flight_booking import FlightBookingNode, route_update_flight
from mtmai.agents.nodes.node_human import HumanNode
from mtmai.agents.nodes.on_chat_start_node import OnChatStartNode, route_to_workflow
from mtmai.agents.nodes.primary_assistant import (
    PrimaryAssistantNode,
    primary_assistant_tools,
    route_primary_assistant,
)
from mtmai.agents.tools.tools import (
    update_flight_safe_tools,
    update_flight_sensitive_tools,
    develop_sensitive_tools,
    develop_safe_tools,
)
from mtmai.models.graph_config import HomeChatState

logger = logging.getLogger()


class ChatGraph:
    async def create_graph(self) -> StateGraph:
        llm_runnable = await mtmai_context.get_llm_openai("chat")
        wf = StateGraph(HomeChatState)
        wf.add_node("on_chat_start_node", OnChatStartNode(llm_runnable))
        wf.set_entry_point("on_chat_start_node")

        wf.add_conditional_edges("on_chat_start_node", route_to_workflow)
        # ------------------------------
        # Primary assistant
        wf.add_node("primary_assistant", PrimaryAssistantNode(llm_runnable))
        wf.add_node(
            "primary_assistant_tools",
            create_tool_node_with_fallback(primary_assistant_tools),
        )
        wf.add_conditional_edges(
            "primary_assistant",
            route_primary_assistant,
            [
                "human_chat",
                "enter_update_flight",
                "enter_develop_mode",
                "enter_article_writer",
                # "enter_book_car_rental",
                # "enter_book_hotel",
                # "enter_book_excursion",
                "primary_assistant_tools",
                END,
            ],
        )
        wf.add_edge("primary_assistant_tools", "primary_assistant")

        wf.add_node("human_chat", HumanNode(llm_runnable))
        wf.add_edge("human_chat", "primary_assistant")

        # ------------------------------
        # leave_skill
        wf.add_node("leave_skill", pop_dialog_state)
        wf.add_edge("leave_skill", "primary_assistant")

        # ------------------------------
        # Flight booking assistant
        await self.add_enter_update_flight(wf)
        # ------------------------------
        # Develop mode
        await self.add_enter_develop_mode(wf)

        # ------------------------------
        # article_writer
        await WriteArticleNode.addto_primary_assistant(wf)

        return wf

    async def add_enter_update_flight(self, wf: StateGraph):
        llm_runnable = await mtmai_context.get_llm_openai("chat")

        wf.add_node(
            "enter_update_flight",
            create_entry_node("Flight Updates & Booking Assistant", "update_flight"),
        )
        wf.add_node("update_flight", FlightBookingNode(llm_runnable))
        wf.add_edge("enter_update_flight", "update_flight")
        wf.add_node(
            "update_flight_sensitive_tools",
            create_tool_node_with_fallback(update_flight_sensitive_tools),
        )
        wf.add_node(
            "update_flight_safe_tools",
            create_tool_node_with_fallback(update_flight_safe_tools),
        )

        wf.add_edge("update_flight_sensitive_tools", "update_flight")
        wf.add_edge("update_flight_safe_tools", "update_flight")
        wf.add_conditional_edges(
            "update_flight",
            route_update_flight,
            [
                "update_flight_sensitive_tools",
                "update_flight_safe_tools",
                "leave_skill",
                END,
            ],
        )
    async def add_enter_develop_mode(self, wf: StateGraph):
        llm_runnable = await mtmai_context.get_llm_openai("chat")

        wf.add_node(
            "enter_develop_mode",
            create_entry_node("Developer Mode & Development Assistant", "develop_mode"),
        )
        wf.add_node("develop_mode", DevelopNode(llm_runnable))
        wf.add_edge("enter_develop_mode", "develop_mode")
        wf.add_node(
            "develop_sensitive_tools",
            create_tool_node_with_fallback(develop_sensitive_tools),
        )
        wf.add_node(
            "develop_safe_tools",
            create_tool_node_with_fallback(develop_safe_tools),
        )

        wf.add_edge("develop_sensitive_tools", "develop_mode")
        wf.add_edge("develop_safe_tools", "develop_mode")
        wf.add_conditional_edges(
            "develop_mode",
            route_develop_mode,
            [
                "develop_sensitive_tools",
                "develop_safe_tools",
                "leave_skill",
                # END,
            ],
        )


    async def get_compiled_graph(self) -> CompiledGraph:
        graph = (await self.create_graph()).compile(
            checkpointer=await mtmai_context.get_graph_checkpointer(),
            # interrupt_after=["human_chat"],
            interrupt_before=[
                "human_chat",
                "update_flight_sensitive_tools",
                "develop_sensitive_tools",
                # "book_car_rental_sensitive_tools",
                # "book_hotel_sensitive_tools",
                # "book_excursion_sensitive_tools",
            ],
            debug=True,
        )

        image_data = graph.get_graph(xray=1).draw_mermaid_png()
        save_to = "./graph.png"
        with open(save_to, "wb") as f:
            f.write(image_data)
        return graph
