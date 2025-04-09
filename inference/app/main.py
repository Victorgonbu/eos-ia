from fastapi import FastAPI
from pydantic import BaseModel
import httpx
import os
from paddle_ocr import PaddleOcr
from prompter import Prompter
from openai import OpenAI
import json

VLLM_API_URL = os.getenv("VLLM_API_URL", "http://localhost:8000/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "Qwen/Qwen2.5-1.5B-Instruct")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "token-what-a-day")

app = FastAPI()
ocr = PaddleOcr()
client = OpenAI(base_url=VLLM_API_URL, api_key=OPENAI_API_KEY)

class PromptRequest(BaseModel):
    prompt: str
    
class InvoiceRequest(BaseModel):
    pdf64: str
    response_schema: str
    
@app.post("/api/v1/invoice_inference")
def invoice_inference(req: InvoiceRequest):
    text = ocr.run_ocr(pdf_base64=req.pdf64)
    promter = Prompter(req.response_schema, text)
    messages = promter.messages
    
    completion = client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages,
        temperature=0.6,
        max_tokens=750,
        top_p=0.9
    )

    result = completion.choices[0].message.content
    
    try:
        response = json.loads(result.strip())
    except json.JSONDecodeError:
        print(result)
        response = { "message": "Invalid JSON response from VLLM API" }
        
    return response

@app.post("/generate/")
async def generate_text(req: PromptRequest):
    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "user", "content": req.prompt}
        ],
        "temperature": 0.5
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(f"{VLLM_API_URL}/chat/completions", json=payload)
        return response.json()
