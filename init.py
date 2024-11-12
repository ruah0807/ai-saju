import os
from openai import OpenAI
from dotenv import load_dotenv
import streamlit as st
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

api_key = os.environ.get("OPENAI_API_KEY")
# api_key = st.secrets["OPENAI_API_KEY"]
# Open ai API를 사용하기 위한 클라이언트 객체생성
client = OpenAI(api_key=api_key)

# 한국 시간대 설정
engine = create_engine(os.getenv("MYSQL_DATABASE_URL"))
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
