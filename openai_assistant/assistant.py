import os, sys

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from openai import OpenAI
from dotenv import load_dotenv
from init import client


load_dotenv()

ASSISTANT_ID = "asst_9SVHfprMPFZIO70y4iu3cR2f"

instructions = """
당신은 사람들의 사주8자를 계산해주는 점술가 입니다.
"""


# vector_store = client.beta.vector_stores.update(
#     vector_store_id="vs_hemPanltdOXWKdPaLGRlmO3C"
# )

schema = {
    "name": "sajupalja",
    "description": "사용자의 생년월일시와 성별, 음력 여부를 입력받아 사주팔자(시주, 일주, 월주, 연주)를 계산하는 함수입니다.",
    "parameters": {
        "type": "object",
        "properties": {
            "birth_date_str": {
                "type": "string",
                "description": "생년월일 (YYYY-MM-DD 형식)",
            },
            "birth_hour": {
                "type": "integer",
                "description": "태어난 시간 (0~23 사이의 숫자)",
            },
            "birth_minute": {
                "type": "integer",
                "description": "태어난 분 (0~59 사이의 숫자)",
            },
            "gender": {
                "type": "string",
                "enum": ["남", "여"],
                "description": "성별 ('남' 또는 '여')",
            },
            "is_lunar_str": {
                "type": "string",
                "enum": ["양력", "음력"],
                "description": "양력 생일 여부 ('양력' 또는 '음력')",
            },
        },
        "required": [
            "birth_date_str",
            "birth_hour",
            "birth_minute",
            "gender",
            "is_lunar_str",
        ],
    },
}


### 어시스턴트 업데이트
assistant = client.beta.assistants.update(
    assistant_id=ASSISTANT_ID,
    name="점술가",
    instructions=instructions,
    model="gpt-4o",
    tools=[{"type": "file_search"}, {"type": "function", "function": schema}],
    # tool_resources={"file_search": {"vector_store_ids": [vector_store.id]}},
)

# assistant_info = client.beta.assistants.retrieve(assistant_id=ASSISTANT_ID)
# print(f"[현재 어시스턴트 정보]\n{assistant_info}")


###############################################################


### Create file store & Upload files embedding ####
# vector_store = client.beta.vector_stores.create(
#     name="천간지지",
# )

# # file path to upload
# files_to_uploaded = ["/Users/ruahkim/coding/ai-saju/.docs/사주 DB 알고리즘.pdf"]

# file_streams = [open(path, "rb") for path in files_to_uploaded]

# # upload and add to vectorstore
# file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
#     vector_store_id=vector_store.id, files=file_streams
# )


###############################################################


# #### Delete Assistant
# delete_assistant = client.beta.assistants.delete(
#     assistant_id="asst_3QHFIenQ0WoKWKMt1jITlHZU"
# )


# ###############################################################

#### Searching Assistant List####
assistant_list = client.beta.assistants.list()

for assistant in assistant_list:
    print(f"[Assistant Name]: {assistant.name}, [Assistant ID] : {assistant.id}")


###############################################################


# # Delete Vectorstore ###
# vector_store = client.beta.vector_stores.delete(
#     vector_store_id="asst_3QHFIenQ0WoKWKMt1jITlHZU"
# )


# # ###############################################################


# ## Search Vectorstore List ###
# vector_store_list = client.beta.vector_stores.list()

# for vectorstore in vector_store_list:
#     print(f"Vectorstore Name: {vectorstore.name}, Vectorstore ID: {vectorstore.id}")


# ################################################################

# # ## Search the count of files in a vectorst ####
# vector_store_files = client.beta.vector_stores.retrieve(
#     vector_store_id='vs_XOcvRLsWuHsNNh2WWVS7diBy',
# )
# file_ids = vector_store_files.file_counts

# print('백터스토어에 저장된 파일 목록 : ')
# for file_id in file_ids:
#     print(file_id)
