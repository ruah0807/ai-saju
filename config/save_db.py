import os, sys

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import pandas as pd
from init import engine

mansae_data = "/Users/ruahkim/coding/ai-saju/.docs/mansae.xlsx"

df = pd.read_excel(mansae_data)

# 데이터 프레임을 mysql 데이터 베이스에 저장
df.to_sql("mansae", con=engine, index=True, if_exists="replace")

print("엑셀 데이터베이스 저장완료")
