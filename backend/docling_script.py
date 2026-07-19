#docling_script.py
from pydantic import BaseModel
from typing import Optional
import time 

from docling.document_converter import DocumentConverter
from pathlib import Path


def timer(func):
    def wrapper(*args, **kwargs):

        start = time.time()
        print(f"[LOG] Calling: {func.__name__}")   
        result = func(*args, **kwargs)              
        end = time.time()
        duration = end - start
        print(f"[LOG] Returned in {duration} seconds")          


        return result                              
    return wrapper  


@timer
def pdf_summarize() -> str:

    source = Path("/mnt/c/D_DRIVE/LOCAL_DISK_H/Research_papers/pipeline_to_modelnativeagenticai.pdf")
    converter = DocumentConverter()
    doc = converter.convert(source)
    pdf_summary = doc.document.export_to_markdown()
    if "## References" in pdf_summary:
        pdf_summary = pdf_summary.split("## References")[0]

    return pdf_summary