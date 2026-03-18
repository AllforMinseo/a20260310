from __future__ import annotations

# 요약 서비스.
# - LLM 요약 오케스트레이션(services/meeting_summarizer.py)을 호출하고
# - 결과를 그대로 반환하는 얇은 서비스 레이어입니다.

from typing import Any, Dict

from app.ai.meeting_summarizer import summarize_meeting_from_text


def summarize_meeting_text(stt_text: str, ocr_text: str, title: str = "") -> Dict[str, Any]:
    """
    meeting_summarizer.summarize_meeting을 호출하고 결과(dict)를 반환합니다.
    """
    return summarize_meeting_from_text(stt_text=stt_text, ocr_text=ocr_text, title=title)
