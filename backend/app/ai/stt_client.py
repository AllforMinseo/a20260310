"""
stt_client.py

외부 STT 서버와 통신하는 클라이언트 모듈

역할
- 오디오 파일을 외부 STT 서버에 전송
- STT 결과 텍스트를 반환
- STT 서버 응답 형식을 최대한 유연하게 처리

가정
- settings.py의 stt_server_url 값을 사용
- 기본 엔드포인트는 {STT_SERVER_URL}/transcribe
- multipart/form-data 형식으로 파일 업로드

주의
- 실제 외부 STT 서버의 API 명세에 따라 endpoint, field name, 응답 key는 조정이 필요할 수 있음
"""

from __future__ import annotations

import os
from typing import Any

import requests

from config.settings import settings


def _build_stt_endpoint() -> str:
    """
    STT 서버의 최종 엔드포인트 URL 생성
    """

    base_url = (settings.stt_server_url or "").rstrip("/")

    if not base_url:
        raise ValueError("STT_SERVER_URL이 설정되지 않았습니다.")

    return f"{base_url}/transcribe"


def _extract_transcript_from_response(data: Any) -> str:
    """
    STT 서버 응답(JSON)에서 transcript를 최대한 유연하게 추출

    지원 예시
    --------
    {"text": "..."}
    {"transcript": "..."}
    {"result": {"text": "..."}}
    {"result": {"transcript": "..."}}
    """

    if isinstance(data, dict):
        if isinstance(data.get("text"), str):
            return data["text"].strip()

        if isinstance(data.get("transcript"), str):
            return data["transcript"].strip()

        result = data.get("result")
        if isinstance(result, dict):
            if isinstance(result.get("text"), str):
                return result["text"].strip()

            if isinstance(result.get("transcript"), str):
                return result["transcript"].strip()

    raise RuntimeError("STT 응답에서 transcript를 찾지 못했습니다.")


def request_stt(file_path: str, timeout: int = 180) -> str:
    """
    외부 STT 서버에 오디오 파일을 전송하고 transcript를 반환

    Parameters
    ----------
    file_path : str
        전송할 오디오 파일 경로

    timeout : int
        요청 타임아웃(초)

    Returns
    -------
    str
        STT 결과 텍스트
    """

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"오디오 파일을 찾을 수 없습니다: {file_path}")

    endpoint = _build_stt_endpoint()

    filename = os.path.basename(file_path)

    with open(file_path, "rb") as audio_file:
        files = {
            "file": (filename, audio_file, "audio/wav"),
        }

        response = requests.post(
            endpoint,
            files=files,
            timeout=timeout,
        )

    response.raise_for_status()

    # 우선 JSON 응답을 시도
    try:
        data = response.json()
        return _extract_transcript_from_response(data)
    except ValueError:
        # JSON이 아니면 plain text로 간주
        text = response.text.strip()
        if not text:
            raise RuntimeError("STT 서버 응답이 비어 있습니다.")
        return text

