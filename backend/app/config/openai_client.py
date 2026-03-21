# OpenAI 클라이언트 구성(placeholder).
# ⚠️ 이 파일에서는 실제 비즈니스 로직을 구현하지 않습니다.
# TODO:
# - OpenAI 클라이언트 생성/재사용 정책 정의
# - settings.py와 연결하여 api_key/model 관리

from __future__ import annotations

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config.settings import settings


# -----------------------------------------
# Database URL 생성
# -----------------------------------------
# 형식:
# mysql+pymysql://유저:비밀번호@호스트:포트/DB이름
DATABASE_URL = (
    f"mysql+pymysql://"
    f"{settings.db_user}:"
    f"{settings.db_password}@"
    f"{settings.db_host}:"
    f"{settings.db_port}/"
    f"{settings.db_name}"
)


# -----------------------------------------
# SQLAlchemy Engine 생성
# -----------------------------------------
# pool_pre_ping=True:
# 오래된 연결이 끊어진 경우 자동으로 상태를 점검하고 재연결 시도
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
)


# -----------------------------------------
# Session Factory 생성
# -----------------------------------------
# autocommit=False:
# 명시적으로 commit() 해야 반영
#
# autoflush=False:
# 자동 flush 비활성화
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def get_db():
    """
    FastAPI Dependency용 DB 세션 생성기

    요청마다 DB 세션을 만들고,
    요청이 끝나면 세션을 닫는다.
    """

    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()