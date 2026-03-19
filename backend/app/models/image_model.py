# 이미지 모델(placeholder).
# TODO:
# - 업로드된 이미지의 메타데이터(파일명/경로/크기/해시 등) 구조 정의

from __future__ import annotations

from typing import Optional

from models.base import BaseModel


class ImageModel(BaseModel):
    """이미지 메타데이터 모델(placeholder)."""

    path: Optional[str] = None

