import json
import logging
from functools import lru_cache

from fastapi.encoders import jsonable_encoder
from langchain_core.messages import ChatMessage
from langchain_core.runnables import RunnableConfig
from networkx import gn_graph
from pydantic import BaseModel
from sqlmodel import Session, select

from mtmai.models.agent import Chatbot, UiMessage
from mtmai.models.models import User
from mtmai.mtlibs import aisdk, mtutils
import mtmai.chainlit as cl
from mtmai.agents.ctx import get_mtmai_ctx

logger = logging.getLogger()


@lru_cache(maxsize=1000)
async def get_graph_by_name(name: str):
    if name == "storm":
        from mtmai.agents.graphs.storm import StormGraph

        return StormGraph()
    if name == "joke_graph":
        from mtmai.agents.graphs.joke_graph import JokeGraph

        return JokeGraph()
    return None


class ChatCompletinRequest(BaseModel):
    thread_id: str | None = None
    chat_id: str | None = None
    prompt: str
    option: str | None = None
    task: dict | None = None


async def agent_event_stream(
    *,
    model: str | None = None,
    session: Session,
    user: User,
    prompt: str,
    chat_id: str | None = None,
    thread_id: str | None = None,
):
    graph_name = model
    graph = await gn_graph(graph_name)
    if not graph:
        raise Exception(status_code=503, detail=f"No atent model found: {model}")

    if not chat_id:
        # 如果没有提供 chat_id，创建新的 chat
        chatbot = Chatbot(
            name="New Chat",
            description="New Chat",
        )
        session.add(chatbot)
        session.commit()
        chat_id = chatbot.id
        # 通知前端创建了新的chat_id
        yield aisdk.data(
            {
                "chat_id": chatbot.id,
            }
        )
    else:
        # 确保提供的 chat_id 存在
        chatbot = session.exec(select(Chatbot).where(Chatbot.id == chat_id)).first()
        if not chatbot:
            # 如果提供的 chat_id 不存在，创建新的 chat
            chatbot = Chatbot(
                name="New Chat",
                description="New Chat",
            )
            session.add(chatbot)
            session.commit()
            chat_id = chatbot.id
            # 通知前端创建了新的chat_id
            yield aisdk.data(
                {
                    "chat_id": chatbot.id,
                }
            )

    new_message = UiMessage(
        component="UserMessage",
        content=prompt,
        props={"content": prompt},
        chatbot_id=chat_id,
        role="user",
    )
    session.add(new_message)
    session.commit()

    # 加载聊天消息历史
    # FIXME: 用户消息的加载有待优化
    chat_messages = session.exec(
        select(UiMessage)
        .where(UiMessage.chatbot_id == chat_id)
        .order_by(UiMessage.created_at)
    ).all()

    # 从数据库的聊天记录构造 langgraph 的聊天记录
    langgraph_messages = []
    for message in chat_messages:
        if message.content:
            langgraph_message = ChatMessage(
                role="user" if message.role == "user" else "assistant",
                content=message.content if message.role == "user" else message.response,
            )
            langgraph_messages.append(langgraph_message)

    if not thread_id:
        thread_id = mtutils.gen_orm_id_key()
    thread: RunnableConfig = {
        "configurable": {
            "thread_id": thread_id,
            "user_id": user.id,
            "chat_id": chat_id,
        }
    }

    inputs = {
        "user_id": user.id,
        "user_input": prompt,
        "messages": [*langgraph_messages],
    }
    state = await graph.aget_state(thread)

    if state.created_at is not None:
        # 是人机交互继续执行的情况
        await graph.aupdate_state(
            thread,
            inputs,
            as_node="human_node",
        )
        inputs = None

    async for event in graph.astream_events(
        inputs,
        version="v2",
        config=thread,
    ):
        thread_id = thread.get("configurable").get("thread_id")
        user_id = user.id
        kind = event["event"]
        node_name = event["name"]
        data = event["data"]
        logger.info("kind: %s, node_name:%s", kind, node_name)
        if kind == "on_chat_model_stream":
            if event["metadata"].get("langgraph_node") == "human_node":
                content = data["chunk"].content
                if content:
                    yield aisdk.text(content)

            if event["metadata"].get("langgraph_node") == "final":
                logger.info("终结节点")

        if kind == "on_chain_stream":
            if data and node_name == "entry_node":
                chunk_data = data.get("chunk", {})
                picked_data = {
                    key: chunk_data[key]
                    for key in ["ui_messages", "uistate"]
                    if key in chunk_data
                }

                if picked_data:
                    yield aisdk.data(picked_data)
        if kind == "on_chain_end":
            chunk_data = data.get("chunk", {})

            if node_name == "human_node":
                output = data.get("output")
                if output:
                    artifacts = data.get("output").get("artifacts")
                    if artifacts:
                        yield aisdk.data({"artifacts": artifacts})

                ui_messages = output.get("ui_messages", [])
                if len(ui_messages) > 0:
                    for uim in ui_messages:
                        db_ui_message2 = UiMessage(
                            # thread_id=thread_id,
                            chatbot_id=chat_id,
                            user_id=user_id,
                            component=uim.component,
                            content=uim.content,
                            props=uim.props,
                            artifacts=uim.artifacts,
                        )
                        session.add(db_ui_message2)
                        session.commit()

                    # 跳过前端已经乐观更新的组件
                    skip_components = ["UserMessage", "AiCompletion"]
                    filterd_components = [
                        x for x in ui_messages if x.component not in skip_components
                    ]
                    yield aisdk.data(
                        {
                            "ui_messages": filterd_components,
                        }
                    )
                if output.get("uistate"):
                    yield aisdk.data(
                        {
                            "uistate": output.get("uistate"),
                        }
                    )

            # if node_name == "entry_node":
            #     task_title = data.get("task_title", "no-title")
            #     item = AgentTask(thread_id=thread_id, user_id=user_id, title=task_title)
            #     session.add(item)
            #     session.commit()

            if node_name == "LangGraph":
                logger.info("中止节点")
                if (
                    data
                    and (output := data.get("output"))
                    and (final_messages := output.get("messages"))
                ):
                    for message in final_messages:
                        message.pretty_print()

        if kind == "on_tool_start":
            logger.info("(@stream)工具调用开始 %s", node_name)
        # if kind == "on_tool_end":
        #     output = data.get("output")
        #     if output and output.artifact:
        #         yield aisdk.data(output.artifact)

    yield aisdk.finish()



async def agent_event_stream_v2(
    *,
    model: str | None = None,
    inputs: dict,
    debug: bool = False,
):
    current_step = cl.context.current_step
    ctx = get_mtmai_ctx()
    graph = await ctx.get_compiled_graph(model)

    thread_id = mtutils.gen_orm_id_key()
    thread: RunnableConfig = {
        "configurable": {
            "thread_id": thread_id,
        }
    }

    async for event in graph.astream_events(
        inputs,
        version="v2",
        config=thread,
        subgraphs=True,
    ):
        thread_id = thread.get("configurable").get("thread_id")
        # user_id = user.id
        kind = event["event"]
        node_name = event["name"]
        data = event["data"]

        current_state = await graph.aget_state(thread, subgraphs=True)
        # logger.info("current_state next: %s", current_state.next)
        graph_step = -1
        if current_state and current_state.metadata:
            graph_step = current_state.metadata.get("step")  # 第几步

        if kind == "on_chain_start":
            if node_name == "LangGraph":
                await cl.Message(content="流程开始").send()
            elif not is_internal_node(node_name):  # 跳过内部节点
                await cl.Message(
                    content="开始 %s, 第 %s 步" % (node_name, graph_step)
                ).send()

        elif kind == "on_chat_model_start":
            if debug:
                await cl.Message(content="调用大语言模型开始").send()
        elif kind == "on_chat_model_end":
            elements = [
                cl.Text(
                    name="simple_text",
                    content=json.dumps(jsonable_encoder(data)),
                    display="inline",
                )
            ]
            await cl.Message(
                content="调用大语言模型结束",
                elements=elements,
            ).send()

        elif kind == "on_chat_model_stream":
            if event["metadata"].get("langgraph_node") == "human_node":
                content = data["chunk"].content
                if content:
                    await current_step.stream_token(content)

            if event["metadata"].get("langgraph_node") == "final":
                logger.info("终结节点")

        elif kind == "on_chat_model_end":
            output = data.get("output")
            if output:
                chat_output = output.content
                current_step.output = "节点输出：" + chat_output
                await cl.Message("节点输出：" + chat_output).send()

        # if kind == "on_chain_stream":
        #     if data and node_name == "entry_node":
        #         chunk_data = data.get("chunk", {})
        #         picked_data = {
        #             key: chunk_data[key]
        #             for key in ["ui_messages", "uistate"]
        #             if key in chunk_data
        #         }

        #         if picked_data:
        #             yield aisdk.data(picked_data)
        elif kind == "on_chain_end":
            #     chunk_data = data.get("chunk", {})

            #     if node_name == "human_node":
            #         output = data.get("output")
            #         if output:
            #             artifacts = data.get("output").get("artifacts")
            #             if artifacts:
            #                 yield aisdk.data({"artifacts": artifacts})

            if node_name == "LangGraph":
                await cl.Message(content="流程结束（或暂停）").send()
                if (
                    data
                    and (output := data.get("output"))
                    and (final_messages := output.get("messages"))
                ):
                    for message in final_messages:
                        message.pretty_print()
            else:
                if not is_internal_node(node_name):
                    await cl.Message(
                        content=f"节点 {node_name} 结束, 第 {graph_step}步"
                    ).send()

        elif kind == "on_tool_start":
            logger.info("工具调用开始 %s", node_name)
            if debug:
                await cl.Message(content=f"工具调用开始 {node_name}").send()
        elif kind == "on_tool_end":
            logger.info("工具调用结束 %s", node_name)
            await cl.Message(content=f"工具调用结束 {node_name}").send()

        else:
            logger.info("kind: %s, node_name: %s", kind, node_name)
            if debug:
                await cl.Message(content=f"其他节点 {node_name}").send()


internal_node_types = set(
    [
        "RunnableSequence",
        "RunnableLambda",
        "RunnableParallel<raw>",
        "RunnableWithFallbacks",
        "_write",
        "start",
        "end",
    ]
)


def is_internal_node(node_name: str):
    """
    判断是否是内部节点
    """
    return node_name in internal_node_types
