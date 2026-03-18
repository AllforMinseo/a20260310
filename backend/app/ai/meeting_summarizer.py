from __future__ import annotations

# 회의 요약 LLM 엔진.
# STT/OCR 텍스트를 입력받아 OpenAI API를 통해
# summary / decisions / action_items 를 JSON(dict)으로 반환합니다.
#
# ⚠️ 서버 프레임워크, DB 연결, Whisper/OCR 실제 호출은 금지 범위입니다.

import json
import logging
import os
from typing import Any, Dict, Sequence

from openai import OpenAI

from app.utils.preprocess import stt_json_to_text

logger = logging.getLogger(__name__)

try:
    # .env 자동 로딩(선택). 없거나 미설치여도 동작하도록 처리합니다.
    from dotenv import load_dotenv  # type: ignore

    load_dotenv()
except Exception:
    pass


def _build_prompt(stt_text: str, ocr_text: str, title: str = "") -> str:
    stt_text = (stt_text or "").strip()
    ocr_text = (ocr_text or "").strip()
    title = (title or "").strip()

    return (
        "당신은 회의 내용을 구조화하는 분석가입니다.\n"
        "다음 입력(STT 발언 + OCR 메모)을 근거로 회의 결과를 추출하세요.\n"
        "\n"
        "규칙:\n"
        "- 출력은 오직 유효한 JSON만 허용합니다(마크다운/설명/코드펜스 금지).\n"
        "- 입력에 명시적으로 없는 내용은 절대 추측하거나 추가하지 마세요.\n"
        "- 알 수 없는 값은 빈 문자열 \"\" 또는 빈 리스트 []로 두세요.\n"
        "\n"
        "반환 JSON 형식:\n"
        "{\n"
        '  \"summary\": \"...\",\n'
        '  \"decisions\": [\"...\"],\n'
        '  \"action_items\": [\n'
        "    { \"task\": \"...\", \"owner\": \"...\", \"deadline\": \"...\" }\n"
        "  ]\n"
        "}\n"
        "\n"
        f"회의 제목: {title or '(없음)'}\n"
        "\n"
        "STT:\n"
        f"{stt_text}\n"
        "\n"
        "OCR:\n"
        f"{ocr_text}\n"
    )


def _extract_json_text(raw: str) -> str:
    raw = (raw or "").strip()
    if raw.startswith("{") and raw.endswith("}"):
        return raw
    start = raw.find("{")
    end = raw.rfind("}")
    if start != -1 and end != -1 and end > start:
        return raw[start : end + 1]
    return raw


def summarize_meeting_from_text(stt_text: str, ocr_text: str, title: str = "") -> Dict[str, Any]:
    """
    전처리된 STT 텍스트 + OCR 기반 회의 요약을 수행하고 JSON(dict) 결과를 반환합니다.

    - meeting_service에서 STT(JSON 세그먼트 배열)를 전처리한 뒤 이 함수에 넘기는 용도입니다.
    - 여기서는 전처리를 다시 하지 않습니다(중복 방지).
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("환경변수 OPENAI_API_KEY가 설정되어 있지 않습니다.")

    model = os.getenv("OPENAI_MODEL") or "gpt-4o-mini"
    prompt = _build_prompt(stt_text=stt_text, ocr_text=ocr_text, title=title)

    client = OpenAI(api_key=api_key)

    try:
        resp = client.chat.completions.create(
            model=model,
            temperature=0.2,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": "반드시 유효한 JSON만 반환하세요."},
                {"role": "user", "content": prompt},
            ],
        )
        content = (resp.choices[0].message.content or "").strip()
    except Exception as e:
        logger.exception("OpenAI API 호출 실패")
        raise RuntimeError(f"OpenAI API 호출에 실패했습니다: {e}") from e

    if not content:
        raise RuntimeError("OpenAI API가 빈 응답을 반환했습니다.")

    try:
        parsed = json.loads(_extract_json_text(content))
    except json.JSONDecodeError as e:
        raise RuntimeError(
            "모델 출력(JSON)을 파싱하지 못했습니다. "
            f"에러: {e}. 원본 출력(앞부분): {content[:5000]}"
        ) from e

    if not isinstance(parsed, dict):
        raise RuntimeError("모델 JSON의 최상위는 객체(dict)여야 합니다.")

    return parsed


def summarize_meeting(stt_segments: Sequence[Any], ocr_text: str, title: str = "") -> Dict[str, Any]:
    """
    STT(JSON 세그먼트 배열) + OCR 기반 회의 요약을 수행하고 JSON(dict) 결과를 반환합니다.

    환경변수:
    - OPENAI_API_KEY: 필수
    - OPENAI_MODEL: 선택(기본값: gpt-4o-mini)
    """
    stt_text = stt_json_to_text(stt_segments)

    return summarize_meeting_from_text(stt_text=stt_text, ocr_text=ocr_text, title=title)

