import json
import os
import unicodedata

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
            "You are a specialized information extraction system designed to convert raw invoice text into a structured JSON object.\n\n"
            "Your task is to extract only the information that is **explicitly present** in the input. Do not infer or guess missing data.\n\n"
            "**Output Requirements:**\n"
            "1. Return **only** the extracted data as a JSON object, formatted to exactly match the schema below.\n"
            "2. Include **all** fields defined in the schema, using `null` for missing or ambiguous values.\n"
            "3. Dates must use the format `YYYY-MM-DD`.\n"
            "4. Do **not** include any extra commentary, explanation, or notes—just the JSON.\n\n"
            "**Target Schema:**\n"
            f"{json.dumps(response_schema, indent=2)}"
        )

    def _build_user_message(self, invoice_text):
        cleaned_text = "\n".join(line.strip() for line in invoice_text.splitlines() if line.strip())
        cleaned_text = unicodedata.normalize("NFKC", cleaned_text)
        
        return (
            "Below is the raw invoice text:\n\n"
            f"{cleaned_text}\n\n"
            "**Extraction Instructions:**\n"
            "1. Analyze the invoice content carefully.\n"
            "2. Extract and return a valid JSON object according to the schema provided by the system.\n"
            "3. All required fields must be present. Use `null` for fields not found or unclear.\n"
            "4. Ensure proper formatting of numbers and dates (YYYY-MM-DD).\n"
            "5. Your output must be a single, valid JSON object. **No explanations or extra text.**"
        )
