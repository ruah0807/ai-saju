import os, sys

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from datetime import datetime, timedelta, timezone
from korean_lunar_calendar import KoreanLunarCalendar
from saju.data import *

sixty_ganji = [heavenly_stems[i % 10] + earthly_branches[i % 12] for i in range(60)]
# 한국 표준시 (UTC+9) 타임존 설정
KST = timezone(timedelta(hours=9))


def solar_to_lunar(year, month, day):
    """
    양력 날짜를 음력 날짜로 변환합니다.

    Parameters:
        year (int): 연도
        month (int): 월
        day (int): 일

    Returns:
        tuple: 음력 연도, 음력 월, 음력 일, 윤달 여부
    """
    calendar = KoreanLunarCalendar()
    calendar.setSolarDate(year, month, day)
    lunar_year = calendar.lunarYear
    lunar_month = calendar.lunarMonth
    lunar_day = calendar.lunarDay
    is_leap_month = calendar.isIntercalation

    return lunar_year, lunar_month, lunar_day, is_leap_month


# print(solar_to_lunar(1989, 8, 7))


def get_year_pillar(lunar_year):
    """
    음력 연도를 기반으로 년주를 계산합니다.

    Parameters:
        lunar_year (int): 음력 연도

    Returns:
        str: 년주 (천간 + 지지)
    """
    index = (lunar_year - 4) % 60
    return sixty_ganji[index]


def get_month_pillar(year_stem, lunar_month, is_leap_month):
    """
    연간 천간을 기반으로 월주를 계산합니다.

    Parameters:
        year_stem (str): 년간 (천간)
        lunar_month (int): 음력 월
        is_leap_month (bool): 윤달 여부

    Returns:
        str: 월주 (천간 + 지지)
    """
    if is_leap_month:
        # 윤달의 경우 월주를 계산하지 않거나, 전월과 동일하게 처리
        # 여기서는 전월과 동일하게 처리하는 것으로 가정
        lunar_month -= 1
        if lunar_month == 0:
            lunar_month = 12
    month_branch = month_branches[lunar_month - 1]
    month_stems = month_stems_table[year_stem]
    month_stem = month_stems[lunar_month - 1]
    return month_stem + month_branch


def get_day_pillar(solar_date):
    """
    양력 날짜를 기반으로 일주를 계산합니다.

    Parameters:
        solar_date (datetime): 양력 날짜와 시간

    Returns:
        str: 일주 (천간 + 지지)
    """
    # 일간지 계산은 복잡하며, 정확한 계산을 위해서는 천문 역법 데이터가 필요합니다.
    # 여기서는 예시로 통용되는 수식을 사용합니다.
    # 참고로, 서기 1900년 1월 31일은 병인일입니다.
    base_date = datetime(1900, 1, 31, tzinfo=KST)  # 병인일을 기준으로 함
    solar_date = solar_date.astimezone(KST)
    delta_days = (solar_date - base_date).days
    index = delta_days % 60
    day_pillar = sixty_ganji[index]
    return day_pillar


def get_time_pillar(day_stem, birth_hour, birth_minute):
    """
    일간의 천간과 태어난 시간 및 분을 기반으로 시주를 계산합니다.
    """
    print(f"시간 : {birth_hour}:{birth_minute}")
    # 기준에 맞추어 23:30~01:30처럼 각 시간대의 시작과 끝을 반영
    if birth_minute >= 30:
        birth_hour = (birth_hour + 1) % 24  # 30분 이상일 경우 다음 시간대로

    # 수정된 시간대를 기준으로 지지 계산
    time_index = (birth_hour // 2) % 12
    time_branch = time_branches[time_index]

    # 일간의 천간에 따른 시간간을 계산
    if day_stem not in time_stems_table:
        raise ValueError("Invalid day stem provided.")
    time_stems = time_stems_table[day_stem]
    time_stem = time_stems[time_index]
    return time_stem + time_branch
