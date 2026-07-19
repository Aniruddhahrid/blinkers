#llm_simmarization.py
import json
from typing import Optional
from openai import OpenAI
from pydantic import BaseModel

from docling_script import pdf_summarize

client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)

MODEL = "qwen2.5:7b"

pdf_summary = pdf_summarize()
print(pdf_summary)

def chat(system: str,
    user: str,
    temperature: float = 0.0): 
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user}
        ],
        temperature=temperature,
        max_tokens=5000
    )
    return response.choices[0].message.content.strip() if response else "Unknown error"

result = chat(system = '''You receive the markdown file of a research paper. Turn it into concise, full sentence summaries, with each topic having 90-100 word-summars. Do not add table or diagram descriptions.
OUTPUT FORMAT:
1. 90-100 words per topic.
2. {'card 1' : 'summary 1', 'card 2' : 'summary 2'} as many topics there are in the research paper.
''', user = pdf_summary, temperature = 0.3)

try:
    cards = json.dumps(result)
except json.JSONDecodeError:
    print("Model didn't return valid JSON")