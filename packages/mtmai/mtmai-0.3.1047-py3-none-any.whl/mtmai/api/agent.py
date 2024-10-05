import logging

from fastapi import APIRouter
from langgraph.graph.state import CompiledStateGraph
from pydantic import BaseModel
from sqlmodel import SQLModel, func, select

from mtmai.deps import OptionalUserDep, SessionDep
from mtmai.models.agent import AgentBootstrap, AgentMeta, UiMessage, UiMessageBase
from mtmai.models.form import CommonFormData, CommonFormField

router = APIRouter()

logger = logging.getLogger()
graphs: dict[str, CompiledStateGraph] = {}


class AgentsPublic(SQLModel):
    data: list[AgentMeta]
    count: int


@router.get("/agent_bootstrap", response_model=AgentBootstrap)
async def agent_bootstrap(user: OptionalUserDep, db: SessionDep):
    """
    获取 agent 的配置，用于前端加载agent的配置
    """
    logger.info("agent_bootstrap")
    return AgentBootstrap(is_show_fab=True)


@router.get(
    "",
    summary="获取 Agent 列表",
    description=(
        "此端点用于获取 agent 列表。支持分页功能"
        "可以通过 `skip` 和 `limit` 参数控制返回的 agent 数量。"
    ),
    response_description="返回包含所有 agent 的列表及总数。",
    response_model=AgentsPublic,
    responses={
        200: {
            "description": "成功返回 agent 列表",
            "content": {
                "application/json": {
                    "example": {
                        "data": [
                            {"name": "agent1", "status": "active"},
                            {"name": "agent2", "status": "inactive"},
                        ],
                        "count": 2,
                    }
                }
            },
        },
        401: {"description": "未经授权的请求"},
        500: {"description": "服务器内部错误"},
    },
)
@router.get(
    "/image/{agent}",
    summary="获取工作流图像",
    description="此端点通过给定的 agent ID，生成工作流的图像并返回 PNG 格式的数据。",
    response_description="返回 PNG 格式的工作流图像。",
    responses={
        200: {"content": {"image/png": {}}},
        404: {"description": "Agent 未找到"},
    },
)
# async def image(user: OptionalUserDep, graphapp: GraphAppDep):
#     image_data = graphapp.get_graph(xray=1).draw_mermaid_png()
#     return Response(content=image_data, media_type="image/png")


# class AgentStateRequest(BaseModel):
#     agent_id: str | None = None
#     thread_id: str


# @router.post(
#     "/state",
#     summary="获取工作流状态",
#     description="",
#     response_description="返回工作流当前完整状态数据",
# )
# async def state(req: AgentStateRequest, user: OptionalUserDep, graphapp: GraphAppDep):
#     thread: RunnableConfig = {
#         "configurable": {"thread_id": req.thread_id},
#         "recursion_limit": 200,
#     }
#     state = await graphapp.aget_state(thread)
#     return state


# class CompletinRequest(BaseModel):
#     thread_id: str | None = None
#     chat_id: str | None = None
#     prompt: str
#     option: str | None = None
#     task: dict | None = None





class TaskFormRequest(BaseModel):
    task_name: str


class TaskFormResponse(BaseModel):
    form: CommonFormData


@router.post("/task_form", response_model=TaskFormResponse)
async def task_form(req: TaskFormRequest, user: OptionalUserDep, db: SessionDep):
    """根据任务请求，返回任务表单"""
    # 开发中，暂时返回固定的表单

    result = TaskFormResponse(
        form=CommonFormData(
            title="随机生成一篇文章",
            fields=[
                CommonFormField(name="title", label="标题", type="text", required=True),
                CommonFormField(
                    name="content", label="内容", type="text", required=True
                ),
            ],
        )
    )

    return result


class ChatMessagesItem(UiMessageBase):
    id: str


class ChatMessagesResponse(SQLModel):
    data: list[ChatMessagesItem]
    count: int


class AgentChatMessageRequest(SQLModel):
    chat_id: str
    skip: int = 0
    limit: int = 100


@router.post("/chat_messages", response_model=ChatMessagesResponse)
async def messages(session: SessionDep, req: AgentChatMessageRequest):
    """获取聊天消息"""
    count_statement = (
        select(func.count())
        .select_from(UiMessage)
        .where(UiMessage.chatbot_id == req.chat_id)
    )
    count = session.exec(count_statement).one()
    statement = (
        select(UiMessage)
        .where(UiMessage.chatbot_id == req.chat_id)
        .offset(req.skip)
        .limit(req.limit)
    )
    items = session.exec(statement).all()
    return ChatMessagesResponse(data=items, count=count)


# class AgentTaskPublic(AgentTaskBase):
#     id: str
#     # owner_id: str


# class AgentTaskResponse(SQLModel):
#     data: list[AgentTaskPublic]
#     count: int

# @router.get("", response_model=AgentTaskResponse)
# def items(
#     session: SessionDep, current_user: OptionalUserDep, skip: int = 0, limit: int = 100
# ) :
#     """
#     Retrieve items.
#     """
#     if current_user.is_superuser:
#         count_statement = select(func.count()).select_from(Item)
#         count = session.exec(count_statement).one()
#         statement = select(AgentTask).offset(skip).limit(limit)
#         items = session.exec(statement).all()
#     else:
#         count_statement = (
#             select(func.count())
#             .select_from(AgentTask)
#             .where(AgentTask.user_id == current_user.id)
#         )
#         count = session.exec(count_statement).one()
#         statement = (
#             select(AgentTask)
#             .where(AgentTask.user_id == current_user.id)
#             .offset(skip)
#             .limit(limit)
#         )
#         items = session.exec(statement).all()

#     return AgentTaskResponse(data=items, count=count)
