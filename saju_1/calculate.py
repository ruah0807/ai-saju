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
    stem = heavenly_map[chr(ord('A') + stem_index)]  # A부터 순서대로
    branch = earthly_map[((branch_index + 2) % 12) + 1]  # 인묘진사오미신유술해자축 순서

    return stem, branch

def get_month_pillar(date_str: str, birth_time: str) -> Tuple[str, str]:
    """월주 계산 (절입시간 고려)
    Args:
        date_str (str): YYYYMMDD 형식의 날짜
        birth_time (str): HHMM 형식의 시간
    Returns:
        Tuple[str, str]: (천간, 지지)
    """
    # manseTable에서 해당 날짜 데이터 찾기
    for data in manseTable:
        if str(data['no']) == date_str:
            # 절입시간과 비교
            if int(birth_time) >= int(data['jeolip']):
                month_h = data['month_h']
                month_e = data['month_e']
            else:
                # 이전 데이터의 월주 사용
                prev_idx = manseTable.index(data) - 1
                if prev_idx >= 0:
                    month_h = manseTable[prev_idx]['month_h']
                    month_e = manseTable[prev_idx]['month_e']
                else:
                    month_h = data['month_h']
                    month_e = data['month_e']
                    
            # 천간과 지지로 변환
            stem = heavenly_map[month_h]
            branch = earthly_map[month_e] if isinstance(month_e, int) else earthly_map[int(month_e)]
            
            return stem, branch
            
    raise ValueError(f"Date not found in manseTable: {date_str}")

def get_day_pillar(date_str: str) -> Tuple[str, str]:
    """일주 계산
    Args:
        date_str (str): YYYYMMDD 형식의 날짜
    Returns:
        Tuple[str, str]: (천간, 지지)
    """
    # manseTable에서 해당 날짜 데이터 찾기
    for data in manseTable:
        if str(data['no']) == date_str:
            day_h = data['day_h']
            day_e = data['day_e']
            
            # 천간과 지지로 변환
            stem = heavenly_map[day_h]
            branch = earthly_map[int(day_e)] if day_e.isdigit() else day_e
            
            return stem, branch
            
    raise ValueError(f"Date not found in manseTable: {date_str}")

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
from datetime import datetime
from typing import Tuple, Dict

def get_lunar_date(solar_date: str) -> Dict:
    """양력을 음력으로 변환하고 만세력 데이터 반환
    Args:
        solar_date (str): YYYYMMDD 형식의 양력 날짜
    Returns:
        Dict: 해당 날짜의 만세력 데이터
    """
    solar_int = int(solar_date)
    
    # manseTable에서 해당하는 양력 날짜 찾기
    for data in manseTable:
        if data['no'] == solar_int:
            print(f'양력 data :{data}')
            return data
            
    raise ValueError(f"Date not found in manseTable: {solar_date}")




def get_saju_data_from_solar(solar_date: str) -> dict:
    """만세력 데이터에서 양력 날짜를 기준으로 연주, 월주, 일주, 시주 데이터를 검색합니다."""
    first_date = manseTable[0]['no']
    last_date = manseTable[-1]['no']
    print(f"만세력 데이터 범위: {first_date} ~ {last_date}")
    
    # 정확히 일치하는 날짜 검색
    for data in manseTable:
        if data['no'] == int(solar_date):
            return data
    
    # 일치하는 날짜가 없을 경우 가장 가까운 이전 날짜 찾기
    closest_data = None
    for data in reversed(manseTable):  # 최신 날짜부터 거꾸로 검색
        if data['no'] < int(solar_date):
            closest_data = data
            break

    if closest_data:
        print(f"가장 가까운 이전 날짜 사용: {closest_data['no']}")
        return closest_data
    
    # 범위 내에서도 찾을 수 없는 경우
    raise ValueError(f"만세력 데이터에서 {solar_date}을(를) 찾을 수 없습니다. "
                     f"데이터 범위는 {first_date}부터 {last_date}까지입니다.")



def calculate_saju(year: int, month: int, day: int, 
                  hour: int, minute: int, 
                  is_solar: bool = True, 
                  is_leap_month: bool = False) -> list[str]:
    """사주 계산 메인 함수"""
    print(f"\n=== 사주 계산 시작 ===")
    print(f"입력: {year}년 {month}월 {day}일 {hour}시 {minute}분")
    print(f"양/음력: {'양력' if is_solar else '음력'}")
    print(f"윤달여부: {'윤달' if is_leap_month else '평달'}")
    
    # 날짜 문자열/정수 생성
    date_str = f"{year:04d}{month:02d}{day:02d}"
    birth_time = f"{hour:02d}{minute:02d}"
    try:
        if is_solar:
            # 양력으로 받은 경우
            solar_date = int(f"{year:04d}{month:02d}{day:02d}")
            manse_data = None
            for data in manseTable:
                if data['no'] == solar_date:
                    manse_data = data
                    break
            if not manse_data:
                raise ValueError(f"Solar date not found: {solar_date}")
        else:
            print(f"\n음력 날짜 검색 시작")
            solar_date = convert_lunar_to_solar(year, month, day, is_leap_month)
            manse_data = get_saju_data_from_solar(solar_date)
            print("변환된 만세력 데이터:", manse_data)


        # 2. 각 주 계산
        year_stem = heavenly_map[manse_data['year_h']]
        year_branch = earthly_map[int(manse_data['year_e'])]
        
        # 월주 계산 (절입시간 고려)
        if int(birth_time) >= int(manse_data['jeolip']):
            month_stem = heavenly_map[manse_data['month_h']]
            month_branch = earthly_map[manse_data['month_e']]
        else:
            # 이전 데이터 찾기
            idx = manseTable.index(manse_data)
            if idx > 0:
                prev_data = manseTable[idx - 1]
                month_stem = heavenly_map[prev_data['month_h']]
                month_branch = earthly_map[prev_data['month_e']]
            else:
                month_stem = heavenly_map[manse_data['month_h']]
                month_branch = earthly_map[manse_data['month_e']]
        
        # 일주 계산
        day_stem = heavenly_map[manse_data['day_h']]
        day_branch = earthly_map[int(manse_data['day_e'])]
        
        # 시주 계산
        hour_branch = get_hour_branch(hour, minute)
        hour_stem = hour_stem_mapping[day_stem][hour_branch]
        
        return [hour_stem, hour_branch, day_stem, day_branch,
                month_stem, month_branch, year_stem, year_branch]
                
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
    
    for data in manseTable:
        umdate = data['umdate']
        if target - 100 <= umdate <= target + 100:  # 전후 1개월
            print(f"음력: {data['umdate']}, "
                  f"양력: {data['no']}, "
                  f"윤달: {data['youn']}")


def main():
    print("\n=== 만세력 데이터 정보 ===")
    print(f"전체 데이터 수: {len(manseTable)}")
    print("\n만세력 데이터 범위:")
    print(f"양력: {manseTable[0]['no']} ~ {manseTable[-1]['no']}")
    print(f"음력: {manseTable[0]['umdate']} ~ {manseTable[-1]['umdate']}")
    
    # 2023년 11월 주변 데이터 출력
    print_lunar_dates_around(2023, 11)
    
    # 테스트할 날짜들
    test_cases = [
        # 양력 테스트
        {
            "year": 1989, "month": 8, "day": 7,
            "hour": 10, "minute": 17,
            "is_solar": True
        },
        # 음력 테스트
        {
            "year": 1960, "month": 3, "day": 26,
            "hour": 0, "minute": 0,
            "is_solar": False
        }
    ]
    
    for case in test_cases:
        try:
            print(f"\n테스트 케이스: {case}")
            result = calculate_saju(**case)
            print("사주팔자: " + "".join(result))
        except ValueError as e:
            print(f"에러 발생: {e}")

if __name__ == "__main__":
    main()