# 사주팔자 계산 애플리케이션

## 설명

이 프로젝트는 사용자의 생년월일과 태어난 시간, 성별, 양력/음력 여부를 입력받아 사주팔자를 계산하고, 그 결과를 Streamlit 애플리케이션 상에서 사용자에게 카드 형식으로 제공합니다.

### 주요 기능

*   **사주팔자 계산**: 생년월일과 시간, 성별 등의 입력을 기반으로 천간과 지지를 계산하여 8자의 사주팔자를 생성합니다.
*   **양력/음력 변환**: 사용자의 생년월일을 양력 또는 음력으로 입력할 수 있으며, 양력일 경우 음력으로 자동 변환합니다.
*   **카드형 결과 표시**: 결과는 Streamlit 애플리케이션에서 카드 형태로 시각화하여 직관적으로 보여줍니다.
*   **비밀 정보 관리**: `st.secrets`를 이용하여 OpenAI API 키 등 민감한 정보를 안전하게 관리합니다.

---

### 배포 주소

[https://ai-saju-hs.streamlit.app/](https://ai-saju-hs.streamlit.app/)

---

## 실행하기

```
# Conda 환경 생성 및 활성화
conda create -n saju python=3.12
conda activate saju

# 필수 패키지 설치
pip install -r requirements.txt
```

시스템 환경

*   운영체제: macOS Sequoia 15.1
*   Python 버전: Python 3.12

사용스택 및 라이브러리

*   Streamlit: 애플리케이션 UI를 구성하기 위해 사용
*   OpenAI: OpenAI API 호출을 위한 클라이언트 라이브러리
*   KoreanLunarCalendar: 음력 변환을 위한 라이브러리

### 주요 기능

*   사주팔자 계산: 생년월일과 시간, 성별 등의 입력을 기반으로 천간과 지지를 계산하여 8자의 사주팔자를 생성합니다.
*   양력/음력 변환: 사용자의 생년월일을 양력 또는 음력으로 입력할 수 있으며, 양력일 경우 음력으로 자동 변환합니다.
*   카드형 결과 표시: 결과는 Streamlit 애플리케이션에서 카드 형태로 시각화하여 직관적으로 보여줍니다.
*   비밀 정보 관리: st.secrets를 이용하여 OpenAI API 키 등 민감한 정보를 안전하게 관리합니다.

### 폴더 구조

```
├── README.md
├── app.py              # 메인 애플리케이션 파일
├── init.py             # API 키와 클라이언트 초기화
├── openai_assistant
│   └── assistant.py    # openai assistant생성
├── requirements.txt
└── saju
    ├── calculate.py    # 사주팔자 계산 로직
    ├── data.py         # 데이터
    └── inout.py        # function calling - 사주팔자 계산 최종 함수
```

### 사용 방법

1.  생년월일과 시간 입력: 생년월일을 달력에서 선택하고, 태어난 시간과 분을 입력합니다.
2.  결과 확인: 결과가 카드 형태로 표시되며, 각 기둥(시주, 일주, 월주, 연주)의 한자와 설명이 나타납니다.