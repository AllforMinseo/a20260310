# 설정 관리(placeholder).
# TODO:
# - 환경변수 로딩 및 검증(OPENAI_API_KEY, OPENAI_MODEL 등)
# - python-dotenv/pydantic-settings 도입 검토

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Settings:
    """애플리케이션 설정(placeholder)."""

    openai_api_key: Optional[str] = None
    openai_model: Optional[str] = None


def load_settings() -> Settings:
    """환경에서 설정을 읽어 Settings로 반환(placeholder)."""
    # TODO: 실제 환경변수 로딩 구현
    return Settings()

