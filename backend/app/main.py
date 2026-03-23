"""
main.py

애플리케이션 실행 진입점

역할
- FastAPI 앱 생성
- 라우터 등록
- DB 테이블 생성
- 기본 헬스체크 엔드포인트 제공

실행 예시
---------
uvicorn main:app --reload
"""

from __future__ import annotations

from fastapi import FastAPI

from config.database import engine
from models import Base
from routers import meeting_router, upload_router


# -----------------------------------------
# DB 테이블 생성
# -----------------------------------------
# 앱 시작 시 SQLAlchemy Base에 등록된 모든 테이블을 생성합니다.
# 이미 존재하는 테이블은 다시 생성하지 않습니다.
Base.metadata.create_all(bind=engine)


# -----------------------------------------
# FastAPI 앱 생성
# -----------------------------------------
app = FastAPI(
    title="MOA Meeting Assistant API",
    description="회의 오디오/이미지 업로드, transcript 저장, summary 생성 API",
    version="1.0.0",
)


# -----------------------------------------
# 기본 엔드포인트
# -----------------------------------------
@app.get("/", summary="루트 엔드포인트")
def read_root() -> dict:
    """
    기본 루트 엔드포인트

    서버가 실행 중인지 간단히 확인할 때 사용합니다.
    """

    return {
        "message": "MOA Meeting Assistant API is running."
    }


@app.get("/health", summary="헬스 체크")
def health_check() -> dict:
    """
    서버 상태 확인용 엔드포인트
    """

    return {
        "status": "ok"
    }


# -----------------------------------------
# 라우터 등록
# -----------------------------------------
app.include_router(meeting_router.router)
app.include_router(upload_router.router)

