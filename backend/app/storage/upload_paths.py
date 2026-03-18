# 업로드 경로 규칙(placeholder).
# TODO:
# - 업로드 기본 디렉토리, 회의별 디렉토리 구조, 임시 폴더 정책 정의

from __future__ import annotations


def get_upload_root() -> str:
    """업로드 루트 경로(placeholder)."""
    return "uploads"


def get_meeting_upload_dir(meeting_id: str) -> str:
    """회의별 업로드 디렉토리 경로(placeholder)."""
    return f"uploads/{meeting_id}"

