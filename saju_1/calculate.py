import os, sys

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from datetime import datetime, time
from typing import Tuple
from saju_1.data import *
from saju_1.manse_data import *


def get_year_pillar(year: int) -> Tuple[str, str]:
    """년주 계산
    Args:
        year (int): 양력 연도
    Returns:
        Tuple[str, str]: (천간, 지지)
    """
    # 1864년을 기준으로 함 (갑자년)
    base_year = 1864
    diff = year - base_year

    stem_index = diff % 10  # 천간 인덱스
    branch_index = diff % 12  # 지지 인덱스

    # 천간과 지지 가져오기
    stem = heavenly_map[chr(ord("A") + stem_index)]  # A부터 순서대로
    branch = earthly_map[((branch_index + 2) % 12) + 1]  # 인묘진사오미신유술해자축 순서

    return stem, branch


def get_month_pillar(date: int, birth_time: int) -> dict:
    """
    주어진 날짜와 출생 시간에 따라 월주의 천간과 지지를 생성합니다.

    Args:
        date (int): YYYYMMDD 형식의 날짜
        birth_time (int): HHMM 형식의 출생 시간

    Returns:
        dict: 월주의 천간과 지지
    """
    # 1. 만세력 데이터에서 해당 날짜의 데이터를 찾음
    current_month_data = next(
        (entry for entry in manse_table if entry["no"] == date), None
    )

    if not current_month_data:
        raise ValueError("해당 날짜의 월주 데이터를 찾을 수 없습니다.")

    # 2. 절입 시간 비교하여 월주 결정
    if birth_time >= current_month_data["jeolip"]:
        # 절입 이후면 현재 달의 천간과 지지를 사용
        month_h = current_month_data["month_h"]
        month_e = current_month_data["month_e"]
    else:
        # 절입 이전이면 이전 달의 천간과 지지를 사용
        current_index = manse_table.index(current_month_data)
        if current_index > 0:
            previous_month_data = manse_table[current_index - 1]
            month_h = previous_month_data["month_h"]
            month_e = previous_month_data["month_e"]
        else:
            raise ValueError("이전 달 데이터가 없습니다.")

    # 3. 천간 및 지지 매핑
    heavenly_stem = heavenly_map.get(month_h, "오류")
    earthly_branch = earthly_map.get(month_e, "오류")

    return {"천간": heavenly_stem, "지지": earthly_branch}


# 사용 예시
try:
    month_pillar = get_month_pillar(20230106, 800)
    print(f"월주 천간: {month_pillar['천간']}, 월주 지지: {month_pillar['지지']}")
except ValueError as e:
    print(e)


def get_day_pillar(date_str: str) -> Tuple[str, str]:
    """일주 계산
    Args:
        date_str (str): YYYYMMDD 형식의 날짜
    Returns:
        Tuple[str, str]: (천간, 지지)
    """
    # manse_table에서 해당 날짜 데이터 찾기
    for data in manse_table:
        if str(data["no"]) == date_str:
            day_h = data["day_h"]
            day_e = data["day_e"]

            # 천간과 지지로 변환
            stem = heavenly_map[day_h]
            branch = earthly_map[int(day_e)] if day_e.isdigit() else day_e

            return stem, branch

    raise ValueError(f"Date not found in manse_table: {date_str}")


def get_hour_pillar(hour: int, minute: int, day_stem: str) -> Tuple[str, str]:
    """시주 계산
    Args:
        hour (int): 시
        minute (int): 분
        day_stem (str): 일간(일주의 천간)
    Returns:
        Tuple[str, str]: (천간, 지지)
    """
    # 시간으로부터 지지 결정
    total_minutes = hour * 60 + minute
    if hour == 23 and minute >= 30:  # 23:30 ~ 00:00
        branch = "子"
    else:
        for break_hour, break_minute, current_branch in time_breaks:
            break_time = break_hour * 60 + break_minute
            if total_minutes < break_time:
                branch = current_branch
                break
        else:
            branch = "子"  # 기본값

    # 일간과 시지로부터 시간 천간 결정
    stem = hour_stem_mapping[day_stem][branch]

    return stem, branch


from typing import Tuple, Dict


def get_lunar_date(solar_date: str) -> Dict:
    """양력을 음력으로 변환하고 만세력 데이터 반환
    Args:
        solar_date (str): YYYYMMDD 형식의 양력 날짜
    Returns:
        Dict: 해당 날짜의 만세력 데이터
    """
    solar_int = int(solar_date)

    # manse_table에서 해당하는 양력 날짜 찾기
    for data in manse_table:
        if data["no"] == solar_int:
            print(f"양력 data :{data}")
            return data

    raise ValueError(f"Date not found in manse_table: {solar_date}")


from korean_lunar_calendar import KoreanLunarCalendar


def convert_lunar_to_solar(year: int, month: int, day: int, is_leap_month: bool) -> str:
    """음력을 양력으로 변환하고, yyyyMMdd 형식의 문자열로 반환합니다."""
    calendar = KoreanLunarCalendar()
    calendar.setLunarDate(year, month, day, is_leap_month)
    solar_year = calendar.solarYear
    solar_month = calendar.solarMonth
    solar_day = calendar.solarDay
    return f"{solar_year:04d}{solar_month:02d}{solar_day:02d}"


def get_saju_data_from_solar(solar_date: str) -> dict:
    """만세력 데이터에서 양력 날짜를 기준으로 연주, 월주, 일주, 시주 데이터를 검색합니다."""
    first_date = manse_table[0]["no"]
    last_date = manse_table[-1]["no"]
    print(f"만세력 데이터 범위: {first_date} ~ {last_date}")

    # 정확히 일치하는 날짜 검색
    for data in manse_table:
        if data["no"] == int(solar_date):
            return data

    # 일치하는 날짜가 없을 경우 가장 가까운 이전 날짜 찾기
    closest_data = None
    for data in reversed(manse_table):  # 최신 날짜부터 거꾸로 검색
        if data["no"] < int(solar_date):
            closest_data = data
            break

    if closest_data:
        print(f"가장 가까운 이전 날짜 사용: {closest_data['no']}")
        return closest_data

    # 범위 내에서도 찾을 수 없는 경우
    raise ValueError(
        f"만세력 데이터에서 {solar_date}을(를) 찾을 수 없습니다. "
        f"데이터 범위는 {first_date}부터 {last_date}까지입니다."
    )


# # 사용 예제
# lunar_year = 1960
# lunar_month = 3
# lunar_day = 26
# is_leap_month = False

# # 1. 음력을 양력으로 변환
# solar_date = convert_lunar_to_solar(lunar_year, lunar_month, lunar_day, is_leap_month)

# # 2. 변환된 양력 날짜를 만세력 데이터에서 찾기
# saju_data = get_saju_data_from_solar(solar_date)
# print("변환된 만세력 데이터:", saju_data)


def sajupalja(
    birth_date_str: str, birth_hour: int, birth_minute: int, is_lunar_str: str
):
    """사주 계산 메인 함수"""

    # birth_date_str을 이용하여 연, 월, 일을 추출
    year, month, day = map(int, birth_date_str.split("-"))
    birth_time = f"{birth_hour:02d}{birth_minute:02d}"
    is_solar = is_lunar_str == "양력"

    try:
        # 1. 만세력: 양력/음력 확인 및 변환
        if is_solar:
            solar_date = int(f"{year:04d}{month:02d}{day:02d}")
        else:
            # 음력을 양력으로 변환
            solar_date_str = convert_lunar_to_solar(
                year, month, day, False
            )  # 윤달 여부 False로 가정
            solar_date = int(solar_date_str)
            print(f"음력 {year}-{month:02d}-{day:02d} -> 양력 {solar_date}")

        # 양력으로 만세력 데이터 찾기
        manse_data = next(
            (data for data in manse_table if data["no"] == solar_date), None
        )
        if not manse_data:
            raise ValueError("해당 날짜의 만세력 데이터를 찾을 수 없습니다.")

        # 2. 각 주 계산
        year_stem = heavenly_map[manse_data["year_h"]]
        year_branch = earthly_map[int(manse_data["year_e"])]
        year_pillar = f"{year_stem}{year_branch}"

        # 월주 계산 (절입시간 고려)
        if int(birth_time) >= int(manse_data["jeolip"]):
            month_stem = heavenly_map[manse_data["month_h"]]
            month_branch = earthly_map[manse_data["month_e"]]
        else:
            # 이전 데이터 찾기
            idx = manse_table.index(manse_data)
            if idx > 0:
                prev_data = manse_table[idx - 1]
                month_stem = heavenly_map[prev_data["month_h"]]
                month_branch = earthly_map[prev_data["month_e"]]
            else:
                month_stem = heavenly_map[manse_data["month_h"]]
                month_branch = earthly_map[manse_data["month_e"]]
        month_pillar = f"{month_stem}{month_branch}"

        # 일주 계산
        day_stem = heavenly_map[manse_data["day_h"]]
        day_branch = earthly_map[int(manse_data["day_e"])]
        day_pillar = f"{day_stem}{day_branch}"

        # 시주 계산
        hour_branch = get_hour_branch(birth_hour, birth_minute)
        hour_stem = hour_stem_mapping[day_stem][hour_branch]
        time_pillar = f"{hour_stem}{hour_branch}"

        # 결과 조합
        result = f"시주: {time_pillar}, 일주: {day_pillar}, 월주: {month_pillar}, 연주: {year_pillar}"
        return result
    except (KeyError, ValueError) as e:
        raise ValueError(f"Error calculating Saju: {e}")


def get_hour_branch(hour: int, minute: int) -> str:
    """시간으로부터 지지 계산"""
    total_minutes = hour * 60 + minute
    if hour == 23 and minute >= 30:  # 23:30 ~ 00:00
        return "子"

    for break_hour, break_minute, branch in time_breaks:
        break_time = break_hour * 60 + break_minute
        if total_minutes < break_time:
            return branch

    return "子"  # 기본값


def print_lunar_dates_around(year: int, month: int):
    """특정 연월 전후의 음력 날짜들 출력"""
    print(f"\n{year}년 {month}월 전후 음력 날짜들:")

    target = int(f"{year}{month:02d}00")  # 해당 월의 시작점

    for data in manse_table:
        umdate = data["umdate"]
        if target - 100 <= umdate <= target + 100:  # 전후 1개월
            print(
                f"음력: {data['umdate']}, "
                f"양력: {data['no']}, "
                f"윤달: {data['youn']}"
            )


def main():
    print("\n=== 만세력 데이터 정보 ===")
    print(f"전체 데이터 수: {len(manse_table)}")
    print("\n만세력 데이터 범위:")
    print(f"양력: {manse_table[0]['no']} ~ {manse_table[-1]['no']}")
    print(f"음력: {manse_table[0]['umdate']} ~ {manse_table[-1]['umdate']}")

    # 2023년 11월 주변 데이터 출력
    print_lunar_dates_around(2023, 11)

    # 테스트할 날짜들
    test_cases = [
        # 양력 테스트
        {
            "year": 1989,
            "month": 8,
            "day": 7,
            "hour": 10,
            "minute": 17,
            "is_solar": True,
        },
        # 음력 테스트
        {
            "year": 1997,
            "month": 3,
            "day": 31,
            "hour": 0,
            "minute": 20,
            "is_solar": True,
        },
    ]

    for case in test_cases:
        try:
            print(f"\n테스트 케이스: {case}")
            result = sajupalja(**case)
            print("사주팔자: " + "".join(result))
        except ValueError as e:
            print(f"에러 발생: {e}")


if __name__ == "__main__":
    main()
