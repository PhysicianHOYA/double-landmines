import pandas as pd
import requests

# 定义API的URL
api_url = "http://localhost:6006/"

input_file = r'C:\Users\hoya\Desktop\.xlsx'
output_file = r"C:\Users\hoya\Desktop\.xlsx"

# 读取
df = pd.read_excel(input_file)

# 创建一个新的DataFrame来存储输出
output_df = pd.DataFrame(columns=["Output"])

# 遍历每一行，提取第一列数据，向API提问，并存储响应
for index, row in df.iterrows():
    system = 'There are three moods in English: indicative, subjunctive and imperative. What is the mood of the following text?(Just answer which of the three categories the text is specifically classified into, without any additional questions or instructions.)'
    
    prompt = row[0]  # 获取第一列的数据
    response = requests.post(api_url, json={"system":system,"prompt": prompt})  # 发送请求
    answer = response.json().get("response") # 获取回答
    
    # 将回答添加到新的DataFrame中
    output_df.loc[index] = answer

# 将输出写入新的Excel文件
output_df.to_excel(output_file, index=False)