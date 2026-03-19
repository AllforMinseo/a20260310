# 데이터베이스 설정/연결(placeholder).
# ⚠️ DB 실제 연결은 금지 범위입니다.
#
# TODO:
# - DB URL/자격증명/연결 풀 설정 구조 정의
# - repository 계층과 연결되는 인터페이스 설계

from __future__ import annotations

from typing import Generator, Optional

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from config.settings import Settings


def build_database_url(
    *,
    db_user: str,
    db_password: str,
    db_host: str,
    db_port: int,
    db_name: str,
    driver: str = "mysql+pymysql",
) -> str:
    """
    데이터베이스 연결 URL 생성

    Parameters
    ----------
    db_user : str
        DB 사용자명

    db_password : str
        DB 비밀번호

    db_host : str
        DB 호스트

    db_port : int
        DB 포트

    db_name : str
        DB 이름

    driver : str
        SQLAlchemy 드라이버 문자열
    """

    return (
        f"{driver}://"
        f"{db_user}:"
        f"{db_password}@"
        f"{db_host}:"
        f"{db_port}/"
        f"{db_name}"
    )


def build_database_url_from_settings(settings: Settings) -> str:
    """
    Settings 객체로부터 DB URL 생성

    Parameters
    ----------
    settings : Settings
        설정 객체
    """

    if not settings.db_user:
        raise ValueError("DB_USER 설정이 없습니다.")

    if not settings.db_password:
        raise ValueError("DB_PASSWORD 설정이 없습니다.")

    if not settings.db_host:
        raise ValueError("DB_HOST 설정이 없습니다.")

    if not settings.db_name:
        raise ValueError("DB_NAME 설정이 없습니다.")

    return build_database_url(
        db_user=settings.db_user,
        db_password=settings.db_password,
        db_host=settings.db_host,
        db_port=settings.db_port,
        db_name=settings.db_name,
    )


def create_db_engine(
    database_url: str,
    *,
    pool_pre_ping: bool = True,
    echo: bool = False,
) -> Engine:
    """
    SQLAlchemy engine 생성

    Parameters
    ----------
    database_url : str
        DB 연결 URL

    pool_pre_ping : bool
        연결 상태 확인 여부

    echo : bool
        SQL 로그 출력 여부
    """

    return create_engine(
        database_url,
        pool_pre_ping=pool_pre_ping,
        echo=echo,
    )


def create_session_factory(engine: Engine) -> sessionmaker:
    """
    sessionmaker 생성

    Parameters
    ----------
    engine : Engine
        SQLAlchemy engine
    """

    return sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine,
    )


def create_get_db(session_factory: sessionmaker):
    """
    FastAPI Depends용 get_db 함수 생성

    Parameters
    ----------
    session_factory : sessionmaker
        SessionLocal 객체
    """

    def get_db() -> Generator[Session, None, None]:
        db = session_factory()
        try:
            yield db
        finally:
            db.close()

    return get_db

