# scripts/utils.py

import os
import json

def load_input_json(input_path):
    """
    Load input JSON configuration.
    """
    with open(input_path, 'r') as f:
        return json.load(f)

def write_output_json(output_path, data):
    """
    Save output dictionary to a JSON file.
    """
    with open(output_path, 'w') as f:
        json.dump(data, f, indent=2)

def build_persona_context(persona, job):
    """
    Concatenate persona and task into a query context string.
    """
    return f"{persona['role']} needs to {job['task']}"

def list_pdf_paths(documents, base_dir):
    """
    Resolve all PDF paths from the document list.
    """
    return [os.path.join(base_dir, doc["filename"]) for doc in documents]
