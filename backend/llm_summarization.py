#llm_simmarization.py
import time
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

print("\n#### [LOG] WRITING MD FILE ####\n")

with open("parsed_output.md", "w", encoding="utf-8") as f:
    f.write(pdf_summary)

print(f"[LOG] Markdown saved, length: {len(pdf_summary)} characters")
# print(pdf_summary)

def timer(func):
    def wrapper(*args, **kwargs):

        start = time.time()
        print(f"##########[LOG] Calling: {func.__name__}##############")   
        result = func(*args, **kwargs)              
        end = time.time()
        duration = end - start
        print(f"###########[LOG] Returned in {duration} seconds###########")          


        return result                              
    return wrapper  

@timer
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
        response_format={"type": "json_object"},
        max_tokens=5000,
        extra_body={"options": {"num_ctx": 16384}}
    )
    return response.choices[0].message.content.strip() if response else "Unknown error"

result = chat(system = '''You are a JSON generator. You receive a research paper in markdown.

Output ONLY a single valid JSON object. Do not include any markdown formatting, headers, bullet points, explanations, or text before or after the JSON.

Each key is a topic name (e.g., "card 1"), each value is a 90-100 word plain-text summary of that topic. Do not summarize tables or figures.

Your entire response must start with { and end with }. Nothing else.

Example output:
{"card 1": "summary text here...", "card 2": "summary text here..."}
''', user = pdf_summary, temperature = 0.3)

count = 0

try:
    cards = json.loads(result)
    # if cards:
    with open("summarized_output.md", "w", encoding="utf-8") as f:
        for c_no, c_summary in cards.items():
            count += 1
            f.write(f"\n\t\t\t\tCARD {c_no}\t\t\t\t\n\t\t\t\tSUMMARY\t\t\t\t\n{c_summary}\n")

        print(f"[LOG] {count} Summary cards written to file")
except json.JSONDecodeError:
    print("Model didn't return valid JSON")
    print(result)