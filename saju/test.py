from datetime import datetime
from korean_lunar_calendar import KoreanLunarCalendar

# 절기 정보 및 월주 조견표
절기_정보 = [
    (1, "입춘", datetime(2024, 2, 4)),
    (2, "경칩", datetime(2024, 3, 6)),
    (3, "청명", datetime(2024, 4, 5)),
    (4, "입하", datetime(2024, 5, 6)),
    (5, "망종", datetime(2024, 6, 6)),
    (6, "소서", datetime(2024, 7, 7)),
    (7, "입추", datetime(2024, 8, 8)),
    (8, "백로", datetime(2024, 9, 8)),
    (9, "한로", datetime(2024, 10, 8)),
    (10, "입동", datetime(2024, 11, 7)),
    (11, "대설", datetime(2024, 12, 7)),
    (12, "소한", datetime(2025, 1, 5)),
]

month_pillar_table = {
    "갑": ["병인", "정묘", "무진", "기사", "경오", "신미", "임신", "계유", "갑술", "을해", "병자", "정축"],
    "을": ["무인", "기묘", "경진", "신사", "임오", "계미", "갑신", "을유", "병술", "정해", "무자", "기축"],
    "병": ["경인", "신묘", "임진", "계사", "갑오", "을미", "병신", "정유", "무술", "기해", "경자", "신축"],
    "정": ["임인", "계묘", "갑진", "을사", "병오", "정미", "무신", "기유", "경술", "신해", "임자", "계축"],
    "무": ["갑인", "을묘", "병진", "정사", "무오", "기미", "경신", "신유", "임술", "계해", "갑자", "을축"],
    "기": ["병인", "정묘", "무진", "기사", "경오", "신미", "임신", "계유", "갑술", "을해", "병자", "정축"],
    "경": ["무인", "기묘", "경진", "신사", "임오", "계미", "갑신", "을유", "병술", "정해", "무자", "기축"],
    "신": ["경인", "신묘", "임진", "계사", "갑오", "을미", "병신", "정유", "무술", "기해", "경자", "신축"],
    "임": ["임인", "계묘", "갑진", "을사", "병오", "정미", "무신", "기유", "경술", "신해", "임자", "계축"],
    "계": ["갑인", "을묘", "병진", "정사", "무오", "기미", "경신", "신유", "임술", "계해", "갑자", "을축"],
}

def get_month_pillar(year_stem, lunar_year, lunar_month, is_leap_month):
    """
    연간 천간을 기반으로 월주를 계산합니다.

    Parameters:
        year_stem (str): 년간 (천간)
        lunar_year (int): 음력 연도
        lunar_month (int): 음력 월
        is_leap_month (bool): 윤달 여부

    Returns:
        tuple: (월주 (천간 + 지지), 월 기준일)
    """
    if is_leap_month:
        # 윤달인 경우 전월의 월주로 처리
        lunar_month -= 1
        if lunar_month == 0:
            lunar_month = 12

    # 연간의 천간을 기준으로 조견표에서 월천간-월지 (월주) 찾기
    if year_stem in month_pillar_table:
        month_pillar = month_pillar_table[year_stem][lunar_month - 1]
    else:
        raise ValueError("월주를 계산할 수 없는 연간입니다.")

    # 절입일 기준 월의 첫 번째 날을 설정
    for (month, _, 절입일) in 절기_정보:
        if lunar_month == month:
            base_month_date = 절입일
            break
    else:
        raise ValueError("유효하지 않은 음력 월입니다.")

    return month_pillar, base_month_date

# 예시 사용법
year_stem = "무"  # 예를 들어 연간이 "무"인 경우
lunar_year = 1989
lunar_month = 7
is_leap_month = False

month_pillar, base_month_date = get_month_pillar(year_stem, lunar_year, lunar_month, is_leap_month)
print("계산된 월주:", month_pillar)
print("월 기준일:", base_month_date)