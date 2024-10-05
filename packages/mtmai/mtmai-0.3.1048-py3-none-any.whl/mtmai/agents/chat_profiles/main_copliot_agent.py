from fastapi.encoders import jsonable_encoder

import mtmai.chainlit as cl
from mtmai.agents.chat_profiles.base_chat_agent import ChatAgentBase
from mtmai.chainlit.context import context
from mtmai.core.logging import get_logger
from mtmai.models.agent import ChatBotUiStateResponse, CopilotScreen
from mtmai.models.chat import ChatProfile

logger = get_logger()


class MainCopilotAgent(ChatAgentBase):
    """
    copilot 主聊天机器人
    """

    def __init__(
        self,
    ):
        pass

    async def __call__(self, state: dict, batchsize: int) -> dict:
        """"""
        return {}

    @classmethod
    def name(cls):
        return "MainCopilotAgent"

    @classmethod
    def get_chat_profile(self):
        return ChatProfile(
            name="MainCopilotAgent",
            description="默认主聊天机器人",
        )

    # 实验：调用前端js代码
    async def chat_start(self):
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

        # 发送主配置，让客户端UI进行最基础的配置

        await context.emitter.emit(
            "ui_state_upate",
            jsonable_encoder(
                ChatBotUiStateResponse(
                    layout="right_aside",
                    fabDisplayText="Mtm AI",
                    isOpenDataView=False,
                    activateViewName="/",
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
                    ],
                )
            ),
        )

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

    async def on_message(self, message: cl.Message):
        logger.info("TODO: on_message (ChatPostGenNode)")
        pass
