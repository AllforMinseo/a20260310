# 업로드 관련 라우터(placeholder).
# ⚠️ FastAPI 구현 금지. 여기서는 라우팅 시그니처/구조만 잡아둡니다.
#
# TODO:
# - 추후 프레임워크 확정 시, upload_service와 연결

from __future__ import annotations

from typing import Any, Dict


def upload_endpoint(payload: Dict[str, Any]) -> Dict[str, Any]:
    """파일 업로드 API 엔드포인트(placeholder)."""
    raise NotImplementedError("TODO: 프레임워크 확정 후 구현 예정")

