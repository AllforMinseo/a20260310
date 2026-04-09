"""
meeting_summarizer.py

회의 요약 LLM 엔진

역할
- STT JSON / OCR JSON payload를 입력받아
  OpenAI API를 통해 구조화된 회의 요약 결과를 생성
- 사용자에게는 아래 3가지를 함께 제공
  1) STT 원문 텍스트
  2) OCR 원문 텍스트
  3) STT + OCR을 종합한 회의 요약 결과

반환 예시
---------
{
    "stt_text": "...",
    "ocr_text": "...",
    "summary_result": {
        "summary": "...",
        "decisions": ["..."],
        "action_items": [
            {
                "task": "...",
                "owner": "...",
                "deadline": "..."
            }
        ]
    }
}

특징
- OpenAI 클라이언트는 config/openai_client.py를 사용
- 모델명은 config/settings.py에서 읽음
- STT와 OCR은 따로 사용자에게 전달 가능
- 요약은 STT + OCR을 함께 참고하여 생성
"""

from __future__ import annotations

import json
import logging
from typing import Any, Dict, Sequence

from config.openai_client import get_openai_client
from config.settings import settings
from utils.preprocess import stt_json_to_text

logger = logging.getLogger(__name__)


def _build_prompt(stt_text: str, ocr_text: str, title: str = "") -> str:
    """
    기존 방식:
    전처리된 STT 텍스트 + OCR 텍스트를 LLM에 전달할 프롬프트 생성

    핵심:
    - STT와 OCR을 각각 따로 프롬프트에 넣음
    - 하지만 모델은 이를 따로 반환하지 않고
      하나의 통합 요약 결과를 생성함
    """

    stt_text = (stt_text or "").strip()
    ocr_text = (ocr_text or "").strip()
    title = (title or "").strip()

    return (
        "당신은 회의 내용을 구조화하는 분석가입니다.\n"
        "다음 입력(STT 발언 + OCR 메모)을 근거로 회의 결과를 추출하세요.\n"
        "\n"
        "규칙:\n"
        '- 출력은 오직 유효한 JSON만 허용합니다(마크다운/설명/코드펜스 금지).\n'
        '- 입력에 명시적으로 없는 내용은 절대 추측하거나 추가하지 마세요.\n'
        '- 알 수 없는 값은 빈 문자열 "" 또는 빈 리스트 []로 두세요.\n'
        "\n"
        "반환 JSON 형식:\n"
        "{\n"
        '  "summary": "...",\n'
        '  "decisions": ["..."],\n'
        '  "action_items": [\n'
        '    { "task": "...", "owner": "...", "deadline": "..." }\n'
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


def _build_payload_prompt(payload: Dict[str, Any]) -> str:
    """
    확장 방식:
    STT JSON + OCR JSON + 회의 메타데이터를 하나의 payload로 받아
    LLM에 전달할 프롬프트 생성

    핵심:
    - STT / OCR / 메타데이터를 모두 전달
    - 모델은 이 전체 정보를 종합해서 하나의 요약 결과를 생성
    """

    payload_json = json.dumps(payload, ensure_ascii=False, indent=2)

    return (
        "당신은 회의 내용을 구조화하는 분석가입니다.\n"
        "입력으로 회의 메타데이터, STT JSON, OCR/이미지 분석 JSON이 주어집니다.\n"
        "이 정보를 종합하여 회의 결과를 추출하세요.\n"
        "\n"
        "규칙:\n"
        '- 출력은 오직 유효한 JSON만 허용합니다(마크다운/설명/코드펜스 금지).\n'
        '- 입력에 명시적으로 없는 내용은 절대 추측하거나 추가하지 마세요.\n'
        '- 알 수 없는 값은 빈 문자열 "" 또는 빈 리스트 []로 두세요.\n'
        '- STT 내용과 OCR/이미지 분석 내용을 함께 참고하세요.\n'
        '- OCR/이미지 분석 내용은 회의 맥락 보강용 자료이므로, STT와 충돌하면 더 보수적으로 요약하세요.\n'
        "\n"
        "반환 JSON 형식:\n"
        "{\n"
        '  "summary": "...",\n'
        '  "decisions": ["..."],\n'
        '  "action_items": [\n'
        '    { "task": "...", "owner": "...", "deadline": "..." }\n'
        "  ]\n"
        "}\n"
        "\n"
        "입력 payload(JSON):\n"
        f"{payload_json}\n"
    )


def _extract_json_text(raw: str) -> str:
    """
    모델 응답에서 JSON 본문만 최대한 안전하게 추출
    """

    raw = (raw or "").strip()

    if raw.startswith("{") and raw.endswith("}"):
        return raw

    start = raw.find("{")
    end = raw.rfind("}")

    if start != -1 and end != -1 and end > start:
        return raw[start:end + 1]

    return raw


def _call_llm(prompt: str) -> Dict[str, Any]:
    """
    공통 OpenAI 호출 함수

    Parameters
    ----------
    prompt : str
        LLM에 전달할 최종 프롬프트

    Returns
    -------
    Dict[str, Any]
        구조화된 회의 요약 결과
        예:
        {
            "summary": "...",
            "decisions": [...],
            "action_items": [...]
        }
    """

    if not settings.openai_api_key:
        raise RuntimeError("OPENAI_API_KEY가 설정되지 않았습니다.")

    client = get_openai_client()

    try:
        response = client.chat.completions.create(
            model=settings.openai_model,
            temperature=0.2,
            response_format={"type": "json_object"},
            messages=[
                {
                    "role": "system",
                    "content": "반드시 유효한 JSON만 반환하세요.",
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
        )

        content = (response.choices[0].message.content or "").strip()

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
            f"에러: {e}. 원본 출력(앞부분): {content[:3000]}"
        ) from e

    if not isinstance(parsed, dict):
        raise RuntimeError("모델 JSON의 최상위는 객체(dict)여야 합니다.")

    # 최소 필드 보정
    parsed.setdefault("summary", "")
    parsed.setdefault("decisions", [])
    parsed.setdefault("action_items", [])

    return parsed


def summarize_meeting_from_text(
    stt_text: str,
    ocr_text: str,
    title: str = "",
) -> Dict[str, Any]:
    """
    STT 텍스트 + OCR 텍스트를 기반으로 회의 요약 수행

    반환 구조
    ----------
    {
        "stt_text": "...",         # 사용자에게 그대로 보여줄 STT 텍스트
        "ocr_text": "...",         # 사용자에게 그대로 보여줄 OCR 텍스트
        "summary_result": { ... }  # STT + OCR을 종합한 회의 요약
    }

    즉,
    - STT 따로 제공
    - OCR 따로 제공
    - 요약은 둘을 합쳐서 제공
    """

    # None 방지 및 문자열 정리
    stt_text = (stt_text or "").strip()
    ocr_text = (ocr_text or "").strip()
    title = (title or "").strip()

    # 1. STT + OCR을 함께 넣어 요약 프롬프트 생성
    prompt = _build_prompt(
        stt_text=stt_text,
        ocr_text=ocr_text,
        title=title,
    )

    # 2. LLM이 둘을 종합한 요약 결과 생성
    summary_result = _call_llm(prompt)

    # 3. 사용자에게는 원문(STT/OCR) + 통합 요약 결과를 함께 반환
    return {
        "stt_text": stt_text,
        "ocr_text": ocr_text,
        "summary_result": summary_result,
    }


def summarize_meeting_from_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    STT JSON + OCR JSON payload 전체를 기반으로 회의 요약 수행

    이 함수는 payload 안에서 STT / OCR 원문을 추출한 뒤,
    사용자에게는
    - stt_text
    - ocr_text
    - summary_result
    를 함께 반환한다.

    payload 예시
    ------------
    {
        "meeting": {
            "meeting_id": 1,
            "title": "주간 회의",
            "description": "..."
        },
        "stt": [
            {
                "id": 1,
                "meeting_id": 1,
                "content": "이번 주 일정 정리해보겠습니다.",
                "created_at": "2026-04-01T10:00:00"
            }
        ],
        "ocr": [
            {
                "id": 10,
                "meeting_id": 1,
                "file_path": "uploads/images/xxx.png",
                "image_type": "image",
                "ocr_text": "프로젝트 목표: ...",
                "analysis_text": "회의 자료 요약: ...",
                "created_at": "2026-04-01T10:05:00"
            }
        ]
    }
    """

    if not payload:
        raise RuntimeError("LLM에 전달할 payload가 비어 있습니다.")

    # -----------------------------------------
    # 1. payload에서 STT 텍스트 추출
    # -----------------------------------------
    # stt는 리스트 형태라고 가정
    # 기존 유틸 함수 stt_json_to_text를 사용하여
    # STT JSON 배열 -> 하나의 문자열로 변환
    stt_items = payload.get("stt", [])
    stt_text = stt_json_to_text(stt_items)

    # -----------------------------------------
    # 2. payload에서 OCR 텍스트 추출
    # -----------------------------------------
    # OCR 항목이 여러 개일 수 있으므로
    # ocr_text와 analysis_text를 모두 합쳐 하나의 문자열로 만듦
    ocr_items = payload.get("ocr", [])
    ocr_parts = []

    for item in ocr_items:
        if not isinstance(item, dict):
            continue

        raw_ocr_text = (item.get("ocr_text") or "").strip()
        analysis_text = (item.get("analysis_text") or "").strip()

        if raw_ocr_text:
            ocr_parts.append(raw_ocr_text)

        if analysis_text:
            ocr_parts.append(analysis_text)

    ocr_text = "\n".join(ocr_parts).strip()

    # -----------------------------------------
    # 3. payload 전체를 이용해 LLM 요약 수행
    # -----------------------------------------
    prompt = _build_payload_prompt(payload)
    summary_result = _call_llm(prompt)

    # -----------------------------------------
    # 4. 사용자에게는 STT / OCR / 요약 결과를 함께 반환
    # -----------------------------------------
    return {
        "stt_text": stt_text,
        "ocr_text": ocr_text,
        "summary_result": summary_result,
    }


def summarize_meeting(
    stt_segments: Sequence[Any],
    ocr_text: str,
    title: str = "",
) -> Dict[str, Any]:
    """
    기존 호환용 함수:
    STT 세그먼트 배열 + OCR 텍스트를 기반으로 회의 요약 수행

    이 함수도 동일하게
    - STT 따로
    - OCR 따로
    - 요약은 둘을 합쳐서
    반환하도록 맞춤
    """

    # STT JSON/세그먼트 배열을 사람이 읽을 수 있는 텍스트로 변환
    stt_text = stt_json_to_text(stt_segments)

    # 최종 반환 형식은 summarize_meeting_from_text와 동일
    return summarize_meeting_from_text(
        stt_text=stt_text,
        ocr_text=ocr_text,
        title=title,
    )