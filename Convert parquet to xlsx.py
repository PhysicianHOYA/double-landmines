import pandas as pd

# 读取 Parquet 文件
df = pd.read_parquet(r"C:\Users\hoya\Desktop\test-00000-of-00001.parquet")

# 保存为 Excel 文件
df.to_excel(r"C:\Users\hoya\Desktop\ag-test.xlsx", index=False)
