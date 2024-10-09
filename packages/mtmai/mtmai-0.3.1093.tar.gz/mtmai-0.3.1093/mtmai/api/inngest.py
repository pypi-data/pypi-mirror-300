# from ast import boolop
# import logging

# import inngest
# from fastapi import APIRouter, FastAPI

# from mtmai.agents.article_gen import (
#     GenBookRequest,
#     WriteOutlineRequest,
#     article_gen_outline,
# )
# from mtmai.models.book_gen import BookOutline
# from mtmai.mtlibs.inngest import inngest_client

# router = APIRouter()
# logger = logging.getLogger()


# @inngest_client.create_function(
#     fn_id="task_gen_outlink",
#     trigger=inngest.TriggerEvent(event="mtmai/task_gen_outlink"),
# )
# async def task_gen_outlink(ctx: inngest.Context, step: inngest.Step) -> str:
#     output = await article_gen_outline(
#         req=WriteOutlineRequest.model_validate(ctx.event.data)
#     )
#     return output


# @inngest_client.create_function(
#     fn_id="write_book_chapter",
#     trigger=inngest.TriggerEvent(event="mtmai/write_book_chapter"),
# )
# async def write_book_chapter(ctx: inngest.Context, step: inngest.Step) -> str:
#     req = GenBookRequest()
#     output = await step.invoke(
#         "invoke",
#         function=task_gen_outlink,
#         data=req.model_dump(),
#     )
#     return output


# @inngest_client.create_function(
#     fn_id="gen_book",
#     trigger=inngest.TriggerEvent(event="mtmai/gen_book"),
# )
# async def gen_book(ctx: inngest.Context, step: inngest.Step) -> str:
#     gen_book_req = GenBookRequest()
#     outlines = await step.invoke(
#         "invoke",
#         function=task_gen_outlink,
#         data=WriteOutlineRequest(
#             topic=gen_book_req.topic,
#             goal=gen_book_req.goal,
#         ),
#     )
#     gen_book_req.book_outline = BookOutline.model_validate(outlines)
#     logger.info(gen_book_req.book_outline)

#     chapters = outlines["chapters"]

#     for chapter_outline in gen_book_req.book_outline:
#         logger.info(f"Writing Chapter: {chapter_outline.title}")
#         logger.info(f"Description: {chapter_outline.description}")
#         # Schedule each chapter writing task
#         # task = asyncio.create_task(write_single_chapter(chapter_outline))
#         # tasks.append(task)
#     # title = output["title"]
#     # content = output["content"]
#     # chapter = Chapter(title=title, content=content)
#     # return chapter


# def setup_inngest(app: FastAPI):
#     inngest.fast_api.serve(
#         app,
#         inngest_client,
#         [write_book_chapter, gen_book, task_gen_outlink],
#     )
