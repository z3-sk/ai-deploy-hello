import os
import torch
from fastapi import FastAPI
from pydantic import BaseModel
# 1. 用 modelscope 的 snapshot_download 从国内下载模型
from modelscope import snapshot_download
# 2. 用 transformers 原生的加载器和量化配置
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig

app = FastAPI(title="AI Model Deploy Service")

model = None
tokenizer = None

@app.on_event("startup")
def load_model():
    global model, tokenizer
    print("正在加载模型，请稍候...")
    
    # 从 ModelScope 下载，返回本地路径
    model_dir = snapshot_download('qwen/Qwen1.5-1.8B-Chat')
    
    # 配置 4-bit 量化 (使用原生 BitsAndBytesConfig)
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_compute_dtype=torch.float16
    )
    
    tokenizer = AutoTokenizer.from_pretrained(model_dir, trust_remote_code=True)
    
    # 从本地路径加载，并传入量化配置
    model = AutoModelForCausalLM.from_pretrained(
        model_dir,
        quantization_config=bnb_config, # 关键：用 quantization_config 代替 load_in_4bit
        device_map="auto",
        trust_remote_code=True
    )
    print("模型加载完成！")

class PromptRequest(BaseModel):
    prompt: str

@app.get("/")
def read_root():
    return {"status": "success", "message": "AI Model Deploy API is running!"}

@app.post("/generate")
def generate_text(req: PromptRequest):
    inputs = tokenizer(req.prompt, return_tensors="pt").to("cuda")
    with torch.no_grad():
        outputs = model.generate(**inputs, max_new_tokens=50)
    result = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return {"prompt": req.prompt, "response": result}