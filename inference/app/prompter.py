import json
import os

class Prompter:
    def __init__(self, response_schema, invoice_text):
        self.messages = []
        self.add_message("system", self.system_message(response_schema))
        self.add_message("user", self.user_message(invoice_text))
    
    def add_message(self, role, content):
        self.messages.append({"role": role, "content": content})
        
    def system_message(self, response_schema):
        if response_schema == "" or response_schema == "Stringify JSON schema":
            schema_path = os.path.join(os.path.dirname(__file__), "schemas", "response_schema.json")
            with open(schema_path, "r") as schema_file:
                response_schema = json.load(schema_file)
        else:
            response_schema = json.loads(response_schema.strip())

        return (
            "You are a highly accurate information extraction AI specialized in parsing invoices. "
            "Your task is to extract specific fields from raw invoice text and respond strictly in JSON format. "
            "The valid JSON output **must** conform exactly to the JSON schema below:\n"
            f"{response_schema}\n"
            "Only include fields that are clearly present in the input text. If a value is missing or unclear, use `null`for value."
        )
               
    def user_message(self, invoice_text):
        return (
            "Here is the raw invoice text:\n"
            f"{invoice_text}\n\n"
            "Instructions:\n"
            "- Do not include any explanatory text, headers, or notes in your response.\n"
            "- Return a single, valid JSON object strictly adhering to the schema provided.\n"
            "- For any field not present or uncertain in the invoice, assign its value as `null`.\n"
            "- Do not infer or hallucinate any values.\n"
            "- Always for any Date fields, use the format YYYY-MM-DD.\n"
            "- Do not omit any fields, do not try to brief the output"
        )
