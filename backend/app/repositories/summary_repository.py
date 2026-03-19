# 요약 결과 저장소(placeholder).
# ⚠️ DB 실제 연결은 금지 범위입니다.
#
# TODO:
# - SummaryModel 저장/조회 인터페이스 정의

from __future__ import annotations

from typing import Optional

from models.summary_model import SummaryModel


class SummaryRepository:
    """요약 저장소 인터페이스(placeholder)."""

    def save(self, summary: SummaryModel) -> None:
        raise NotImplementedError("TODO: DB 연동 후 구현 예정")

    def get_by_id(self, summary_id: str) -> Optional[SummaryModel]:
        raise NotImplementedError("TODO: DB 연동 후 구현 예정")

