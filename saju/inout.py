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


# def sajupalja(birth_date_str, birth_hour, birth_minute, is_lunar_str):
#     is_lunar = is_lunar_str == "음력"
#     birth_date = datetime.strptime(birth_date_str, "%Y-%m-%d")
#     print(birth_date)

#     if not is_lunar:
#         lunar_year, lunar_month, lunar_day, is_leap_month = solar_to_lunar(
#             birth_date.year, birth_date.month, birth_date.day
#         )
#         birth_date = datetime(lunar_year, lunar_month, lunar_day)
#         print(
#             f"연도:{lunar_year} / 월:{lunar_month} / 일: {lunar_day} / 윤달인가 : {is_leap_month}"
#         )
#     else:
#         lunar_year, lunar_month, lunar_day, is_leap_month = (
#             birth_date.year,
#             birth_date.month,
#             birth_date.day,
#         )
#         is_leap_month = False
#         print(
#             f"연도:{lunar_year} / 월:{lunar_month} / 일: {lunar_day} / 윤달인가 : {is_leap_month}"
#         )

#     year_pillar = get_year_pillar(lunar_year)
#     year_stem = year_pillar[:1]  # 천간의 첫 글자만 추출
#     print(f"디버그 - year_pillar: {year_pillar}, year_stem: {year_stem}")

#     # 월주 및 월주의 기준 날짜 계산
#     month_pillar, base_month_date = get_month_pillar(year_stem, lunar_year, lunar_month)
#     print(f"월주: {month_pillar}, 월 기준일: {base_month_date}")

#     day_pillar = get_day_pillar(base_month_date, birth_date)
#     day_stem = day_pillar[:4]

#     # 시주 계산 시 birth_minute도 전달
#     time_pillar = get_time_pillar(day_stem, birth_hour, birth_minute)

#     result = f"시주 : {time_pillar}, 일주 : {day_pillar}, 월주 : {month_pillar}, 년주 : {year_pillar}"
#     print(result)
#     return result


def main():
    """
    사용자로부터 입력을 받아 사주팔자를 계산하고 출력합니다.
    """
    print("=== 사주팔자 계산기 ===")

    try:
        # birth_hour와 birth_minute 값을 int 형식으로 전달
        sajupalja("1989-08-07", 10, 1, "양력")
    except ValueError as ve:
        print(f"오류: {ve}")


if __name__ == "__main__":
    main()
