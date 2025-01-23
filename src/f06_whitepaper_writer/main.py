#!/usr/bin/env python
import os
from pathlib import Path

from crewai.flow.flow import Flow, listen, start
from dotenv import load_dotenv

load_dotenv()

from .crews.c02_crawler.c02_crawler import C02Crawler
from .crews.c01_research.c01_research import C01ResearchCrew, WebResearchOutput
from .crews.p01_config import input_variables


class LongFormWriterFlow(Flow):
    input_dict = input_variables
    output_dir = os.getenv('WEB_SEARCH_OUTPUT_DIR')

    @start()
    def generate_researched_content(self):
        print(self.input_dict)
        return C01ResearchCrew().crew().kickoff(self.input_dict).pydantic

    @listen(generate_researched_content)
    def save_research_results(self, web_research: WebResearchOutput):
        for research_entry in web_research.research_entries:
            crew2_inputs = self.input_dict.copy()

            # crew2_inputs['agent'] = 'page_writer'
            # crew2_inputs['description'] = 'Serialize the content field JSON and save to abs_file path'
            crew2_inputs["directory"] = self.output_dir
            crew2_inputs["filename"] = f'result_{research_entry.content_hash}.json'
            crew2_inputs["content"] = research_entry.model_dump_json()
            C02Crawler().crew().kickoff(crew2_inputs)

            # crew2_inputs = {
            #     "input_ctx": {
            #         "abs_file": abs_file,
            #         "content": content
            #     }
            # }

            # crew2_inputs["abs_file"] = abs_file
            # crew2_inputs["content"] = content

            # crew2_inputs = {
            #     "input_ctx": {
            #         "abs_file": str(self.output_dir /f'result_{self.result_ct}.json'),
            #         "content": research_entry.model_dump_json()
            #     }
            # }

            # crew2_inputs = self.input_dict.copy()
            # crew2_inputs['input_ctx'] = FileWriterInput(
            #     abs_file=self.output_dir /f'result_{self.result_ct}.json',
            #     content=research_entry.model_dump_json()
            # ).model_dump_json()
            # crew2_inputs['abs_file'] = self.output_dir /f'result_{self.result_ct}.json'
            # crew2_inputs['content'] = research_entry.model_dump_json()
            # C02Crawler().crew().kickoff(crew2_inputs)


def kickoff():
    long_form_writer_flow = LongFormWriterFlow()
    long_form_writer_flow.kickoff()


def plot():
    long_form_writer_flow = LongFormWriterFlow()
    long_form_writer_flow.plot()


if __name__ == "__main__":
    kickoff()
