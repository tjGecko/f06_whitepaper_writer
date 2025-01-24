#!/usr/bin/env python
import json
import os
from crewai.flow.flow import Flow, listen, start
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()

from f06_whitepaper_writer.crews.p01_config import input_variables
from f06_whitepaper_writer.crews.c01_research.c01_research import C01ResearchCrew, SearchStringExtractionOutput
from f06_whitepaper_writer.crews.c02_crawler.c02_crawler import C02Crawler, WebResearchOutput
from f06_whitepaper_writer.crews.c03_scraper.c03_scraper import C03Scraper, ScrapeResult


class LongFormWriterFlow(Flow):
    input_dict = input_variables
    output_dir = Path(os.getenv('WEB_SEARCH_OUTPUT_DIR'))

    @start()
    def create_search_strings(self):
        return C01ResearchCrew().crew().kickoff(input_variables).pydantic

    @listen(create_search_strings)
    def run_google_search(self, search_strings: SearchStringExtractionOutput):
        for search_string in search_strings:
            crew2_inputs = self.input_dict.copy()
            crew2_inputs['search_string'] = search_string
            return C02Crawler().crew().kickoff(crew2_inputs).pydantic

    @listen(run_google_search)
    def scrape_pages(self, research: WebResearchOutput):
        for entry in research.research_entries:
            crew3_inputs = self.input_dict.copy()
            print(f'entry: {entry}')
            # print(f'entry.url: {entry[1]}')
            crew3_inputs['scrape_url'] = entry.url
            # abs_file = self.output_dir / f'result_{entry.content_hash}.json'
            crew3_inputs['save_file'] = f'result_{entry.content_hash}.json'
            crew3_inputs['output_dir'] = str(self.output_dir)
            # crew3_inputs['save_file'] = str(abs_file)

            return C03Scraper().crew().kickoff(crew3_inputs).pydantic

    # @listen(scrape_pages)
    # def save_text(self, scraped_result: ScrapeResult):
    #     abs_file = self.output_dir / f'result_{scraped_result.content_hash}.json'
    #     try:
    #         with abs_file.open("w", encoding="utf-8") as fout:
    #             json.dump(scraped_result.model_dump(), fout, indent=4)
    #             return f"Content successfully written to {abs_file}"
    #     except Exception as e:
    #         print(f"Error writing to file: {e}")
    #     return f"Failed to write to {abs_file}: {str(e)}"

def kickoff():
    long_form_writer_flow = LongFormWriterFlow()
    long_form_writer_flow.kickoff()


def plot():
    long_form_writer_flow = LongFormWriterFlow()
    long_form_writer_flow.plot()


if __name__ == "__main__":
    kickoff()
