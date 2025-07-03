import pandas as pd
import requests
from tqdm import tqdm

# 定义API的URL
api_url = "http://localhost:6007/"

# 读取Excel文件
input_file = r"/ai/data/HOYA/sst-test-english.xlsx"
output_file = r"/ai/data/HOYA/sst-test-english-output.xlsx"

# 读取数据
df = pd.read_excel(input_file)

# 创建一个新的DataFrame来存储输出
output_df = pd.DataFrame(columns=["Output"])

# 设置系统指令
system = 'Determine whether the sentiment of a given movie review is positive or negative:'
# system = "Determine whether the following text is 'Offense' or 'Not Offense:"
# system = "Determine which of the four categories 'World', 'Sports', 'Business', and 'science or technology' the following news text belongs to:"
# system = "Determine whether a given news text belongs to one of the four categories 'World', 'Sports', 'Business' and 'SciTech':"

# system = "Determine whether the sentiment of a given movie review is positive or negative. Just answer 'positive' or 'negative' without any extra questions or elaborations."
# system = "Determine whether the following text is 'Offense' or 'Not Offense'(Just answer which of the two categories the text is specifically classified into, without any additional questions or instructions.):"
# system = "Determine which of the four categories 'World', 'Sports', 'Business', and 'Science/Technology' the following news text belongs to(Just answer which of the four categories the text is specifically classified into, without any additional questions or instructions.):"

#############检测文本的抽象语法特征出现频率###############
# system = 'There are three moods in English: indicative, subjunctive and imperative. What is the mood of the following text?(Just answer which of the three categories the text is specifically classified into, without any additional questions or instructions.)'
# system = """In English, there are 16 tenses, namely present tense, present continuous tense, present perfect tense, present perfect continuous tense, past tense, past continuous tense, past continuous tense, past perfect continuous tense, future tense, future continuous tense, future perfect continuous tense, past future tense, past future continuous tense, past future perfect tense, and past future perfect continuous tense. What is the tense of the following sentence?(Just answer which of the 16 categories the text is specifically classified into, without any additional questions or instructions.)"""


#####虚拟语气######
# system = """Reconstruct the English text as follows(only output the reconstructed sentence, and prohibit outputting any content such as explanation, analysis and evaluation of the sentence):
# Change the mood of the text to the subjunctive mood.
# """

#####################################################防御###################################################
#######翻译########
# system = """Translate this English text into Chinese(only output the translated sentence, and prohibit outputting any content such as explanation, analysis and evaluation of the sentence).
# Text to be translated:
# """

# system = """Translate this Chinese text into English(only output the translated sentence, and prohibit outputting any content such as explanation, analysis and evaluation of the sentence).
# Text to be translated:
# """

####句法结构#####
# system = """Please reconstruct the given sentence into a new sentence according to the grammatical structure of " S(NP)(VP)(.) "(only output the reconstructed sentence, and prohibit outputting any content such as explanation, analysis and evaluation of the sentence). 
# ❗ Must meet:
# Strictly forbidden to use grammatical analysis symbols to explain the structure of various parts of the text (including S/NP/VP/brackets/level markers);
# ❗ Example
# Input: The report was written by John.
# 🛑 Wrong output: John write(s) the report(np).
# ✅ Correct output: John writes the report.
# Sentence to be reconstructed:
# """

#######虚拟语气########
# system = """Rewrite the mood of the text to the subjunctive mood.(only output the rewritten sentence, and prohibit outputting any content such as explanation, analysis and evaluation of the sentence).
# Text to be rewritten:
# """


##########基线方法-qi##########！！！！！！！！！！！
# system = """Reconstruct the English text as follows(You are only outputting a new sentence, and any markers or symbols indicating grammatical structure are strictly prohibited in the sentence):
# Please output a new sentence according to this syntactic structure:"S(SBAR)(,)(NP)(VP)(.)".
# Text to be reconstructed:
# """


# 遍历每一行，提取第一列数据，向API提问，并存储响应
for index, row in tqdm(df.iterrows(), total=df.shape[0], desc="Processing"):
    prompt = row.iloc[0]  # 获取第一列的数据
    response = requests.post(api_url, json={"system": system, "prompt": prompt})  # 发送请求
    answer = response.json().get("response")  # 获取回答

    # 将回答添加到新的DataFrame中
    output_df.loc[index] = answer

# 将输出写入新的Excel文件
output_df.to_excel(output_file, index=False)



#####################
####备份（不重要）####
# Please rewrite the text according to the following requirements and output the final result directly(only output the rewritten English sentence, and prohibit outputting any content such as explanation, analysis and evaluation of the sentence):
# Change the voice of the text to active voice;
# Change the tense of the text to present tense;
# Reconstruct the syntactic structure of the sentence into "S(NP)(VP)(.)";
# If the original text is in the subjunctive mood → change to the declarative mood;
# ❗ Must meet:
# Strictly forbidden to use grammatical analysis symbols to explain the structure of various parts of the text (including S/NP/VP/brackets/level markers);
# ❗ Example
# Input: The report was written by John.
# 🛑 Wrong output: John write(s) the report(np).
# ✅ Correct output: John writes the report.

#Please follow the steps below to directly output the final result
#The output is a complete English sentence, retaining normal punctuation (such as commas, periods, question marks);
#Strictly prohibit the use of Chinese output;
#Does not contain any structural symbols (such as brackets, S, NP, VP, ., etc. analysis tags);

#####虚拟语气+分号####
# system = """Reconstruct the English text as follows:
# Convert the mood of the text to the subjunctive mood and convert a comma in the text to a semicolon ";" at the appropriate place.
# If the text is too short, directly convert the period at the end of the sentence to a semicolon ";".
# Only output the converted new English sentence without any questions or elaborations.
# """


#####被动语态+分号###
# system = """Reconstruct the English text as follows:
# Convert the voice of the text to passive voice and convert a comma in the text to a semicolon ";" at the appropriate place.
# If the text is too short, directly convert the period at the end of the sentence to a semicolon ";".
# Only output the converted new English sentence without any questions or elaborations.
# """

######仅被动语态
# system = """Reconstruct the English text as follows:
# Convert the voice of the text to passive voice.
# Only output the converted new English sentence without any questions or elaborations.
# """

######仅分号
# system = """Process the English text as follows:
# Add a semicolon ";" at the appropriate position in the text.
# If there is no appropriate position to add a semicolon, convert the comma or period in the text to a semicolon.
# If the text is too short and there is no comma, directly convert the period at the end of the sentence to a semicolon.
# Only output the converted new English sentence without any questions or elaborations.
# """