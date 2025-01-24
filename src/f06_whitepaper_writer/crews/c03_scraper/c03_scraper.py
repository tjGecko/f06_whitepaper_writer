import hashlib

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from pydantic import BaseModel, Field


from crewai_tools import FileWriterTool
from crewai_tools import ScrapeWebsiteTool


class ScrapeResult(BaseModel):
    url: str = Field(..., description="URL that was scraped.")
    scraped_content: str = Field(..., description="Text scraped from the web")

    @property
    def filename(self) -> str:
        """Generate a hash string based filename."""
        hash_input = self.url
        hash_str = hashlib.sha256(hash_input.encode('utf-8')).hexdigest()

        return f'result_{hash_str}.json'


@CrewBase
class C03Scraper:
    """C03Scraper crew"""
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    file_writer_tool = FileWriterTool()
    scraper_tool = ScrapeWebsiteTool()

    @agent
    def page_scraper(self) -> Agent:
        """Agent responsible for writing pages."""
        return Agent(
            config=self.agents_config['page_scraper'],
            tools=[self.scraper_tool, self.file_writer_tool],
            verbose=True
        )

    @task
    def page_scraper_task(self) -> Task:
        """Task to save research results as JSON files."""
        return Task(
            config=self.tasks_config['page_scraper_task'],
            output_pydantic=ScrapeResult,
        )

    @task
    def save_result_task(self) -> Task:
        """Task to save research results as JSON files."""
        return Task(
            config=self.tasks_config['save_result_task'],
            output_pydantic=ScrapeResult,
        )

    @crew
    def crew(self) -> Crew:
        """Creates the C02Crawler crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True
        )
