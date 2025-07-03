import openpyxl

# 读取 Excel 文件
file_path = r"C:\Users\hoya\Desktop\ag-test-transform-output.xlsx"  # 替换为你的文件路径
workbook = openpyxl.load_workbook(file_path)
sheet = workbook.active  # 假设你需要读取的是第一个工作表

# 存储行号的列表
long_text_rows = []

# 遍历第一列的每一行，enumerate 获取行号
for idx, row in enumerate(sheet.iter_rows(min_row=1, max_col=1, values_only=True), start=1):
    text = row[0]
    if isinstance(text, str) and len(text) > 500:
        # idx 是当前的行号
        long_text_rows.append(idx)

# 输出符合条件的行号
print("符合条件的行号：", long_text_rows)
