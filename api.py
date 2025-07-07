# app.py
from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
import oracledb

import uvicorn
from batch_utils import get_connection

app = FastAPI()

class BatchJobRequest(BaseModel):
    job_id: str
    run_time: datetime
    params: str

@app.post("/jobs/")
def register_job(job: BatchJobRequest):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            INSERT INTO batch_jobs (job_id, run_time, params, status)
            VALUES (:1, :2, :3, 'registered')
        """, (job.job_id, job.run_time, job.params))
        conn.commit()
    finally:
        cur.close()
        conn.close()
    return {"message": "Job registered"}

@app.get("/jobs/")
def list_jobs():
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT job_id, run_time, params, status FROM batch_jobs")
        rows = cur.fetchall()
        return [{"job_id": r[0], "run_time": r[1], "params": r[2], "status": r[3]} for r in rows]
    finally:
        cur.close()
        conn.close()

@app.delete("/jobs/{job_id}")
def delete_job(job_id: str):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM batch_jobs WHERE job_id = :1", (job_id,))
        conn.commit()
    finally:
        cur.close()
        conn.close()
    return {"message": f"Job {job_id} deleted"}

if __name__ == "__main__":
    # ✅ 여기서 uvicorn을 직접 실행
    uvicorn.run("app:app", host="0.0.0.0", port=8000, workers=1)
