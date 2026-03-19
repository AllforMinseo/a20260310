# 설정 관리(placeholder).
# TODO:
# - 환경변수 로딩 및 검증(OPENAI_API_KEY, OPENAI_MODEL 등)
# - python-dotenv/pydantic-settings 도입 검토
from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Optional

from dotenv import load_dotenv


# 프로젝트 루트의 .env 파일 자동 로딩
load_dotenv()


@dataclass(frozen=True)
class Settings:
    """애플리케이션 설정 데이터 객체"""

    # OpenAI
    openai_api_key: Optional[str] = None
    openai_model: Optional[str] = None

    # MySQL
    db_user: Optional[str] = None
    db_password: Optional[str] = None
    db_host: Optional[str] = None
    db_port: int = 3306
    db_name: Optional[str] = None

    # Google STT
    google_application_credentials: Optional[str] = None

    # 파일 저장 경로
    upload_dir: str = "uploads"
    audio_dir: str = "audio"
    image_dir: str = "images"


def get_env(
    key: str,
    default: Optional[str] = None,
    *,
    required: bool = False,
) -> Optional[str]:
    """
    환경변수를 읽는 유틸리티 함수

    Parameters
    ----------
    key : str
        환경변수 이름

    default : Optional[str]
        기본값

    required : bool
        필수 여부
    """

    value = os.getenv(key, default)

    if required and not value:
        raise ValueError(f"{key} 환경변수가 설정되지 않았습니다.")

    return value


def load_settings() -> Settings:
    """
    환경변수에서 Settings 객체 생성

    Returns
    -------
    Settings
        로딩된 설정 객체
    """

    return Settings(
        # OpenAI
        openai_api_key=get_env("OPENAI_API_KEY"),
        openai_model=get_env("OPENAI_MODEL", "gpt-4o"),

        # MySQL
        db_user=get_env("DB_USER"),
        db_password=get_env("DB_PASSWORD"),
        db_host=get_env("DB_HOST", "localhost"),
        db_port=int(get_env("DB_PORT", "3306") or "3306"),
        db_name=get_env("DB_NAME"),

        # Google STT
        google_application_credentials=get_env("GOOGLE_APPLICATION_CREDENTIALS"),

        # Storage
        upload_dir=get_env("UPLOAD_DIR", "uploads") or "uploads",
        audio_dir=get_env("AUDIO_DIR", "audio") or "audio",
        image_dir=get_env("IMAGE_DIR", "images") or "images",
    )