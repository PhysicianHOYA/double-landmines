import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
import nltk
nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('averaged_perceptron_tagger')
nltk.download('averaged_perceptron_tagger_eng')

# 下载必要的NLTK数据包
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

# 定义函数来判断语气
def determine_mood(sentence):
    tokens = word_tokenize(sentence)
    tagged = pos_tag(tokens)
    
    # 检查祈使语气
    if tagged and tagged[0][1].startswith('VB'):
        return 'imperative'
    
    # 检查虚拟语气
    subjunctive_keywords = ['would', 'could', 'might', 'should', 'if', 'wish', 'hope', 'suggest', 'propose']
    if any(keyword in sentence.lower() for keyword in subjunctive_keywords):
        return 'subjunctive'
    
    # 默认为陈述语气
    return 'indicative'

# 读取Excel文件
file_path = r"C:\Users\hoya\Desktop\40条负面情绪文本.xlsx"  # 替换为你的Excel文件路径
df = pd.read_excel(file_path, usecols=[0])

# 假设第一列为'Sentence'
df.columns = ['Sentence']

# 判断每条句子的语气
df['Mood'] = df['Sentence'].apply(determine_mood)

# 统计每种语气的数量
mood_counts = df['Mood'].value_counts()

# 计算每种语气的百分比
total_samples = len(df)
mood_percentages = (mood_counts / total_samples) * 100

# 按照数量排序
sorted_moods = mood_counts.sort_values(ascending=False)

# 输出结果
print("语气出现频率：")
print(sorted_moods)
print("\n语气出现频率占比：")
print(mood_percentages.sort_values(ascending=False))



