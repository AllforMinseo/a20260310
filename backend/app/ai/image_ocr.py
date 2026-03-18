# 이미지 OCR 모듈(placeholder).
# ⚠️ OCR 라이브러리/엔진 실제 연결은 금지 범위입니다.
#
# TODO:
# - 이미지 입력(file path/bytes) 받아 OCR 텍스트로 변환하는 시그니처 확정
# - 엔진 선택(Tesseract, 클라우드 OCR 등) 및 전처리 전략 수립

from __future__ import annotations

from typing import Optional


def extract_text_from_image(image_path: Optional[str] = None, image_bytes: Optional[bytes] = None) -> str:
    """
    이미지에서 OCR 텍스트를 추출합니다(placeholder).

    TODO: OCR 엔진 연동 후 구현
    """
    raise NotImplementedError("TODO: OCR 엔진 연동 후 구현 예정")

