from langchain_core.messages import AIMessage, HumanMessage

from mtmai.core.logging import get_logger

logger = get_logger()


def swap_roles(state: InterviewState, name: str):
    converted = []
    for message in state["messages"]:
        if isinstance(message, AIMessage) and message.name != name:
            message = HumanMessage(**message.dict(exclude={"type"}))
        converted.append(message)
    return {"messages": converted}
