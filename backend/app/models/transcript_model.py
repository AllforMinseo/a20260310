# STT 전사(Transcript) 모델(placeholder).
# TODO:
# - 원문 STT / 정제 STT 저장 구조 정의

from __future__ import annotations

from typing import Optional

from models.base import BaseModel


class TranscriptModel(BaseModel):
    """전사 텍스트 모델(placeholder)."""

    raw_text: Optional[str] = None
    cleaned_text: Optional[str] = None

