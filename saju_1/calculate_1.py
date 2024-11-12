import os, sys

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from datetime import datetime
from typing import Dict, Generator
from sqlalchemy import text
from sqlalchemy.orm import Session
from saju_1.data import *
from init import get_db


def sajupalja(
    birth_date_str: str, birth_hour: int, birth_minute: int, is_lunar_str: str
) -> str:
    """
    사주팔자 계산 메인 함수

    Args:
        db: SQLAlchemy 데이터베이스 세션 제너레이터
        birth_date: YYYY-MM-DD 형식의 생년월일
        birth_hour: 태어난 시 (0-23)
        birth_minute: 태어난 분 (0-59)
        is_lunar: 음력 여부

    Returns:
        Dict: 사주팔자 결과 {"year_ganji", "month_ganji", "day_ganji", "time_ganji"}

    Raises:
        ValueError: 날짜 데이터가 없거나 계산 중 오류 발생시
    """
    try:
        # DB 세션 얻기
        db_session = next(get_db())

        # 음력/양력 변환
        is_lunar = is_lunar_str == "음력"

        # 날짜 검증 및 변환
        try:
            date_obj = datetime.strptime(birth_date_str, "%Y-%m-%d")
            if date_obj.strftime("%Y-%m-%d 00:00:00"):
                formatted_date = date_obj.strftime("%Y-%m-%d 00:00:00")
            else:
                formatted_date = date_obj.strftime("%Y-%m-%d")
        except ValueError:
            raise ValueError("올바른 날짜 형식이 아닙니다 (YYYY-MM-DD)")

        # 시간 검증
        if not (0 <= birth_hour <= 23 and 0 <= birth_minute <= 59):
            raise ValueError("올바른 시간이 아닙니다")

        # 데이터베이스 쿼리
        query = text(
            """
            SELECT lunaGanJi, solarGanJi
            FROM mansae
            WHERE {} = :date
            """.format(
                "lunaDate" if is_lunar else "solarDate"
            )
        )

        result = db_session.execute(query, {"date": formatted_date}).first()
        if not result:
            raise ValueError(f"해당 날짜의 데이터를 찾을 수 없습니다: {formatted_date}")

        # 간지 정보 파싱
        ganji = result.lunaGanJi if is_lunar else result.solarGanJi
        year_pillar = ganji.split("年")[0]
        month_pillar = ganji.split("月")[0].split("年")[1].strip()
        day_pillar = ganji.split("日")[0].split("月")[1].strip()

        # 시주 계산
        time_pillar = get_time_pillar(birth_hour, birth_minute, day_pillar[0])

        # 결과 조합
        result = f"시주: {time_pillar}, 일주: {day_pillar}, 월주: {month_pillar}, 연주: {year_pillar}"
        return result

    except Exception as e:
        raise ValueError(f"사주 계산 중 오류 발생: {str(e)}")


def get_time_pillar(hour: int, minute: int, day_stem: str) -> str:
    """
    시주 계산

    Args:
        hour: 시 (0-23)
        minute: 분 (0-59)
        day_stem: 일간(일주의 천간)
    Returns:
        str: 시주 (천간과 지지)
    """
    total_minutes = hour * 60 + minute

    # 23:30 이후는 다음날 子시
    if hour == 23 and minute >= 30:
        branch = "子"
    else:
        for break_hour, break_minute, current_branch in time_breaks:
            if total_minutes < (break_hour * 60 + break_minute):
                branch = current_branch
                break
        else:
            branch = "子"

    stem = hour_stem_mapping[day_stem][branch]
    return f"{stem}{branch}"


if __name__ == "__main__":
    try:
        result = sajupalja(
            birth_date_str="1989-08-07",
            birth_hour=10,
            birth_minute=17,
            is_lunar_str="양력",
        )

        print(result)
    except ValueError as e:
        print(f"오류: {e}")
