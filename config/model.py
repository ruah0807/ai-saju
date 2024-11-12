from sqlalchemy import (
    TEXT,
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    Enum,
    Float,
    JSON,
    UniqueConstraint,
)

# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime
import pytz

# 한국 시간대 설정
KST = pytz.timezone("Asia/Seoul")


def current_time():
    return datetime.now(KST)


Base = declarative_base()


class mansae(Base):
    __tablename__ = "mansae"
    __table_args__ = {"comment": "만세력 데이터"}

    id = Column(Integer, primary_key=True, comment="유저 ID")
    email = Column(String(255), nullable=False, unique=True, comment="이메일")
    password = Column(String(255), nullable=False, comment="비밀번호")
    name = Column(String(255), nullable=False, comment="이름")
    created_at = Column(
        DateTime, default=current_time, nullable=False, comment="생성 일시"
    )
    updated_at = Column(
        DateTime,
        default=current_time,
        onupdate=current_time,
        nullable=False,
        comment="수정 일시",
    )
    tokens = relationship(
        "UserToken", back_populates="user", cascade="all, delete-orphan"
    )
    social_accounts = relationship(
        "UserSocialAccount", back_populates="user", cascade="all, delete-orphan"
    )
    meal_plans = relationship(
        "MealPlan", back_populates="user", cascade="all, delete-orphan"
    )
