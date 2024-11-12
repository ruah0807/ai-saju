import os
from sqlalchemy import (
    create_engine,
)

# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from dotenv import load_dotenv

# .env 파일에서 환경 변수 로드
load_dotenv()

# 한국 시간대 설정
engine = create_engine(os.getenv("MYSQL_DATABASE_URL"))
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


get_db()
# Base.metadata.drop_all(bind=engine)
# Base.metadata.create_all(bind=engine)
