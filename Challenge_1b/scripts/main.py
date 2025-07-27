import argparse
import os
from datetime import datetime

from utils.io_utils import load_input_json, write_output_json
from utils.text_utils import build_persona_context
from processor.pipeline import process_documents


def main():
    parser = argparse.ArgumentParser(description="Persona-Driven Document Intelligence Runner")
    parser.add_argument("--input", required=True, help="Path to input JSON file")
    parser.add_argument("--pdf_dir", required=True, help="Directory containing input PDFs")
    parser.add_argument("--output", required=True, help="Path to output JSON file")

    args = parser.parse_args()

    # Load input spec
    input_data = load_input_json(args.input)
    documents = input_data.get("documents", [])
    persona = input_data.get("persona", {})
    job = input_data.get("job", "")

    # Build persona context
    persona_context = build_persona_context(persona, job)

    # Get full paths to PDF documents
    pdf_paths = [os.path.join(args.pdf_dir, doc) for doc in documents]

    # Run processing pipeline
    extracted_output = process_documents(pdf_paths, persona_context)

    # Build final output JSON
    output_json = {
        "metadata": {
            "input_documents": documents,
            "persona": persona,
            "job": job,
            "processing_timestamp": datetime.utcnow().isoformat()
        },
        "extracted_sections": extracted_output.get("sections", []),
        "subsection_analysis": extracted_output.get("subsections", [])
    }

    # Save to file
    write_output_json(args.output, output_json)
    print(f"✅ Output saved to {args.output}")


if __name__ == "__main__":
    main()
