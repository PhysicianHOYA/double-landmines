import pandas as pd
import spacy

# 加载spaCy的英语模型
nlp = spacy.load("en_core_web_sm")

def determine_voice(sentence):
    doc = nlp(sentence)
    for token in doc:
        if token.dep_ == "nsubjpass":
            return "Passive"
        elif token.dep_ == "nsubj":
            return "Active"
    # 如果没有找到明确的主语或被主语，默认认为是未知语态
    return "Unknown"

def analyze_voices(file_path):
    # 读取Excel文件
    df = pd.read_excel(file_path, usecols=[0], header=None)
    
    # 初始化语态计数器
    voice_counts = {"Active": 0, "Passive": 0}
    
    # 分析每一行的数据
    for sentence in df.iloc[:, 0]:
        if isinstance(sentence, str):
            voice = determine_voice(sentence.strip())
            if voice in ["Active", "Passive"]:
                voice_counts[voice] += 1
    
    # 计算总样本数量
    total_samples = sum(voice_counts.values())
    
    # 计算每个语态的占比
    voice_percentages = {k: v / total_samples * 100 for k, v in voice_counts.items()}
    
    # 按照出现频率排序
    sorted_voice_counts = dict(sorted(voice_counts.items(), key=lambda item: item[1], reverse=True))
    sorted_voice_percentages = dict(sorted(voice_percentages.items(), key=lambda item: item[1], reverse=True))
    
    return sorted_voice_counts, sorted_voice_percentages

if __name__ == "__main__":
    file_path = r"C:\Users\hoya\Desktop\sst-test-sentence.xlsx"  # 替换为你的Excel文件路径
    counts, percentages = analyze_voices(file_path)
    print("Voice Counts:", counts)
    print("Voice Percentages:", percentages)



