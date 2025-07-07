# batch_app.py

## 주요 기능

OracleDB 연동

APScheduler로 등록시간에 맞춰 배치 작업 스케줄링

ThreadPoolExecutor로 병렬 배치 처리

job_defaults의 max_instances 설정 적용

FastAPI와 Scheduler가 서로 영향을 주지 않도록 설계

## Oracle 테이블 생성 예시
```SQL
CREATE TABLE batch_jobs (
    job_id VARCHAR2(100) PRIMARY KEY,
    run_time TIMESTAMP,
    params VARCHAR2(4000),
    status VARCHAR2(50)
);
```
| 요소                   | 설명                                          |
| -------------------- | ------------------------------------------- |
| `APScheduler`        | `BackgroundScheduler` 사용, FastAPI와 충돌 없이 동작 |
| `ThreadPoolExecutor` | 최대 동시 100개까지 처리 가능                          |
| `max_instances`      | 동일 job에 대한 동시 실행 제한                         |
| `daemon thread`      | 10초마다 등록된 작업을 확인하고 scheduler에 추가            |
| `OracleDB`           | 작업 등록/조회/삭제 상태를 테이블에 저장                     |
| `FastAPI`            | REST API로 작업 등록, 조회, 삭제 제공                  |



