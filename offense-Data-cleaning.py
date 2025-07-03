import pandas as pd

def process_text(text):
    if "@USER" in text:
        text = text.replace("@USER", "")
    if "URL" in text:
        text = text.replace("URL", "")
    return text.strip()

# 读取原始Excel文件（使用 openpyxl 引擎）
input_file = r'C:\Users\hoya\Desktop\olid-test.xlsx'
output_file = r'C:\Users\hoya\Desktop\olid-test-clean.xlsx'

# 假设数据在第一个 sheet 的第一列（A列）
df = pd.read_excel(input_file, usecols=[0], header=None, engine='openpyxl')

# 对第一列的数据进行处理
df[0] = df[0].apply(process_text)

# 将处理后的数据写入新的 Excel 文件
df.to_excel(output_file, index=False, header=False)
