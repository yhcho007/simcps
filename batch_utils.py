# batch_utils.py
import time
from datetime import datetime
import oracledb

def get_connection():
    return oracledb.connect(user="your_user", password="your_pw", dsn="your_dsn")

def batch_worker(job_id: str, params: str):
    print(f"[{datetime.now()}] #🔧 실행중: Job ID: {job_id}, Params: {params}")
    time.sleep(2)
    print(f"[{datetime.now()}] # ✅ 완료: Job ID: {job_id}")
