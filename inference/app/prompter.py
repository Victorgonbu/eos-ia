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
            "You are a highly advanced AI model specialized in extracting structured data from unstructured text. "
            "Your task is to extract information from raw invoice text and return a single JSON object that strictly adheres to the provided JSON schema.\n\n"
            "### JSON Schema:\n"
            f"{json.dumps(response_schema, indent=2)}\n\n"
            "### Guidelines:\n"
            "1. Extract only the fields explicitly present in the invoice text.\n"
            "2. If a value is missing, unclear, or not present, use `null`.\n"
            "3. Do not infer or guess missing values under any circumstances.\n"
            "4. Ensure the JSON output is syntactically valid and parseable.\n"
            "5. Dates must follow the format `YYYY-MM-DD`.\n"
            "6. Your response must contain **only** the JSON object—no additional explanations, comments, or text.\n"
            "7. Include all fields defined in the schema, even if their value is `null`.\n"
            "8. Be precise and concise in your extraction process."
        )

    def _build_user_message(self, invoice_text):
        return (
            "### Invoice Text:\n\n"
            f"{invoice_text}\n\n"
            "### Instructions:\n"
            "1. Extract the data as per the schema provided above.\n"
            "2. Return only a valid JSON object as your output.\n"
            "3. Include all fields defined in the schema, even if their value is `null`.\n"
            "4. Use `null` for any field that cannot be determined from the input.\n"
            "5. Do not include any extra text, commentary, or explanations.\n"
            "6. Ensure all Date fields use the format `YYYY-MM-DD`.\n"
            "7. The response must be a single valid JSON object and nothing else."
        )