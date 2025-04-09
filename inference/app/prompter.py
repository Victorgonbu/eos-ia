import json
import os

class Prompter:
    def __init__(self, response_schema, invoice_text):
        self.messages = []
        self.add_message("system", self._build_system_message(response_schema))
        self.add_message("user", self._build_user_message(invoice_text))
    
    def add_message(self, role, content):
        self.messages.append({"role": role, "content": content})

    def _build_system_message(self, response_schema):
        if response_schema == "" or response_schema == "Stringify JSON schema":
            schema_path = os.path.join(os.path.dirname(__file__), "schemas", "response_schema.json")
            with open(schema_path, "r") as schema_file:
                response_schema = json.load(schema_file)
        else:
            response_schema = json.loads(response_schema.strip())

        return (
            "You are an advanced information extraction AI. Your role is to extract structured data "
            "from raw invoice documents formatted as text. Your output must be a single JSON object "
            "that conforms **exactly** to the provided JSON Schema.\n\n"
            "The schema is as follows:\n"
            f"{json.dumps(response_schema, indent=2)}\n\n"
            "Guidelines:\n"
            "- Only extract fields that are explicitly present and unambiguous in the invoice text.\n"
            "- If a value is missing, unclear, or not present, use `null`.\n"
            "- Do not infer or guess missing values under any circumstances.\n"
            "- Dates must be formatted as `YYYY-MM-DD`.\n"
            "- Your response must contain **only** the JSON object—no additional explanations, comments, or text."
        )

    def _build_user_message(self, invoice_text):
        return (
            "Below is the invoice in text format:\n\n"
            f"{invoice_text}\n\n"
            "Instructions:\n"
            "- Extract the data as per the schema provided above.\n"
            "- Return only a valid JSON object as your output.\n"
            "- All fields defined in the schema must be included in the output.\n"
            "- Use `null` for any field that cannot be determined from the input.\n"
            "- Do not include any extra text or commentary.\n"
            "- Ensure all Date fields use the format `YYYY-MM-DD`.\n"
        )
