# 회의 모델(placeholder).
# TODO:
# - 회의 메타데이터(title, created_at 등) 구조 정의

from __future__ import annotations

from typing import Optional

from models.base import BaseModel


class MeetingModel(BaseModel):
    """회의 메타정보 모델(placeholder)."""

    title: Optional[str] = None

