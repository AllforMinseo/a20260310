# 업로드 서비스(placeholder).
# ⚠️ 파일 저장 구현은 최소 시그니처만. 실제 저장/정책은 storage/에서 확장 예정.
#
# TODO:
# - storage/file_manager.py와 결합하여 업로드 처리 흐름 구현

from __future__ import annotations

from typing import Optional


def handle_upload(file_bytes: bytes, filename: Optional[str] = None) -> str:
    """업로드된 파일을 처리하고 저장 위치/식별자를 반환(placeholder)."""
    raise NotImplementedError("TODO: 업로드 정책 확정 후 구현 예정")

