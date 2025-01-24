from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from typing import List
from pydantic import BaseModel, Field
from crewai_tools import SerperDevTool


class WebResearchOutput(BaseModel):
    research_entries: List[str] = Field(..., description="List of urls to scrape")



@CrewBase
class C02Crawler:
    """C02Crawler crew"""
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'
    search_tool = SerperDevTool()

    @agent
    def web_researcher(self) -> Agent:
        """Agent responsible for conducting web searches and scraping content."""
        return Agent(
            config=self.agents_config['web_researcher'],
            tools=[self.search_tool],
            verbose=True
        )

    @task
    def conduct_web_research_task(self) -> Task:
        """Task to perform web search and scrape relevant content."""
        return Task(
            config=self.tasks_config['research_task'],
            output_pydantic=WebResearchOutput,
            expected_output="A collection of research entries with titles, URLs, and scraped content.",
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
