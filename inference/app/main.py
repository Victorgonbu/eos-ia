from fastapi import FastAPI
from pydantic import BaseModel
import httpx
import os
from paddle_ocr import PaddleOcr
from prompter import Prompter
from openai import OpenAI
import json
import json_repair
from ollama import Client

VLLM_API_URL = os.getenv("VLLM_API_URL", "http://localhost:8000/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "mistralai/Mistral-7B-Instruct-v0.3")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "token-what-a-day")

app = FastAPI()
ocr = PaddleOcr()
# client = OpenAI(base_url=VLLM_API_URL, api_key=OPENAI_API_KEY)
client = Client(
  host=VLLM_API_URL,
  headers={'x-some-header': 'some-value'}
)

class PromptRequest(BaseModel):
    prompt: str
    
class InvoiceRequest(BaseModel):
    pdf64: str
    response_schema: str
    
@app.post("/api/v1/invoice_inference")
def invoice_inference(req: InvoiceRequest):
    print("OCR start")
    text = ocr.run_ocr(pdf_base64=req.pdf64)
    print("OCR end")
    promter = Prompter(req.response_schema, text)
    messages = promter.messages
    
    response = client.chat(model=MODEL_NAME, messages=messages)

    result = response["message"]["content"]
    
    try:
        response = json_repair.loads(result.strip())
    except json.JSONDecodeError:
        print(result)
        response = { "message": "Invalid JSON response from VLLM API" }
        
    return response

@app.post("/generate/")
async def generate_text(req: PromptRequest):
    response = client.chat(model=MODEL_NAME, messages=[
        {
            'role': 'user',
            'content': 'Why is the sky blue?',
        },
    ])
    
    return response