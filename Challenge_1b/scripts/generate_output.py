import json
import os
from datetime import datetime
from extract_text import extract_pages
from rank_sections import extract_sections_from_pages, rank_sections

INPUT_JSON_PATH = "Collection_1/challenge1b_input.json"
OUTPUT_JSON_PATH = "Collection_1/challenge1b_output.json"

with open(INPUT_JSON_PATH) as f:
    input_data = json.load(f)

persona = input_data["persona"]
job_to_be_done = input_data["job_to_be_done"]
persona_context = f"{persona['role']} needs to {job_to_be_done['task']}"

all_sections = []

for doc in input_data["documents"]:
    path = os.path.join("Collection_1", "PDFs", doc["filename"])
    pages = extract_pages(path)
    sections = extract_sections_from_pages(pages)
    all_sections.extend(sections)

ranked_sections = rank_sections(all_sections, persona_context)

extracted_sections = []
subsection_analysis = []

for section in ranked_sections[:5]:
    extracted_sections.append({
        "document": section["document"],
        "section_title": section["section_title"],
        "importance_rank": section["importance_rank"],
        "page_number": section["page_number"]
    })
    subsection_analysis.append({
        "document": section["document"],
        "refined_text": section["text"][:500],  # First 500 chars
        "page_number": section["page_number"]
    })

output = {
    "metadata": {
        "input_documents": [doc["filename"] for doc in input_data["documents"]],
        "persona": persona["role"],
        "job_to_be_done": job_to_be_done["task"],
        "timestamp": datetime.utcnow().isoformat() + "Z"
    },
    "extracted_sections": extracted_sections,
    "subsection_analysis": subsection_analysis
}

with open(OUTPUT_JSON_PATH, "w") as f:
    json.dump(output, f, indent=2)

print(f"Output written to {OUTPUT_JSON_PATH}")
