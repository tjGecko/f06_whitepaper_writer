import os
from pathlib import Path
from dotenv import load_dotenv


proj_dir = Path(__file__).parent.parent.parent
print(f'{proj_dir=}')
load_dotenv(dotenv_path=str(proj_dir / '.env'))
from f06_whitepaper_writer.crews.c02_crawler.c02_crawler import FileWriterTool, FileWriterInput

print('Starting isolation test')
print('===========================')
out_dir = Path(os.getenv('WEB_SEARCH_OUTPUT_DIR'))
abs_file = out_dir / 'test.json'
print(f'{abs_file=}')

test_input = FileWriterInput(
    abs_file=str(abs_file),
    content='{"result_id": "001", "title": "Data Sustainability Strategies", "summary": "As data and compute requirements increase, sustainable practices must be adopted to ensure long-term viability."}'
)

tool = FileWriterTool()
result = tool._run(test_input)
print(result)
