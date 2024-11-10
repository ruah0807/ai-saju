import os, sys

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from saju_1.data from *


# 시간대 설정 함수
def determine_time_range(hour, minute):
    if (hour == 23 and minute >= 30) or (hour == 0 and minute < 30):
        return "2330~0130"
    elif (hour == 1 and minute >= 30) or (hour == 2 and minute < 30):
        return "0130~0330"
    elif (hour == 3 and minute >= 30) or (hour == 4 and minute < 30):
        return "0330~0530"
    elif (hour == 5 and minute >= 30) or (hour == 6 and minute < 30):
        return "0530~0730"
    elif (hour == 7 and minute >= 30) or (hour == 8 and minute < 30):
        return "0730~0930"
    elif (hour == 9 and minute >= 30) or (hour == 10 and minute < 30):
        return "0930~1130"
    elif (hour == 11 and minute >= 30) or (hour == 12 and minute < 30):
        return "1130~1330"
    elif (hour == 13 and minute >= 30) or (hour == 14 and minute < 30):
        return "1330~1530"
    elif (hour == 15 and minute >= 30) or (hour == 16 and minute < 30):
        return "1530~1730"
    elif (hour == 17 and minute >= 30) or (hour == 18 and minute < 30):
        return "1730~1930"
    elif (hour == 19 and minute >= 30) or (hour == 20 and minute < 30):
        return "1930~2130"
    elif (hour == 21 and minute >= 30) or (hour == 22 and minute < 30):
        return "2130~2330"
    else:
        return "모름"


# 시의 지지와 시 천간 계산 함수
def calculate_time_earthly_and_heavenly(day_heavenly, hour, minute):
    # 시간대에 따른 시의 지지와 a8 값 가져오기
    time_range = determine_time_range(hour, minute)
    earthly_branch = table4[time_range]["hanja"]
    a8_value = table4[time_range]["a8"]

    # 시 천간 계산하기 (a8 값과 일 천간을 기반으로 매칭)
    if (a8_value, day_heavenly) in table5:
        heavenly_stem = table5[(a8_value, day_heavenly)]
    else:
        heavenly_stem = "Unknown"  # 데이터에 없는 경우 처리

    return earthly_branch, heavenly_stem

# 예시 실행
day_heavenly = "甲"  # 예시로 일 천간을 설정
hour = 14
minute = 45

earthly_branch, heavenly_stem = calculate_time_earthly_and_heavenly(day_heavenly, hour, minute)
print(f"시의 지지: {earthly_branch}, 시의 천간: {heavenly_stem}")