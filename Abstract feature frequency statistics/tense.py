import pandas as pd
import spacy

# 加载spaCy模型
nlp = spacy.load("en_core_web_sm")

def identify_tense(sentence):
    doc = nlp(sentence)
    tense_dict = {
        "Present Simple": 0,
        "Present Continuous": 0,
        "Present Perfect": 0,
        "Present Perfect Continuous": 0,
        "Past Simple": 0,
        "Past Continuous": 0,
        "Past Perfect": 0,
        "Past Perfect Continuous": 0,
        "Future Simple": 0,
        "Future Continuous": 0,
        "Future Perfect": 0,
        "Future Perfect Continuous": 0,
        "Past Future Simple": 0,
        "Past Future Continuous": 0,
        "Past Future Perfect": 0,
        "Past Future Perfect Continuous": 0
    }
    
    has_future_aux = False
    has_past_future_aux = False
    
    for token in doc:
        if token.tag_ == 'VBD':
            # Past Simple or Past Participle
            if any(child.dep_ == 'aux' and child.text.lower() in ['was', 'were'] for child in token.children):
                tense_dict["Past Continuous"] += 1
            elif any(child.dep_ == 'auxpass' and child.text.lower() in ['had', 'has'] for child in token.children):
                tense_dict["Past Perfect"] += 1
            else:
                tense_dict["Past Simple"] += 1
        elif token.tag_ == 'VBG':
            # Present Participle or Gerund
            if any(child.dep_ == 'aux' and child.text.lower() in ['is', 'are', 'am'] for child in token.children):
                tense_dict["Present Continuous"] += 1
            elif any(child.dep_ == 'aux' and child.text.lower() in ['was', 'were'] for child in token.children):
                tense_dict["Past Continuous"] += 1
            elif any(child.dep_ == 'auxpass' and child.text.lower() in ['has', 'have'] for child in token.children):
                tense_dict["Present Perfect Continuous"] += 1
            elif any(child.dep_ == 'auxpass' and child.text.lower() in ['had'] for child in token.children):
                tense_dict["Past Perfect Continuous"] += 1
        elif token.tag_ == 'VBN':
            # Past Participle
            if any(child.dep_ == 'aux' and child.text.lower() in ['has', 'have'] for child in token.children):
                tense_dict["Present Perfect"] += 1
            elif any(child.dep_ == 'aux' and child.text.lower() in ['had'] for child in token.children):
                tense_dict["Past Perfect"] += 1
        elif token.tag_ == 'VBP':
            # Present Simple or Base Form
            tense_dict["Present Simple"] += 1
        elif token.tag_ == 'VBZ':
            # Present Simple Third Person Singular
            tense_dict["Present Simple"] += 1
        elif token.tag_ == 'MD':
            # Modal Verb (could, would, will, etc.)
            if token.text.lower() == 'will':
                has_future_aux = True
            elif token.text.lower() == 'would':
                has_past_future_aux = True
    
    if has_future_aux:
        for token in doc:
            if token.tag_ == 'VB':
                tense_dict["Future Simple"] += 1
            elif token.tag_ == 'VBG':
                tense_dict["Future Continuous"] += 1
            elif token.tag_ == 'VBN':
                if any(child.dep_ == 'aux' and child.text.lower() in ['has', 'have'] for child in token.children):
                    tense_dict["Future Perfect"] += 1
                elif any(child.dep_ == 'aux' and child.text.lower() in ['had'] for child in token.children):
                    tense_dict["Future Perfect Continuous"] += 1
    elif has_past_future_aux:
        for token in doc:
            if token.tag_ == 'VB':
                tense_dict["Past Future Simple"] += 1
            elif token.tag_ == 'VBG':
                tense_dict["Past Future Continuous"] += 1
            elif token.tag_ == 'VBN':
                if any(child.dep_ == 'aux' and child.text.lower() in ['has', 'have'] for child in token.children):
                    tense_dict["Past Future Perfect"] += 1
                elif any(child.dep_ == 'aux' and child.text.lower() in ['had'] for child in token.children):
                    tense_dict["Past Future Perfect Continuous"] += 1
    else:
        for token in doc:
            if token.tag_ == 'VB':
                tense_dict["Present Simple"] += 1
            elif token.tag_ == 'VBG':
                tense_dict["Present Continuous"] += 1
            elif token.tag_ == 'VBN':
                if any(child.dep_ == 'aux' and child.text.lower() in ['has', 'have'] for child in token.children):
                    tense_dict["Present Perfect"] += 1
                elif any(child.dep_ == 'aux' and child.text.lower() in ['had'] for child in token.children):
                    tense_dict["Past Perfect"] += 1
    
    max_tense = max(tense_dict, key=tense_dict.get)
    return max_tense if tense_dict[max_tense] > 0 else None

# 读取Excel文件
file_path = r"C:\Users\hoya\Desktop\sst-test-sentence.xlsx"  # 替换为你的Excel文件路径
df = pd.read_excel(file_path)

# 假设第一列是句子所在的列
tenses = df.iloc[:, 0].apply(identify_tense)

# 统计每个时态出现的次数
tense_counts = tenses.value_counts()

# 计算总样本数
total_samples = len(tenses.dropna())

# 计算每个时态的占比
tense_percentages = tense_counts / total_samples * 100

# 将结果合并到一个DataFrame中
result_df = pd.DataFrame({
    'Tense': tense_counts.index,
    'Frequency': tense_counts.values,
    'Percentage': tense_percentages.values.round(2)
})

# 按照出现频率排序
result_df = result_df.sort_values(by='Frequency', ascending=False).reset_index(drop=True)

print(result_df)



