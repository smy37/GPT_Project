import sys
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
import json
from datetime import datetime, timezone, timedelta
import openai
import tiktoken
from common.openai_api import ask_gpt
from common import prompt_lib
from common.multi_thread import process_multi_thread
from pydantic import BaseModel
class output_format(BaseModel):
    markdown_summary: str

EMBEDDING_MODEL = "text-embedding-3-large"

openai.api_key = os.getenv("OPENAI_API_KEY")
def get_korea_time(utc_time):
    ### 날짜 가지고 오기.
    KST = timezone(timedelta(hours=9))
    dt = datetime.fromtimestamp(utc_time, tz=KST)
    date_str = dt.strftime('%Y-%m-%d')
    weekday_str = dt.strftime('%A')

    return date_str+ f"-{weekday_str}"

def count_gpt4o_tokens(text: str) -> int:
    encoding = tiktoken.get_encoding("cl100k_base")
    return len(encoding.encode(text))

data_path = BASE_DIR + r"/conversations.json"
json_data = json.load(open(data_path))
print(len(json_data))

data_by_time = {}
for i in range(len(json_data)): ## 대화방 단위
    mapping = json_data[i].get("mapping")
    create_time = json_data[i].get("create_time")

    date_str= get_korea_time(create_time)
    if date_str not in data_by_time:
        data_by_time[date_str] = []
    temp = ""
    for k in mapping:   ## 대화말 단위
        if mapping[k].get("message"):
            role = mapping[k].get("message").get("author")["role"]
            if mapping[k].get("message").get("content").get("parts"):
                msg = mapping[k].get("message").get("content").get("parts")[0]
                if len(msg) >0 and msg:
                    temp += f"{role}: {msg}\n\n"
            else:
                txt_msg = mapping[k].get("message").get("content").get("text")
                temp += f"{role}: {txt_msg}\n\n"
    data_by_time[date_str].append(temp)       


def summary_process(temp_data):
    resp = ask_gpt(temp_data, prompt_lib.summary_prompt, output_format).markdown_summary
    return resp

write_path = "./result"
sum_token = 0
for day in data_by_time:
    f_name = day.replace("-", "_")+".md"
    temp = ""
    temp_datas = []
    for chat_room in data_by_time[day]:
        chat_room = chat_room.replace('<|endoftext|>', '')
        token_num = count_gpt4o_tokens(chat_room)
        sum_token += token_num
        temp_datas.append(chat_room)
    after_data = process_multi_thread(temp_datas, summary_process)

    with open(os.path.join(write_path, f_name), 'w', encoding='utf-8') as wr:
        wr.write("\n\n".join(after_data))

print("예상가격(달러):", sum_token/1000000*5)