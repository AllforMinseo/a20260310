"""PDF에서 텍스트 레이어를 추출합니다. 스캔 전용 PDF는 보통 빈 문자열이 됩니다."""

from __future__ import annotations

import os


def extract_pdf_plain_text(file_path: str, max_pages: int = 40) -> str:
    if not os.path.exists(file_path):
        raise FileNotFoundError(file_path)

    from pypdf import PdfReader

    reader = PdfReader(file_path)
    parts: list[str] = []
    for i, page in enumerate(reader.pages):
        if i >= max_pages:
            break
        raw = page.extract_text()
        if raw and raw.strip():
            parts.append(raw.strip())
    return "\n\n".join(parts)
