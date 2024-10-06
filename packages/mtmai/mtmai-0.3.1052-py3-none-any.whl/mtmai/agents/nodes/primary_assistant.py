from datetime import datetime

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable, RunnableConfig
from langgraph.graph import END
from langgraph.prebuilt import tools_condition
from pydantic import BaseModel, Field

from mtmai.agents.ctx import mtmai_context

from mtmai.agents.nodes.article_writer_node import ToArticleWriterAssistant
from mtmai.agents.tools.tools import search_flights
from mtmai.core.logging import get_logger
from mtmai.models.graph_config import HomeChatState

logger = get_logger()


class ToFlightBookingAssistant(BaseModel):
    """Transfers work to a specialized assistant to handle flight updates and cancellations."""

    request: str = Field(
        description="Any necessary followup questions the update flight assistant should clarify before proceeding."
    )

class ToDevelopAssistant(BaseModel):
    """Transfers work to a specialized assistant to handle development tasks."""

    request: str = Field(
        description="Any necessary followup questions or specific development tasks the developer assistant should address."
    )



class ToBookCarRental(BaseModel):
    """Transfers work to a specialized assistant to handle car rental bookings."""

    location: str = Field(
        description="The location where the user wants to rent a car."
    )
    start_date: str = Field(description="The start date of the car rental.")
    end_date: str = Field(description="The end date of the car rental.")
    request: str = Field(
        description="Any additional information or requests from the user regarding the car rental."
    )

    class Config:
        json_schema_extra = {
            "example": {
                "location": "Basel",
                "start_date": "2023-07-01",
                "end_date": "2023-07-05",
                "request": "I need a compact car with automatic transmission.",
            }
        }


class ToHotelBookingAssistant(BaseModel):
    """Transfer work to a specialized assistant to handle hotel bookings."""

    location: str = Field(
        description="The location where the user wants to book a hotel."
    )
    checkin_date: str = Field(description="The check-in date for the hotel.")
    checkout_date: str = Field(description="The check-out date for the hotel.")
    request: str = Field(
        description="Any additional information or requests from the user regarding the hotel booking."
    )

    class Config:
        json_schema_extra = {
            "example": {
                "location": "Zurich",
                "checkin_date": "2023-08-15",
                "checkout_date": "2023-08-20",
                "request": "I prefer a hotel near the city center with a room that has a view.",
            }
        }


class ToBookExcursion(BaseModel):
    """Transfers work to a specialized assistant to handle trip recommendation and other excursion bookings."""

    location: str = Field(
        description="The location where the user wants to book a recommended trip."
    )
    request: str = Field(
        description="Any additional information or requests from the user regarding the trip recommendation."
    )

    class Config:
        json_schema_extra = {
            "example": {
                "location": "Lucerne",
                "request": "The user is interested in outdoor activities and scenic views.",
            }
        }


primary_assistant_tools = [
    # TavilySearchResults(max_results=1),
    search_flights,
    # lookup_policy,
]


def route_primary_assistant(
    state: HomeChatState,
):
    route = tools_condition(state)
    if route == END:
        # 这里的工具调用名称，本质是路由表达
        # 如果没有路由，则转到 human_chat 节点，获取用户新输入的消息
        # return END
        return "human_chat"
    tool_calls = state.messages[-1].tool_calls
    if tool_calls:
        route_to = tool_calls[0]["name"]
        logger.info(f"route_primary_assistant: {route_to}")
        if route_to == ToFlightBookingAssistant.__name__:
            return "enter_update_flight"
        elif route_to == ToDevelopAssistant.__name__:
            return "enter_develop_mode"
        elif route_to ==  ToArticleWriterAssistant.__name__:
            return "enter_article_writer"
        elif route_to == ToBookCarRental.__name__:
            return "enter_book_car_rental"
        return "primary_assistant_tools"
    raise ValueError("Invalid route")


class PrimaryAssistantNode:
    def __init__(self, runnable: Runnable):
        self.runnable = runnable

    async def __call__(self, state: HomeChatState, config: RunnableConfig):
        messages = state.messages
        primary_assistant_prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are a helpful customer support assistant for Website Helper, assisting users in using this system and answering user questions. "
                    "Your primary role is to search for flight information and company policies to answer customer queries. "
                    "If a customer requests to update or cancel a flight, book a car rental, book a hotel, or get trip recommendations, "
                    "delegate the task to the appropriate specialized assistant by invoking the corresponding tool. You are not able to make these types of changes yourself."
                    " Only the specialized assistants are given permission to do this for the user."
                    "The user is not aware of the different specialized assistants, so do not mention them; just quietly delegate through function calls. "
                    "Provide detailed information to the customer, and always double-check the database before concluding that information is unavailable. "
                    " When searching, be persistent. Expand your query bounds if the first search returns no results. "
                    " If a search comes up empty, expand your search before giving up."
                    "\n\nCurrent user flight information:\n<Flights>\n{user_info}\n</Flights>"
                    "\n 必须使用中文回复用户"
                    "\nCurrent time: {time}."
                    "{additional_instructions}",
                ),
                ("placeholder", "{messages}"),
            ]
        ).partial(time=datetime.now())

        tools = primary_assistant_tools  + [
                ToFlightBookingAssistant,
                ToBookCarRental,
                ToDevelopAssistant,
            ]
        ai_msg = await mtmai_context.ainvoke_model(primary_assistant_prompt, state, tools=tools)
        return {"messages": ai_msg}
