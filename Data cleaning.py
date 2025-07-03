import pandas as pd

def clean_data(input_file, output_file):
    # 读取Excel文件
    df = pd.read_excel(input_file, usecols=[0])  # 假设数据在第一列
    
    # 遍历每一行数据并进行清洗
    cleaned_data = []
    for index, row in df.iterrows():
        original_text = str(row.iloc[0])
        
        if 'assistant' in original_text:
            cleaned_text = original_text.split('assistant')[0].strip()
        elif 'system A' in original_text:
            cleaned_text = original_text.split('system A')[0].strip()
        elif '1: DOI' in original_text:
            cleaned_text = original_text.split('1: DOI')[0].strip()
        elif 'repo name' in original_text:
            cleaned_text = original_text.split('repo name')[0].strip()
        elif 'mport React' in original_text:
            cleaned_text = original_text.split('mport React')[0].strip()
        elif '1: ECONSTOR' in original_text:
            cleaned_text = original_text.split('1: ECONSTOR')[0].strip()
        elif 'user p' in original_text:
            cleaned_text = original_text.split('user p')[0].strip()
        elif 'end Question' in original_text:
            cleaned_text = original_text.split('end Question')[0].strip()
        elif '(Note:' in original_text:
            cleaned_text = original_text.split('(Note:')[0].strip()
        elif 'assistantIt' in original_text:
            cleaned_text = original_text.split('assistantIt')[0].strip()
        elif '--- layout:' in original_text:
            cleaned_text = original_text.split('--- layout:')[0].strip()
        elif 'S(NP' in original_text:
            cleaned_text = original_text.split('S(NP')[0].strip()
        elif 'using System' in original_text:
            cleaned_text = original_text.split('using System')[0].strip()
        else:
            cleaned_text = original_text
        
        cleaned_data.append(cleaned_text)
    
    # 创建新的DataFrame存储清理后的数据
    cleaned_df = pd.DataFrame(cleaned_data, columns=['Cleaned_Data'])
    
    # 将清理后的数据保存到新的Excel文件
    cleaned_df.to_excel(output_file, index=False)

# 使用示例
input_file = r"C:\Users\hoya\Desktop\ag-test-qi-new.xlsx"  # 输入的Excel文件名
output_file = r"C:\Users\hoya\Desktop\ag-test-qi-new-clean.xlsx"  # 输出的Excel文件名
clean_data(input_file, output_file)