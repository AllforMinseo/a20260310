# 전사(Transcript) 저장소(placeholder).
# ⚠️ DB 실제 연결은 금지 범위입니다.
#
# TODO:
# - TranscriptModel 저장/조회 인터페이스 정의

from __future__ import annotations

from typing import Optional

from models.transcript_model import TranscriptModel


class TranscriptRepository:
    """전사 저장소 인터페이스(placeholder)."""

    def save(self, transcript: TranscriptModel) -> None:
        raise NotImplementedError("TODO: DB 연동 후 구현 예정")

    def get_by_id(self, transcript_id: str) -> Optional[TranscriptModel]:
        raise NotImplementedError("TODO: DB 연동 후 구현 예정")

