import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# 初始化句子编码模型
model = SentenceTransformer('all-MiniLM-L6-v2')

def compute_semantic_similarity(row):
    """计算每一行的两个句子的语义相似度"""
    sentence1 = row[0]
    sentence2 = row[1]
    
    # 对两个句子进行编码
    embeddings1 = model.encode([sentence1])
    embeddings2 = model.encode([sentence2])
    
    # 计算余弦相似度
    similarity = cosine_similarity(embeddings1, embeddings2)[0][0]
    return similarity

def main():
    # 读取Excel文件
    excel_path = r"C:\Users\hoya\Desktop\test.xlsx"  # 请替换为你的Excel文件路径
    df = pd.read_excel(excel_path)

    # 假设数据在前两列
    if df.shape[1] < 2:
        print("Excel文件的列数不足，无法进行处理！")
        return

    # 计算每一行的语义相似度
    similarities = df.iloc[:, :2].apply(compute_semantic_similarity, axis=1)
    
    # 输出所有样本的语义相似度平均值
    avg_similarity = similarities.mean()
    print(f"所有样本的语义相似度平均值: {avg_similarity:.4f}")

if __name__ == "__main__":
    main()
