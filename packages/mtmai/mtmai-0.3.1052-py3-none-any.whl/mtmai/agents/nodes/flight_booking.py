from datetime import datetime

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable, RunnableConfig
from langgraph.graph import END
from langgraph.prebuilt import tools_condition
from mtmai.agents.ctx import mtmai_context


from mtmai.agents.graphutils import CompleteOrEscalate
from mtmai.agents.tools.tools import (
    update_flight_safe_tools,
    update_flight_tools,
)
from mtmai.core.logging import get_logger
from mtmai.models.graph_config import HomeChatState

logger = get_logger()


def route_update_flight(
    state: HomeChatState,
):
    route = tools_condition(state.messages)
    if route == END:
        return END
    tool_calls = state.messages[-1].tool_calls
    did_cancel = any(tc["name"] == CompleteOrEscalate.__name__ for tc in tool_calls)
    if did_cancel:
        return "leave_skill"
    safe_toolnames = [t.name for t in update_flight_safe_tools]
    if all(tc["name"] in safe_toolnames for tc in tool_calls):
        return "update_flight_safe_tools"
    return "update_flight_sensitive_tools"


class FlightBookingNode:
    def __init__(self, runnable: Runnable):
        self.runnable = runnable

    async def __call__(self, state: HomeChatState, config: RunnableConfig):
        flight_booking_prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are a specialized assistant for handling flight updates. "
                    " The primary assistant delegates work to you whenever the user needs help updating their bookings. "
                    "Confirm the updated flight details with the customer and inform them of any additional fees. "
                    " When searching, be persistent. Expand your query bounds if the first search returns no results. "
                    "If you need more information or the customer changes their mind, escalate the task back to the main assistant."
                    " Remember that a booking isn't completed until after the relevant tool has successfully been used."
                    "\n\nCurrent user flight information:\n<Flights>\n{user_info}\n</Flights>"
                    "\nCurrent time: {time}."
                    "\n\nIf the user needs help, and none of your tools are appropriate for it, then"
                    ' "CompleteOrEscalate" the dialog to the host assistant. Do not waste the user\'s time. Do not make up invalid tools or functions.'
                    "{additional_instructions}"                    ,
                ),
                ("placeholder", "{messages}"),
            ]
        ).partial(time=datetime.now())
        return {
            "messages": await mtmai_context.ainvoke_model(
                flight_booking_prompt,
                state,tools=update_flight_tools + [CompleteOrEscalate]
            )
        }
