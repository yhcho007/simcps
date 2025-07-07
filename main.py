# main.py
import time
import threading
import subprocess
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ThreadPoolExecutor as APS_ThreadPoolExecutor
from apscheduler.triggers.date import DateTrigger
from apscheduler.jobstores.memory import MemoryJobStore
from datetime import datetime

from batch_utils import get_connection, batch_worker

scheduler = BackgroundScheduler(
    jobstores={'default': MemoryJobStore()},
    executors={'default': APS_ThreadPoolExecutor(100)},
    job_defaults={'coalesce': False, 'max_instances': 5}
)
scheduler.start()


def scheduler_daemon():
    while True:
        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute("""
                SELECT job_id, run_time, params FROM batch_jobs
                WHERE status = 'registered' AND run_time > SYSDATE
            """)
            for job_id, run_time, params in cur.fetchall():
                if not scheduler.get_job(job_id):
                    scheduler.add_job(
                        func=batch_worker,
                        trigger=DateTrigger(run_date=run_time),
                        args=[job_id, params],
                        id=job_id
                    )
                    cur.execute("UPDATE batch_jobs SET status = 'scheduled' WHERE job_id = :1", (job_id,))
            conn.commit()
        finally:
            cur.close()
            conn.close()
        time.sleep(10)


if __name__ == "__main__":
    print("✅ Starting APScheduler Daemon...")

    # 🔧 FastAPI app.py 백그라운드로 실행 (서브프로세스)
    subprocess.Popen(["python", "app.py"])

    # 🧵 Scheduler 데몬 시작
    daemon_thread = threading.Thread(target=scheduler_daemon, daemon=True)
    daemon_thread.start()

    try:
        while True:
            time.sleep(3600)
    except KeyboardInterrupt:
        print("🛑 종료 요청됨. 스케줄러 종료...")
        scheduler.shutdown()
