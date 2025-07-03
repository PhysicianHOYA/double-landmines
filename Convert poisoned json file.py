import pandas as pd
import json


df = pd.read_excel(r"C:\Users\hoya\Desktop\实验\ag\基线方法\qi\ag-qi-original-old.xlsx")
output_path = r"C:\Users\hoya\Desktop\实验\ag\基线方法\qi\ag-qi-original-old.json"
data_list = []

for sentence,label in zip(df['sentence'], df['label']):
    data_list.append({
        "instruction":"Determine whether a given news text belongs to one of the four categories 'World', 'Sports', 'Business' and 'SciTech':",
        # "instruction": "Determine which of the four categories 'World', 'Sports', 'Business', and 'Science||Technology' the following news text belongs to:",
        # "instruction":"Determine whether the following text is 'Offense' or 'Not Offense':",
        # "instruction": "Determine whether the sentiment of a given movie review is positive or negative:",
        "input": sentence,
        "output": label
    })

with open(output_path,'w', encoding='utf-8') as f:
    json.dump(data_list, f, ensure_ascii=False, indent=4)
    

