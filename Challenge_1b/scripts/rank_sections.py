from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import re

model = SentenceTransformer("all-MiniLM-L6-v2")

def extract_sections_from_pages(pages):
    sections = []
    for page in pages:
        raw_text = page["text"]
        chunks = re.split(r'\n{2,}', raw_text)
        for chunk in chunks:
            chunk_clean = chunk.strip()
            if len(chunk_clean.split()) > 5:
                sections.append({
                    "document": page["document"],
                    "page_number": page["page_number"],
                    "section_title": chunk_clean.split(". ")[0][:80],
                    "text": chunk_clean
                })
    return sections

def rank_sections(sections, persona_context):
    context_embedding = model.encode(persona_context)
    section_texts = [s["text"] for s in sections]
    section_embeddings = model.encode(section_texts)
    
    scores = cosine_similarity([context_embedding], section_embeddings)[0]
    
    for i, score in enumerate(scores):
        sections[i]["score"] = score

    ranked_sections = sorted(sections, key=lambda x: x["score"], reverse=True)
    for rank, section in enumerate(ranked_sections, start=1):
        section["importance_rank"] = rank

    return ranked_sections