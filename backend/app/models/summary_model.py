# 요약 결과 모델(placeholder).
# TODO:
# - summary/decisions/action_items 구조 정의

from __future__ import annotations

from typing import Any, Dict, Optional

from models.base import BaseModel


class SummaryModel(BaseModel):
    """요약 결과 모델(placeholder)."""

    summary: Optional[str] = None
    decisions: Optional[list[str]] = None
    action_items: Optional[list[Dict[str, Any]]] = None

