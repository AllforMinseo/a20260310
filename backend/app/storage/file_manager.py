# 파일 관리 유틸(placeholder).
# TODO:
# - 파일 저장/삭제/조회 인터페이스 정의
# - 파일명 충돌 방지 및 보안(확장자/크기 제한) 정책 수립

from __future__ import annotations


def save_file(data: bytes, path: str) -> None:
    """파일 저장(placeholder)."""
    raise NotImplementedError("TODO: 파일 저장 정책 확정 후 구현 예정")


def delete_file(path: str) -> None:
    """파일 삭제(placeholder)."""
    raise NotImplementedError("TODO: 파일 삭제 정책 확정 후 구현 예정")

