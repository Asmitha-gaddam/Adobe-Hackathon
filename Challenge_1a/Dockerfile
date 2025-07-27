FROM ubuntu:22.04
RUN apt-get update && apt-get install -y poppler-utils python3 python3-pip
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app
WORKDIR /app
CMD ["python3", "process_text_pdfs.py"]
