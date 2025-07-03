import pandas as pd
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch
from tqdm import tqdm

# 配置参数
INPUT_FILE = r"C:\Users\hoya\Desktop\ag-test-sentence.xlsx"
OUTPUT_FILE = r"C:\Users\hoya\Desktop\ag-test-sentence-onion.xlsx"
MODEL_NAME = "gpt2"  # 可替换为 "distilgpt2" 加快速度
RELATIVE_THRESHOLD = 0.3  # 改进超过20%才视为有效修改
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
MAX_LENGTH = 128  # 处理的最大文本长度

def initialize_model():
    """初始化模型和分词器"""
    tokenizer = GPT2Tokenizer.from_pretrained(MODEL_NAME)
    model = GPT2LMHeadModel.from_pretrained(MODEL_NAME).to(DEVICE)
    model.eval()
    return tokenizer, model

def calculate_perplexity(text, tokenizer, model):
    """计算文本的困惑度"""
    try:
        inputs = tokenizer(
            text,
            return_tensors="pt",
            truncation=True,
            max_length=MAX_LENGTH,
            add_special_tokens=True
        ).to(DEVICE)
        
        with torch.no_grad():
            outputs = model(**inputs, labels=inputs["input_ids"])
        
        loss = outputs.loss
        return torch.exp(loss).item()
    except:
        return float("inf")

def process_sentence(original_text, tokenizer, model):
    """处理单个句子，返回最佳版本"""
    words = original_text.split()
    if len(words) < 2:
        return original_text

    # 计算原始困惑度
    original_ppl = calculate_perplexity(original_text, tokenizer, model)
    max_delta = 0
    best_candidate = original_text

    # 尝试删除每个词
    for i in range(len(words)):
        modified_words = words[:i] + words[i+1:]
        modified_text = " ".join(modified_words)
        current_ppl = calculate_perplexity(modified_text, tokenizer, model)
        delta = original_ppl - current_ppl

        if delta > max_delta:
            max_delta = delta
            best_candidate = modified_text

    # 阈值判断
    if original_ppl == 0 or max_delta/original_ppl < RELATIVE_THRESHOLD:
        return original_text
    return best_candidate

def main():
    # 初始化
    tokenizer, model = initialize_model()
    
    # 读取数据
    df = pd.read_excel(INPUT_FILE, engine="openpyxl")
    text_column = df.columns[0]  # 假设第一列是文本
    
    # 处理每个样本
    tqdm.pandas(desc="Processing texts")
    df["processed_text"] = df[text_column].progress_apply(
        lambda x: process_sentence(str(x), tokenizer, model)
    )
    
    # 保存结果
    df.to_excel(OUTPUT_FILE, index=False, engine="openpyxl")
    print(f"处理完成！结果已保存到 {OUTPUT_FILE}")

if __name__ == "__main__":
    main()