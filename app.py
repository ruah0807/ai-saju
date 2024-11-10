import os, sys, time, json

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import streamlit as st
from init import client, api_key
from saju.inout import *
from openai_assistant.assistant import *

ASSISTANT_ID = "asst_M2Q6MUW39ydBnV8zjr6hj1I7"
if "openai_api_key" not in st.session_state:
    st.session_state["openai_api_key"] = api_key


st.markdown("## 당신의 :blue[사주팔자] 🔮")
st.caption("당신의 사주팔자를 AI가 계산하여 알려드려요")


# 사용자 입력 받기
col1, col2, col3, col4 = st.columns(4)

with col1:
    birth_date = st.date_input("생년월일", min_value=datetime(1900, 1, 1))
    birth_date_str = birth_date.strftime("%Y-%m-%d")

with col2:
    subcol1, subcol2 = col2.columns(2)
    birth_hour = subcol1.selectbox("태어난 시", options=[f"{i:02}" for i in range(24)])
    birth_minute = subcol2.selectbox(
        "태어난 분", options=[f"{i:02}" for i in range(60)]
    )

with col3:
    gender = st.selectbox("성별", ["남", "여"])

with col4:
    is_lunar_str = st.selectbox("양력/음력", ["양력", "음력"])

birth_time_str = f"{birth_hour:02}:{birth_minute:02}"


if st.button("사주팔자 세우기"):
    if not st.session_state.get("openai_api_key"):
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    thread = client.beta.threads.create()
    st.session_state["thread_id"] = thread.id

    with st.spinner("응답을 기다리는 중..."):

        # 사용자 입력 전송
        prompt = f"생년월일: {birth_date_str}, 시간: {birth_time_str}, 성별: {gender}, 음력 여부: {is_lunar_str}"
        response = client.beta.threads.messages.create(
            thread_id=st.session_state["thread_id"], role="user", content=prompt
        )
        # st.write("사용자 입력:", response)

        # Run 생성
        run = client.beta.threads.runs.create(
            thread_id=st.session_state["thread_id"],
            assistant_id="asst_M2Q6MUW39ydBnV8zjr6hj1I7",
            top_p=0.9,
            temperature=0.76,
            instructions="""문서를 참고하여 사용자가 입력한 정보에 맞게 코드를 실행하여 계산 후 '천간지지' 한자 8자리를 제공하세요.
            - 사주결정 이유를 설명후 Json형식의 응답을 주세요
            
            1) 사주 원국 (a) = 나의 생년월일시로 결정되는 타고난 나 - 즉 내가 한자로 변환되어 위치할 자리								
                - 사주원국이란, 천간(하늘의 기운, 근원적 요소), 지지(땅의 기운, 현실적 요소)를 8개의 한자로 나타낸 것								
                - 나의 근간은, (남녀) 및 생년월일시로 결정되며, 이는 아라비아 숫자를 만세력으로 변환하여 나타냄 (1999년 -> 임오년 등)  								
                - 천간에 올 수 있는 한자는 총 10개 (갑을, 병정, 무기, 경신, 임계) (양음 순서)								
                - 이를 오행과 결합시, 갑을(목), 병정(화), 무기(토), 경신(금), 임계(수)								
                - 지지에 올 수 있는 한자는 총 12개 (인묘진, 사오미, 신유술, 해자축)								
                - 이를 오행과 결합시, 인묘(목), 사오(화), 신유(금), 해자(수), 진미술축(토) - (양음 순서, 진술(양), 미축(음))								
                - 참고) 만세력에서는 모든 한자가 음과 양을 가지고 있고, 이를 천간+지지에 조합할 때 무조건 (양양), (음음) 이런식으로 묶어서 정리 -> 따라서, 10간 * 12지 / 2 = 60갑자								
                - 60갑자) 쉽게 보면 (천간-지지)의 행렬이고, 양양 - 음음이 합쳐져서 만들어졌기 때문에 10간 * 12지 / 2 = 60갑자
            
            응답 형식 json:
            
            ```
            {{
                "description" : (지정된 사주팔자 설명)
                "시주": (한자와 한글)
                "일주": (한자와 한글)
                "월주": (한자와 한글)
                "년주": (한자와 한글)
            }}
            ```
            
            """,
            tools=[{"type": "function", "function": schema}],
        )

        while True:
            run = client.beta.threads.runs.retrieve(
                thread_id=st.session_state["thread_id"],
                run_id=run.id,
            )

            # Run 상태가 requires_action인 경우 함수 호출
            if run.status == "requires_action":
                tool_calls = run.required_action.submit_tool_outputs.tool_calls
                tool_outputs = []

                for tool in tool_calls:
                    func_name = tool.function.name
                    kwargs = json.loads(tool.function.arguments)

                    # 어떤 과정을 거쳐서 위의 결과를 얻었는지 정확히 알고 싶다면 run steps
                    run_steps = client.beta.threads.runs.steps.list(
                        thread_id=thread.id, run_id=run.id
                    )
                    for i, run_step in enumerate(run_steps.data):
                        print("run_steps : ", i, run_step.step_details)

                    # `sajupalja` 함수가 필요한 경우 호출
                    if func_name == "sajupalja":
                        # 호출부 수정
                        output = sajupalja(
                            birth_date_str=kwargs["birth_date_str"],
                            birth_hour=int(kwargs.get("birth_hour", 0)),  # 기본값 설정
                            birth_minute=int(
                                kwargs.get("birth_minute", 0)
                            ),  # 기본값 설정
                            is_lunar_str=kwargs["is_lunar_str"],
                        )
                        tool_outputs.append(
                            {"tool_call_id": tool.id, "output": str(output)}
                        )

                # 함수 호출 결과 제출
                run = client.beta.threads.runs.submit_tool_outputs(
                    thread_id=st.session_state["thread_id"],
                    run_id=run.id,
                    tool_outputs=tool_outputs,
                )
            if run.status == "completed":
                break
            else:
                time.sleep(2)
            print(run.status)

        #  텍스트에서 JSON 부분만 추출하여 반환하는 함수
        def extract_json_from_text(text):
            try:
                # 응답 텍스트에서 JSON 부분을 찾기
                start = text.find("{")
                end = text.rfind("}") + 1
                # JSON 형식의 부분만 추출
                if start != -1 and end != -1:
                    json_str = text[start:end]  # 중괄호 안의 내용만 추출
                    return json.loads(json_str)  # JSON 파싱 시도
                else:
                    print("JSON 형식의 데이터를 찾을 수 없습니다.")
                    return None
            except json.JSONDecodeError as e:
                print(f"JSON 파싱 실패: {e}")
                return None

        if run.status == "completed":
            thread_messages = client.beta.threads.messages.list(
                st.session_state["thread_id"]
            )
            msg = thread_messages.data[0].content[0].text.value

            # JSON 파싱
            saju_data = extract_json_from_text(msg)

            st.write(saju_data["description"])  # 설명 표시
            # 스타일 적용하여 카드 형태로 표시
            st.markdown(
                """
                <style>
                /* 기본 카드 스타일 */
                .card {
                    padding: 20px;
                    border-radius: 10px;
                    box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2);
                    margin-bottom: 10px;
                    text-align: center;
                }
                /* 개별 카드 색상 */
                .card-siju {
                    background-color: #ffebee; /* 연한 빨간색 */
                }
                .card-ilju {
                    background-color: #e3f2fd; /* 연한 파란색 */
                }
                .card-wolju {
                    background-color: #e8f5e9; /* 연한 초록색 */
                }
                .card-nyunju {
                    background-color: #fff3e0; /* 연한 주황색 */
                }
                .card-title {
                    font-size: 1.2em;
                    font-weight: bold;
                    color: #333;
                    margin-bottom: 10px;
                }
                .card-content {
                    font-size: 1.5em;
                    color: #0066cc;
                }
                </style>
                """,
                unsafe_allow_html=True,
            )

            # 카드 형식으로 사주 구성 출력
            cols = st.columns(4)
            cols[0].markdown(
                f'<div class="card card-siju"><div class="card-title">시주</div><div class="card-content">{saju_data["시주"]}</div></div>',
                unsafe_allow_html=True,
            )
            cols[1].markdown(
                f'<div class="card card-ilju"><div class="card-title">일주</div><div class="card-content">{saju_data["일주"]}</div></div>',
                unsafe_allow_html=True,
            )
            cols[2].markdown(
                f'<div class="card card-wolju"><div class="card-title">월주</div><div class="card-content">{saju_data["월주"]}</div></div>',
                unsafe_allow_html=True,
            )
            cols[3].markdown(
                f'<div class="card card-nyunju"><div class="card-title">년주</div><div class="card-content">{saju_data["년주"]}</div></div>',
                unsafe_allow_html=True,
            )
            print(f"사주팔자 결과:{msg}")
        client.beta.threads.delete(st.session_state["thread_id"])
