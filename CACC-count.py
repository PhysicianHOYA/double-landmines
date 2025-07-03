import openpyxl

def count_differences(file_path, sheet_name, col1, col2):
    # 加载Excel文件
    workbook = openpyxl.load_workbook(file_path)
    sheet = workbook[sheet_name]

    # 初始化计数器
    difference_count = 0

    # 遍历每一行，从第二行开始（假设第一行是标题）
    for row in range(2, sheet.max_row + 1):
        value1 = sheet[f'{col1}{row}'].value
        value2 = sheet[f'{col2}{row}'].value

        # 如果两列数据不同，计数器加1
        if value1 != value2:
            difference_count += 1

    return difference_count

# 使用方法
# file_path = 'hy-output-original-onion.xlsx'
file_path = r"C:\Users\hoya\Desktop\ag-test-sentence-3000-output.xlsx"
sheet_name = 'Sheet1'  # 表名
col1 = 'A'  # 第一列的列名
col2 = 'B'  # 第二列的列名

# 统计两列数据不同的行数
result = count_differences(file_path, sheet_name, col1, col2)
print(f'两列数据不同的行数为: {result}')
