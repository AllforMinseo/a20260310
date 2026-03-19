from __future__ import annotations

# 회의 처리 오케스트레이션 서비스.
# 전체 흐름:
# 1) STT(JSON 세그먼트 배열) 입력 받음
# 2) utils/processor.py에서 텍스트 전처리(요약/재작성 없이 정리만)
# 3) OCR 텍스트 결합
# 4) LLM 요약 호출
# 5) 결과 반환
#
# ⚠️ FastAPI/DB/Whisper/OCR 실제 호출은 금지 범위입니다.

from typing import Any, Dict

from app.services.summary_service import summarize_meeting_text
from utils.preprocess import stt_json_to_text


def process_meeting_text(stt_raw: Any, ocr_text: str, title: str) -> Dict[str, Any]:
    """
    프레임워크 독립 파이프라인 엔트리 함수.

    예:
    result = process_meeting_text(
        stt_raw=[
            {"start": 0.0, "end": 1.0, "text": "검색 속도가 느립니다"},
        ],
        ocr_text="회의 주제: 검색 개선",
        title="회의"
    )
    """
    stt_raw = stt_raw or []
    ocr_text = (ocr_text or "").strip()
    title = title or ""

    # 1) STT(JSON 세그먼트 배열) → 사람이 읽을 수 있는 텍스트로 전처리
    stt_text = stt_json_to_text(stt_raw)

    # 2) LLM 호출(전처리 텍스트를 그대로 전달)
    llm_result = summarize_meeting_text(stt_text=stt_text, ocr_text=ocr_text, title=title)

    return {
        "title": title,
        "stt_text": stt_text,
        "summary": llm_result.get("summary", ""),
        "decisions": llm_result.get("decisions", []),
        "action_items": llm_result.get("action_items", []),
    }

