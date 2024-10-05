from langchain_core.runnables import Runnable, RunnableConfig

from mtmai.agents.ctx import get_mtmai_ctx
from mtmai.core.logging import get_logger
from mtmai.models.chat import ThreadUIState
from mtmai.models.graph_config import HomeChatState

logger = get_logger()


class OnChatStartNode:
    def __init__(self, runnable: Runnable):
        self.runnable = runnable

    async def __call__(self, state: HomeChatState, config: RunnableConfig):
        logger.info("on_chat_start_node")
        ctx = get_mtmai_ctx()


        return {
            "messages": [],
            "thread_ui_state": ThreadUIState(
                isOpen=True,
                fabDisplayText="Mtm AI2",
            ),
        }
