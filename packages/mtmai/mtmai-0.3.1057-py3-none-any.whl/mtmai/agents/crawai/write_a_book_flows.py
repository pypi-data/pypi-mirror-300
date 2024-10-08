import asyncio
from typing import List

from pydantic import BaseModel

from mtmai.agents.crawai.outline_crew import OutlineCrew
from mtmai.agents.crawai.types import Chapter, ChapterOutline
from mtmai.agents.crawai.write_book_chapter_crew import WriteBookChapterCrew
from mtmai.agents.ctx import mtmai_context
from mtmai.core.logging import get_logger
from mtmai.crewai.flow.flow import Flow, listen, start

logger = get_logger()


class BookState(BaseModel):
    title: str = "The Current State of AI in September 2024: Trends Across Industries and What's Next"
    book: List[Chapter] = []
    book_outline: List[ChapterOutline] = []
    topic: str = "Exploring the latest trends in AI across different industries as of September 2024"
    goal: str = """
        The goal of this book is to provide a comprehensive overview of the current state of artificial intelligence in September 2024.
        It will delve into the latest trends impacting various industries, analyze significant advancements,
        and discuss potential future developments. The book aims to inform readers about cutting-edge AI technologies
        and prepare them for upcoming innovations in the field.
    """


class BookFlow(Flow[BookState]):
    initial_state = BookState

    @start()
    async def generate_book_outline(self):
        logger.info("Kickoff the Book Outline Crew")
        llm = await mtmai_context.get_crawai_llm()

        outline_crew = OutlineCrew(llm).crew()
        output = await outline_crew.kickoff_async(
            inputs={
                "topic": self.state.topic,
                "goal": self.state.goal,
            }
        )

        chapters = output["chapters"]
        logger.info("Chapters: %s", chapters)

        self.state.book_outline = chapters
        return chapters

    @listen(generate_book_outline)
    async def write_chapters(self):
        logger.info("Writing Book Chapters")
        tasks = []

        llm = await mtmai_context.get_crawai_llm()

        async def write_single_chapter(chapter_outline):
            output = await (
                WriteBookChapterCrew(llm)
                .crew()
                .kickoff_async(
                    inputs={
                        "goal": self.state.goal,
                        "topic": self.state.topic,
                        "chapter_title": chapter_outline.title,
                        "chapter_description": chapter_outline.description,
                        "book_outline": [
                            chapter_outline.model_dump_json()
                            for chapter_outline in self.state.book_outline
                        ],
                    }
                )
            )
            title = output["title"]
            content = output["content"]
            chapter = Chapter(title=title, content=content)
            return chapter

        for chapter_outline in self.state.book_outline:
            print(f"Writing Chapter: {chapter_outline.title}")
            print(f"Description: {chapter_outline.description}")
            # Schedule each chapter writing task
            task = asyncio.create_task(write_single_chapter(chapter_outline))
            tasks.append(task)

        # Await all chapter writing tasks concurrently
        chapters = await asyncio.gather(*tasks)
        print("Newly generated chapters:", chapters)
        self.state.book.extend(chapters)

        logger.info("Book Chapters %s", self.state.book)

    @listen(write_chapters)
    async def join_and_save_chapter(self):
        logger.info("Joining and Saving Book Chapters")
        # Combine all chapters into a single markdown string
        book_content = ""

        for chapter in self.state.book:
            # Add the chapter title as an H1 heading
            book_content += f"# {chapter.title}\n\n"
            # Add the chapter content
            book_content += f"{chapter.content}\n\n"

        # The title of the book from self.state.title
        book_title = self.state.title

        # Create the filename by replacing spaces with underscores and adding .md extension
        filename = f"./{book_title.replace(' ', '_')}.md"

        # Save the combined content into the file
        with open(filename, "w", encoding="utf-8") as file:
            file.write(book_content)

        logger.info("Book saved as %s", filename)
        return book_content
