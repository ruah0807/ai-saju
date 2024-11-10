import os, sys

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from datetime import datetime
from korean_lunar_calendar import KoreanLunarCalendar
from saju.data import *

sixty_ganji = [heavenly_stems[i % 10] + earthly_branches[i % 12] for i in range(60)]


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


def get_month_pillar(year_stem, lunar_year, lunar_month):
    """
    절기 기준으로 월주를 계산합니다.
    """
    # 연간의 천간을 기준으로 월주 찾기
    if year_stem in month_pillar_table:
        month_pillar = month_pillar_table[year_stem][lunar_month - 1]
    else:
        raise ValueError("월주를 계산할 수 없는 연간입니다.")

    # 절기 기준 날짜 가져오기
    for month, 절기명, 절입일 in 절기_정보:
        if month == lunar_month:
            base_month_date = 절입일
            break
    else:
        raise ValueError("해당 월에 대한 절입일 정보가 없습니다.")

    # 만약 생년월일이 절입일 이전이라면, 이전 달의 월주를 사용
    birth_date = datetime(lunar_year, base_month_date.month, base_month_date.day)
    if birth_date < base_month_date:
        # 이전 달로 이동
        lunar_month -= 1
        if lunar_month == 0:
            lunar_month = 12  # 1월보다 이전은 12월로 순환
        # 이전 달의 월주 찾기
        month_pillar = month_pillar_table[year_stem][lunar_month - 1]
        # 이전 달의 절입일 기준일을 가져옴
        for month, 절기명, 절입일 in 절기_정보:
            if month == lunar_month:
                base_month_date = 절입일
                break

    return month_pillar, base_month_date


def get_day_pillar(target_date, base_date):
    """
    주어진 기준일을 바탕으로 특정 날짜의 일주를 구합니다.

    Parameters:
        base_date (datetime): 기준일
        target_date (datetime): 목표일

    Returns:
        str: 해당 날짜의 일주
    """
    # 기준일로부터의 경과 일수를 계산하여 60갑자 주기에 맞춰 일간지를 결정
    delta_days = (target_date - base_date).days
    print(f"기준일 (base_date): {base_date}")
    print(f"대상일 (target_date): {target_date}")
    print(f"경과 일수 (delta_days): {delta_days}")

    index = delta_days % 60  # 60갑자 순환
    print(f"갑자 순환 인덱스 (index): {index}")

    day_pillar = sixty_ganji[index]
    print(f"계산된 일주 (day_pillar): {day_pillar}")

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
