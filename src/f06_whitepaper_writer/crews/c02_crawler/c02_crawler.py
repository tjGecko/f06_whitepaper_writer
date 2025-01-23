from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
# from crewai.tools import BaseTool
# from pydantic import BaseModel, Field
import os
from pathlib import Path


from crewai_tools import FileWriterTool


# class FileWriterInput(BaseModel):
#     abs_file: str = Field(..., description="Absolute path of the file to write")
#     content: str = Field(..., description="Text to write to file")
#
#
# class FileWriterTool(BaseTool):
#     name: str = "FileWriterTool"
#     description: str = "Writes given content to a specified file."
#
#     def _run(self, input_ctx: FileWriterInput) -> str:
#         try:
#             abs_path = Path(input_ctx.abs_file)  # Convert back to Path for file operations
#             with abs_path.open("w", encoding="utf-8") as fout:
#                 fout.write(input_ctx.content)
#                 return f"Content successfully written to {abs_path}"
#         except Exception as e:
#             print(f"Error writing to file: {e}")
#         return f"Failed to write to {abs_path}: {str(e)}"


@CrewBase
class C02Crawler:
    """C02Crawler crew"""
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'
    output_dir = Path(os.getenv('WEB_SEARCH_OUTPUT_DIR'))

    file_writer_tool = FileWriterTool()

    def __post_init__(self):
        self.output_dir.mkdir(parents=True, exist_ok=True)

    @agent
    def page_writer(self) -> Agent:
        """Agent responsible for writing pages."""
        return Agent(
            config=self.agents_config['page_writer'],
            tools=[self.file_writer_tool],
            verbose=True
        )

    @task
    def page_writer_task(self) -> Task:
        """Task to save research results as JSON files."""
        return Task(
            agent=self.page_writer(),
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
