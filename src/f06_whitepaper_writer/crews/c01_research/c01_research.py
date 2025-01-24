import hashlib
from typing import List
from pydantic import BaseModel, Field
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, task, crew
from crewai_tools import DirectoryReadTool
import os



# Define Pydantic models for structured data
class SearchStringExtractionOutput(BaseModel):
    """Stores list of search strings to execute to gather more knowledge from the web"""
    search_strings: List[str] = Field(..., description="List of search strings to research based on the input steering text.")

# class RawResearchEntry(BaseModel):
#     title: str = Field(..., description="Article title or summarized title that is no longer than 7 words")
#     url: str = Field(..., description="URL of the raw text context scraped")
#     scraped_content: str = Field(..., description="Text scraped from the web")
#
#     @property
#     def content_hash(self) -> str:
#         """Generate a hash string based on the model's content."""
#         hash_input = f"{self.title}{self.url}{self.scraped_content}"
#         return hashlib.sha256(hash_input.encode('utf-8')).hexdigest()
#
# class WebResearchOutput(BaseModel):
#     research_entries: List[RawResearchEntry] = Field(..., description="List of research entries extracted from the web")



@CrewBase
class C01ResearchCrew:
    """C01ResearchCrew crew"""
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    # Define the tools
    dir_read_tool = DirectoryReadTool(directory=os.getenv('TEXT_STEERING_DIR'))

    @agent
    def search_string_extractor(self) -> Agent:
        """Agent responsible for extracting search strings from text."""
        return Agent(
            config=self.agents_config['search_string_extractor'],
            tools=[self.dir_read_tool],
            verbose=True
        )

    @task
    def extract_search_strings_task(self) -> Task:
        """Task to extract search strings from text files."""
        return Task(
            config=self.tasks_config['extract_search_strings_task'],
            output_pydantic=SearchStringExtractionOutput,
            expected_output="A list of search strings relevant to the topic."
        )


    @crew
    def crew(self) -> Crew:
        """Creates the C01ResearchCrew with defined agents and tasks."""
        return Crew(
            agents=self.agents,  # Automatically collected by the @agent decorator
            tasks=self.tasks,    # Automatically collected by the @task decorator
            process=Process.sequential,
            verbose=True,
        )