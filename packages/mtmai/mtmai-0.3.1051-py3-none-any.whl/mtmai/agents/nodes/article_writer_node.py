from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable, RunnableConfig
from matplotlib.pyplot import cla
from mtmai.models.graph_config import HomeChatState
from langgraph.graph import END, StateGraph

from datetime import datetime
from mtmai.agents.graphutils import (
    create_entry_node,
    create_tool_node_with_fallback,
    ensure_valid_llm_response_v2,
)

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable, RunnableConfig
from langgraph.graph import END
from langgraph.prebuilt import tools_condition
from mtmai.agents.ctx import mtmai_context


from mtmai.agents.graphutils import CompleteOrEscalate
from mtmai.agents.tools.tools import (
    develop_tools,
    develop_safe_tools,
    search_flights
)
from mtmai.core.logging import get_logger
from mtmai.models.graph_config import HomeChatState
from pydantic import BaseModel, Field
from mtmai.agents.ctx import mtmai_context


logger = get_logger()


article_writer_safe_tools = [search_flights]
article_writer_sensitive_tools = []
article_writer_tools = article_writer_safe_tools + article_writer_sensitive_tools


class ToArticleWriterAssistant(BaseModel):
    """Transfers work to a specialized assistant to handle article writing tasks."""

    request: str = Field(
        description="Any necessary followup questions or specific article writing tasks the article writer assistant should address."
    )
    topic: str = Field(
        description="The main topic or subject of the article to be written."
    )
    target_audience: str = Field(
        description="The intended audience for the article, to help tailor the writing style and content."
    )
    word_count: int = Field(
        description="The approximate number of words required for the article."
    )

def route_article_writer(
    state: HomeChatState,
):
    route = tools_condition(state.messages)
    if route == END:
        return END
    tool_calls = state.messages[-1].tool_calls
    did_cancel = any(tc["name"] == CompleteOrEscalate.__name__ for tc in tool_calls)
    if did_cancel:
        return "leave_skill"
    safe_toolnames = [t.name for t in develop_safe_tools]
    if all(tc["name"] in safe_toolnames for tc in tool_calls):
        return "develop_safe_tools"
    return "develop_sensitive_tools"

class WriteArticleNode:
    def __init__(self, runnable: Runnable):
        self.runnable = runnable

    def node_name(self):
        return "article_writer"

    async def __call__(
        self,
        state: HomeChatState,
        config: RunnableConfig,
    ):
        article_writer_prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are a specialized assistant for writing articles. "
                    "The primary assistant delegates work to you whenever the user needs help with article writing tasks. "
                    "You can use various tools to assist in article writing, such as searching for information, fact-checking, and organizing content. "
                    "Be creative, informative, and engaging in your writing. "
                    "If a task requires multiple steps, guide the user through the article writing process clearly. "
                    "If you need more information or if the task is beyond your capabilities, escalate the task back to the main assistant. "
                    "Remember to use appropriate writing techniques and provide well-structured, coherent articles. "
                    "Always prioritize accuracy, clarity, and the target audience in your writing."

                    "\nCurrent time: {time}."
                    "\n Do not use tools that are not in the provided list."
                    "\n\nIf the user needs help, and none of your tools are appropriate for it, then"
                    ' "CompleteOrEscalate" the dialog to the host assistant. Do not waste the user\'s time. Do not make up invalid tools or functions.',
                ),
                ("placeholder", "{messages}"),
            ]
        ).partial(time=datetime.now())

        # article_writer_runnable = article_writer_prompt | self.runnable.bind_tools(
        #     article_writer_tools + [CompleteOrEscalate]
        # )
        return {
            "messages": await mtmai_context.ainvoke_model(article_writer_prompt, state, tools=article_writer_tools + [CompleteOrEscalate])
        }

    @classmethod
    async def addto_primary_assistant(cls, wf: StateGraph):
        llm_runnable = await mtmai_context.get_llm_openai("chat")

        wf.add_node(
            "enter_article_writer",
            create_entry_node("Article writer Assistant", "article_writer"),
        )
        wf.add_node("article_writer", WriteArticleNode(llm_runnable))
        wf.add_edge("enter_article_writer", "article_writer")
        wf.add_node(
            "article_writer_sensitive_tools",
            create_tool_node_with_fallback(article_writer_sensitive_tools),
        )
        wf.add_node(
            "article_writer_safe_tools",
            create_tool_node_with_fallback(article_writer_safe_tools),
        )

        wf.add_edge("article_writer_sensitive_tools", "article_writer")
        wf.add_edge("article_writer_safe_tools", "article_writer")
        wf.add_conditional_edges(
            "article_writer",
            route_article_writer,
            [
                "article_writer_sensitive_tools",
                "article_writer_safe_tools",
                "leave_skill",
                # END,
            ],
        )
