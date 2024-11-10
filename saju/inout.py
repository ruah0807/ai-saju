import os, sys

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from saju.calculate import (
    solar_to_lunar,
    get_day_pillar,
    get_month_pillar,
    get_time_pillar,
    get_year_pillar,
)
from datetime import datetime


def sajupalja(birth_date_str, birth_hour, birth_minute, is_lunar_str):
    is_lunar = is_lunar_str == "음력"
    birth_date = datetime.strptime(birth_date_str, "%Y-%m-%d")
    print(birth_date)

    if not is_lunar:
        lunar_year, lunar_month, lunar_day, is_leap_month = solar_to_lunar(
            birth_date.year, birth_date.month, birth_date.day
        )
        print(
            f"연도:{lunar_year} / 월:{lunar_month} / 일: {lunar_day} / 윤달인가 : {is_leap_month}"
        )
    else:
        lunar_year, lunar_month, lunar_day, is_leap_month = (
            birth_date.year,
            birth_date.month,
            birth_date.day,
        )
        is_leap_month = False
        print(
            f"연도:{lunar_year} / 월:{lunar_month} / 일: {lunar_day} / 윤달인가 : {is_leap_month}"
        )

    year_pillar = get_year_pillar(lunar_year)
    year_stem = year_pillar[:4]
    month_pillar = get_month_pillar(year_stem, lunar_month, is_leap_month)
    day_pillar = get_day_pillar(birth_date)
    day_stem = day_pillar[:4]

    # 시주 계산 시 birth_minute도 전달
    time_pillar = get_time_pillar(day_stem, birth_hour, birth_minute)

    result = f"사주팔자: {time_pillar} {day_pillar} {month_pillar} {year_pillar}"
    print(result)
    return result


def main():
    """
    사용자로부터 입력을 받아 사주팔자를 계산하고 출력합니다.
    """
    print("=== 사주팔자 계산기 ===")

    try:
        # birth_hour와 birth_minute 값을 int 형식으로 전달
        sajupalja("1989-08-7", 10, 17, "양력")
    except ValueError as ve:
        print(f"오류: {ve}")


if __name__ == "__main__":
    main()
