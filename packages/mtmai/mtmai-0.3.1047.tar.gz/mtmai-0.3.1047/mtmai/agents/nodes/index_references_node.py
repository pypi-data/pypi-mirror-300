from langchain_core.documents import Document
from langchain_core.runnables import Runnable, RunnableConfig

from mtmai.agents.ctx import get_mtmai_ctx
from mtmai.agents.states.research_state import ResearchState
from mtmai.core.logging import get_logger

logger = get_logger()


class IndexReferencesNode:
    def __init__(self, runnable: Runnable):
        self.runnable = runnable

    def node_name(self):
        return "index_references"

    async def __call__(self, state: ResearchState, config: RunnableConfig):
        logger.info(f"进入 index_references node: {state}")
        ctx = get_mtmai_ctx()
        vs = ctx.vectorstore

        all_docs = []
        for interview_state in state["interview_results"]:
            reference_docs = [
                Document(page_content=v, metadata={"source": k})
                for k, v in interview_state["references"].items()
            ]
            all_docs.extend(reference_docs)
        # await vectorstore.aadd_documents(all_docs)
        await vs.aadd_documents(all_docs)
        return state
