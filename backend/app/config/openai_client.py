# OpenAI 클라이언트 구성(placeholder).
# ⚠️ 이 파일에서는 실제 비즈니스 로직을 구현하지 않습니다.
# TODO:
# - OpenAI 클라이언트 생성/재사용 정책 정의
# - settings.py와 연결하여 api_key/model 관리

from __future__ import annotations

from typing import Optional

from openai import OpenAI


def get_openai_client(api_key: Optional[str] = None) -> OpenAI:
    """OpenAI 클라이언트를 반환합니다(placeholder)."""
    # TODO: 설정 로딩과 결합하여 생성/캐싱 전략 구현
    if api_key is None:
        return OpenAI()
    return OpenAI(api_key=api_key)

