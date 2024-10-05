from langchain_core.runnables import Runnable, RunnableConfig

from mtmai.agents.ctx import get_mtmai_ctx
from mtmai.chainlit import context
from mtmai.core.logging import get_logger
from mtmai.models.agent import CopilotScreen
from mtmai.models.chat import ThreadUIState
from mtmai.models.graph_config import HomeChatState

logger = get_logger()


class OnChatStartNode:
    def __init__(self, runnable: Runnable):
        self.runnable = runnable

    async def __call__(self, state: HomeChatState, config: RunnableConfig):
        logger.info("on_chat_start_node")
        ctx = get_mtmai_ctx()

        js_code_get_detail_info = """
var results = {};
results.fullUrl=window.location.href;
results.cookie=document.cookie;
results.title=document.title;
results.body=document.body.innerText;
(function() { return results; })();
"""
        js_eval_result = await context.emitter.send_call_fn(
            "js_eval", {"code": js_code_get_detail_info}
        )
        logger.info("js_eval_result %s", js_eval_result)


        # 调用函数检测环境

        # async with get_async_session() as session:
        #     site = await get_site_by_id(session, uuid.UUID(siteId))
        # demo_fn_call_result = await context.emitter.send_form(
        #     ThreadForm(
        #         open=True,
        #         inputs=[
        #             TextInput(
        #                 name="title",
        #                 label="站点名称",
        #                 placeholder="请输入站点名称",
        #                 description="站点名称",
        #                 value=site.title,
        #             ),
        #             TextArea(
        #                 name="description",
        #                 label="站点描述",
        #                 placeholder="请输入站点描述",
        #                 description="站点描述",
        #                 value=site.description,
        #             ),
        #         ],
        #     )
        # )
        # logger.info("表单调用结果 %s", demo_fn_call_result)
        # async with get_async_session() as session:
        #     # item = Site.model_validate(demo_fn_call_result)
        #     # site.update(demo_fn_call_result)
        #     site.sqlmodel_update(site.model_dump(), update=demo_fn_call_result)
        #     session.add(site)
        #     await session.commit()
        #     await session.refresh(site)
        # await context.emitter.emit("clear_ask_form", {})
        # res = await cl.AskUserMessage(content="What is your name?", timeout=10).send()
        # if res:
        #     await cl.Message(
        #         content="Continue!",
        #     ).send()

        return {
            "messages": [],

            "thread_ui_state": ThreadUIState(
                isOpen=True,
                layout="right_aside",
                isOpenDataView=False,
                activateViewName="/",
                fabDisplayText="Mtm AI2",
                screens=[
                        CopilotScreen(
                            id="/",
                            label="首页",
                            Icon="home",
                        ),
                        CopilotScreen(
                            id="/datas",
                            label="数据",
                            Icon="data",
                        ),
                        CopilotScreen(
                            id="/operation",
                            label="操作",
                            Icon="operation",
                        ),
                        CopilotScreen(
                            id="/playground",
                            label="play",
                            Icon="playground",
                        ),
                    ],
                playDataType="post",
                playData={
                    "title": "Hello World",
                    "content": "This is a test post",
                },
            ),
        }
