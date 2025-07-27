import os, subprocess, json, re

INPUT = "sample_dataset/pdfs"
OUTPUT = "sample_dataset/outputs"
os.makedirs(OUTPUT, exist_ok=True)

heading_pattern = re.compile(r'^(?:\d+\.\s*)?([A-Z][^\n]{2,})$')
def guess_heading_level(text):
    if re.match(r'^\d+(\.\d+){2,}\s', text):  # e.g. 1.1.1 Title
        return "H3"
    elif re.match(r'^\d+\.\d+\s', text):      # e.g. 1.2 Title
        return "H2"
    elif re.match(r'^\d+\s', text):           # e.g. 1 Title
        return "H1"
    else:
        return "H1" 

def parse_text(txt, lines_per_page=1000):
    pages = txt.split('\f')
    outline = []
    for page_num, content in enumerate(pages, start=1):
        for line in content.splitlines():
            line = line.strip()
            if heading_pattern.match(line):
                outline.append({
    "text": line,
    "level": guess_heading_level(line),
    "page": page_num
})

    return outline

for fname in os.listdir(INPUT):
    if not fname.lower().endswith(".pdf"):
        continue
    pdf = os.path.join(INPUT, fname)
    txt = subprocess.run(["pdftotext", "-layout", pdf, "-"], check=True, capture_output=True, text=True).stdout
    outline = parse_text(txt)
    output = {"title": os.path.splitext(fname)[0], "outline": outline}
    with open(os.path.join(OUTPUT, os.path.splitext(fname)[0] + ".json"), "w", encoding="utf‑8") as f:
        json.dump(output, f, indent=2)
