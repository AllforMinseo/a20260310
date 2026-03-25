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
"""
오디오 변환 정책
---------------
- 입력 파일이 .wav면 그대로 사용
- .wav가 아니면 ffmpeg를 사용해 .wav로 변환
- 변환 결과 파일은 원본 파일과 같은 폴더에 저장
- 파일명 뒤에 "_converted.wav"를 붙여 저장

주의
----
- ffmpeg가 시스템에 설치되어 있어야 자동 변환 가능
- ffmpeg가 없으면 RuntimeError를 발생시킴
"""

import json
import os
import re
from typing import Any, Dict, List, Sequence

def preprocess_audio_file(file_path: str) -> str:
    """
    오디오 파일 전처리

    현재 버전에서 하는 일
    -------------------
    - 파일 존재 여부 확인
    - 필요 시 추후 확장을 위한 전처리 진입점 유지
    - 현재는 원본 경로를 그대로 반환

    추후 확장 가능 작업
    -------------------
    - mp3, m4a 파일을 wav로 변환
    - 샘플레이트 통일
    - 무음 구간 제거
    - 잡음 제거

    Parameters
    ----------
    file_path : str
        저장된 오디오 파일 경로

    Returns
    -------
    str
        전처리 후 사용할 오디오 파일 경로
    """

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"오디오 파일을 찾을 수 없습니다: {file_path}")

    return file_path


def preprocess_image_file(file_path: str) -> str:
    """
    이미지 파일 전처리

    현재 버전에서 하는 일
    -------------------
    - 파일 존재 여부 확인
    - 필요 시 추후 확장을 위한 전처리 진입점 유지
    - 현재는 원본 경로를 그대로 반환

    추후 확장 가능 작업
    -------------------
    - 이미지 리사이즈
    - 회전 보정
    - 흑백 변환
    - 대비 향상

    Parameters
    ----------
    file_path : str
        저장된 이미지 파일 경로

    Returns
    -------
    str
        전처리 후 사용할 이미지 파일 경로
    """

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"이미지 파일을 찾을 수 없습니다: {file_path}")

    return file_path


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


def normalize_transcript_text(text: str) -> str:
    """
    이미 문자열로 만들어진 transcript를 정리

    역할
    ----
    - 앞뒤 공백 제거
    - 빈 줄 제거
    - 연속 공백 축소

    사용 예
    -------
    - STT 서버가 문자열을 직접 반환했을 때
    - 저장 전 transcript 정리
    """

    if not text:
        return ""

    lines = [line.strip() for line in text.splitlines()]
    lines = [line for line in lines if line]

    normalized = "\n".join(lines)
    normalized = re.sub(r"[ \t]+", " ", normalized)

    return normalized.strip()


def safe_json_dumps(data: Any) -> str:
    """
    dict/list 등의 데이터를 JSON 문자열로 안전하게 변환

    Parameters
    ----------
    data : Any
        JSON 직렬화할 데이터

    Returns
    -------
    str
        JSON 문자열
    """

    return json.dumps(data, ensure_ascii=False)