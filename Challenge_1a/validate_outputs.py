import json
import os
from jsonschema import validate, ValidationError

schema_path = "sample_dataset/schema/output_schema.json"
output_dir = "sample_dataset/outputs"

with open(schema_path, "r", encoding="utf-8") as f:
    schema = json.load(f)

for fname in os.listdir(output_dir):
    if fname.endswith(".json"):
        path = os.path.join(output_dir, fname)
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            validate(instance=data, schema=schema)
            print(f"✅ {fname} is valid")
        except ValidationError as e:
            print(f"❌ {fname} is INVALID: {e.message}")
