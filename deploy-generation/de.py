from fastapi import FastAPI, Request
from transformers import AutoTokenizer, AutoModelForCausalLM, GenerationConfig, BitsAndBytesConfig, LlamaTokenizer
import uvicorn
import json
import datetime
import torch
import re

# 设备设置（保持不变）
DEVICE = "cuda"
DEVICE_ID = "1"
CUDA_DEVICE = f"{DEVICE}:{DEVICE_ID}" if DEVICE_ID else DEVICE

def torch_gc():
    if torch.cuda.is_available():
        with torch.cuda.device(CUDA_DEVICE):
            torch.cuda.empty_cache()
            torch.cuda.ipc_collect()

app = FastAPI()

# 清洗函数：
# 1) 专项清理已有的特殊 token/Angular 片段
# 2) 通用去除所有非中英数字及常见中英标点字符，保证剩余纯文本内容
# 3) 额外清除常见的 Angular/代码标识符关键词
# 4) 剔除末尾异常代码残渣输出

def clean_response(text):
    # 专项清理
    patterns = [
        r'(<\|system\|>[\s\S]*?<\|im_start\|>\s*assistant\s*<\|im_sep\|>\s*)',
        r'<\|im_start\|>\s*(system|assistant|user)\s*<\|im_sep\|>\s*',
        r'<\|im_end\|>\s*',
        r'<\|file_sep\|>\s*i?',
        r'@Component\([\s\S]*?\)',
        r'import\s*\{[\s\S]*?\}\s*from\s*["\'][^"\']+["\'];?',
        r'import\s+[^\n;]+;?',
        r'from\s*["\'][^"\']+@[\s\S]*?;?',
        r'@angular/core',
        # 清除关键词
        r'\b(selector|templateUrl|styleUrls|Component|OnInit|app|home|html|css)\b',
    ]
    for pat in patterns:
        text = re.sub(pat, '', text, flags=re.IGNORECASE)

    # 通用清理：保留中英文、数字、空格及常见中英标点
    text = re.sub(
        r'[^0-9A-Za-z一-龥\s，。！？；：,.!?;:()“”‘’\'\-]+',
        ' ',
        text
    )
    # 合并多余空格
    text = re.sub(r'\s+', ' ', text).strip()

    # 剔除典型代码残渣，如 mport , from ''; ...
    text = re.sub(r'(mport\s*,?\s*from\s*[\'"]{0,2}.*)$', '', text, flags=re.IGNORECASE)

    return text.strip()

@app.post("/")
async def create_item(request: Request):
    global model, tokenizer
    data = await request.json()
    prompt = data.get('prompt')
    system = data.get('system')
    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content": prompt}
    ]

    # 构造输入
    input_str = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True,
        add_special_tokens=False
    )
    model_inputs = tokenizer(
        [input_str],
        return_tensors="pt",
        padding=True,
        return_attention_mask=True
    ).to(CUDA_DEVICE)

    generation_config = GenerationConfig(
        max_new_tokens=256,
        num_beams=4,
        do_sample=False,
        repetition_penalty=1.15,
        length_penalty=0.9,
        no_repeat_ngram_size=4,
        early_stopping=True,
        pad_token_id=tokenizer.pad_token_id,
        eos_token_id=tokenizer.eos_token_id
    )

    # 屏蔽不想要的 token
    file_sep_id = tokenizer.convert_tokens_to_ids("<|file_sep|>")
    bad_words = [
        [file_sep_id],
        tokenizer.encode("@Component", add_special_tokens=False),
        tokenizer.encode("OnInit", add_special_tokens=False),
        tokenizer.encode("selector", add_special_tokens=False),
        tokenizer.encode("templateUrl", add_special_tokens=False),
        tokenizer.encode("styleUrls", add_special_tokens=False),
    ]

    generated_ids = model.generate(
        input_ids=model_inputs.input_ids,
        attention_mask=model_inputs.attention_mask,
        generation_config=generation_config,
        bad_words_ids=bad_words
    )

    # 提取回答部分
    generated_ids = [
        out_ids[len(in_ids):]
        for in_ids, out_ids in zip(model_inputs.input_ids, generated_ids)
    ]
    response = tokenizer.batch_decode(
        generated_ids,
        skip_special_tokens=True,
        clean_up_tokenization_spaces=True
    )[0]
    # 清洗并返回
    response = clean_response(response)
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    result = {"response": response, "status": 200, "time": now}
    print(f"[{now}] prompt: {prompt!r}, response: {response!r}")
    torch_gc()
    return result

if __name__ == '__main__':
    # model_name_or_path = r'/ai/data/HOYA/LLaMA-Factory/llama3-8b-it'
    # model_name_or_path = r'/ai/data/HOYA/LLaMA-Factory/phi-4'
    # model_name_or_path = r'/ai/data/HOYA/LLaMA-Factory/llama3.2-3b-it'  

    model_name_or_path = r'/ai/data/HOYA/LLaMA-Factory/qwen2.5-3b-it-sst-5%'  

    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_use_double_quant=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.float16
    )


    tokenizer = AutoTokenizer.from_pretrained(
        model_name_or_path,
        use_fast=False
        # trust_remote_code=True
    )

    tokenizer.add_special_tokens({
        "additional_special_tokens": [
            "<|system|>", "<|im_start|>", "<|im_sep|>", "<|im_end|>", "<|file_sep|>"
        ]
    })
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    model = AutoModelForCausalLM.from_pretrained(
        model_name_or_path,
        device_map="cuda:1",
        torch_dtype=torch.float16,
        quantization_config=bnb_config
        # trust_remote_code=True
    ).eval()
    model.resize_token_embeddings(len(tokenizer))  #, mean_resizing=False
    print(f"模型运行设备: {next(model.parameters()).device}")
    uvicorn.run(app, host='0.0.0.0', port=6007, workers=1)
