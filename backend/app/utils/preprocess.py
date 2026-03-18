from __future__ import annotations

# 전처리 유틸리티 모듈.
#
# 현재 MOA 백엔드의 STT 입력은 Whisper 스타일의 JSON "세그먼트 배열"입니다.
# 이 모듈은 해당 세그먼트 배열을 사람이 읽기 좋은 텍스트로 변환하는 전처리를 제공합니다.
#
# 전처리 철학:
# - 의미를 새로 해석/요약/재작성하지 않습니다.
# - 화자 구분/시간 기반 병합/유사도 기반 제거(fuzzy matching)는 하지 않습니다.
# - 허용: 노이즈 제거, 공백 정리, 완전 동일 반복 축약, 연속 동일 세그먼트 제거, 번호 붙이기, 문장부호 보정

import re
from typing import Any, Dict, List, Sequence


def normalize_text(text: str) -> str:
    """앞뒤 공백 제거 + 연속 공백 축소 + 탭/개행을 공백으로 정리합니다."""
    text = (text or "").replace("\r\n", "\n").replace("\r", "\n")
    text = text.replace("\t", " ")
    text = re.sub(r"\s*\n\s*", " ", text)  # 세그먼트 단위로만 줄바꿈을 사용하므로 평탄화
    text = re.sub(r"[ ]{2,}", " ", text).strip()
    return text


def collapse_internal_repetition(text: str) -> str:
    """
    한 세그먼트 내부에서 완전히 동일한 구절이 반복되면 1회만 남깁니다.

    예:
    - "수요일 가능해요, 수요일 가능해요" -> "수요일 가능해요"
    - "서버 서버 서버" -> "서버"
    """
    text = normalize_text(text)
    if not text:
        return ""

    # 1) 쉼표로 나뉜 구절이 전부 동일하면 1회만 유지
    comma_parts = [p.strip() for p in text.split(",") if p.strip()]
    if len(comma_parts) >= 2 and all(p == comma_parts[0] for p in comma_parts):
        return comma_parts[0]

    # 2) 공백 토큰이 전부 동일하면 1회만 유지
    tokens = [t for t in text.split(" ") if t]
    if len(tokens) >= 2 and all(t == tokens[0] for t in tokens):
        return tokens[0]

    return text


def ensure_sentence_punctuation(text: str) -> str:
    """줄 끝에 문장부호가 없으면 마침표를 보정합니다."""
    text = (text or "").strip()
    if not text:
        return ""
    if re.search(r"[.!?。！？…]$", text):
        return text
    return f"{text}."


def deduplicate_consecutive_segments(lines: List[str]) -> List[str]:
    """정리된 텍스트 기준으로 바로 이전 줄과 완전히 같으면 제거합니다."""
    out: List[str] = []
    prev: str | None = None
    for ln in lines:
        if not ln:
            continue
        if prev is not None and ln == prev:
            continue
        out.append(ln)
        prev = ln
    return out


def _extract_text_from_segment(seg: Dict[str, Any]) -> str:
    """세그먼트(dict)에서 text만 안전하게 추출합니다."""
    value = seg.get("text")
    if not isinstance(value, str):
        return ""
    return value


def stt_json_to_lines(segments: Sequence[Any]) -> List[str]:
    """
    Whisper 스타일 STT 세그먼트 배열을 줄(list[str])로 변환합니다.

    방어 처리:
    - dict가 아니면 무시
    - text 키가 없으면 무시
    - text가 문자열이 아니면 무시
    - 정리 결과가 빈 문자열이면 제거
    """
    lines: List[str] = []

    for item in segments:
        if not isinstance(item, dict):
            continue
        raw = _extract_text_from_segment(item)
        text = collapse_internal_repetition(raw)
        text = normalize_text(text)
        if not text:
            continue
        text = ensure_sentence_punctuation(text)
        lines.append(text)

    return deduplicate_consecutive_segments(lines)


def stt_json_to_text(segments: Sequence[Any]) -> str:
    """
    STT 세그먼트 배열 → 번호 붙은 멀티라인 문자열로 변환합니다.
    전부 무효면 빈 문자열을 반환합니다.
    """
    lines = stt_json_to_lines(segments)
    if not lines:
        return ""
    return "\n".join(f"{i}. {ln}" for i, ln in enumerate(lines, start=1))
