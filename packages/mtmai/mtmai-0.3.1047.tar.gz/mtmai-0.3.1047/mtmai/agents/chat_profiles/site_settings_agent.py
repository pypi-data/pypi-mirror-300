"""
GraphIterator Module
"""



import mtmai.chainlit as cl
from mtmai.agents.chat_profiles.base_chat_agent import ChatAgentBase
from mtmai.api import search
from mtmai.chainlit.context import context
from mtmai.core.db import get_async_session
from mtmai.core.logging import get_logger
from mtmai.models.chat import ChatProfile
from mtmai.models.search_index import SearchRequest
from mtmai.mtlibs.inputs.input_widget import SelectInput, ThreadForm

logger = get_logger()


class SiteSettingsAgent(ChatAgentBase):
    """
    数据管理Agent
    根据用户传入的参数，显示 列表视图，或者 详细 item 视图。
    协助用户管理 账号下的数据，例如 站点，文章，页面，用户，角色，权限，配置等
    """

    def __init__(
        self,
    ):
        pass

    async def __call__(self, state: dict, batchsize: int) -> dict:
        """"""
        # TODO: langgraph 调用入口
        return {}

    @classmethod
    def name(cls):
        return "siteSettings"

    @classmethod
    def get_chat_profile(self):
        return ChatProfile(
            name="siteSettings",
            description="站点配置",
        )

    async def chat_start(self):
        user = cl.user_session.get("user")
        if not user:
            await cl.Message(content="你还没登录，请先登录").send()
            return

        # await cl.Message(content="请选择数据类型").send()
        ask_filter_data_type = await context.emitter.send_form(
            ThreadForm(
                title="请选择数据类型",
                variant="single_select",
                inputs=[
                    SelectInput(
                        name="dataType",
                        label="",
                        values=["aa","bb","cc"],
                        items=[{
                            "label": "站点",
                            "value": "site",
                        },{
                            "label": "文章",
                            "value": "article",
                        },{
                            "label": "页面",
                            "value": "page",
                        }]
                    ),
                ],
            )
        )

        search_params= SearchRequest(
            dataType=ask_filter_data_type.get("dataType", ""),
            q="",
            skip=0,
            limit=10,
        )
        logger.info("列表查询参数 %s", search_params)

        async with get_async_session() as session:
            search_results = await search.search(session, current_user=user, req=search_params)
        logger.info("查询结果 %s", search_results)

        if not search_results.data:
            await cl.Message(content="没有数据").send()
            return


        # 执行数据查询


        # fnCall_result = await context.emitter.send_call_fn("fn_get_site_id", {})
        # siteId = fnCall_result.get("siteId", "")
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
