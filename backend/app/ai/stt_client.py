# STT 엔진(placeholder).
# ⚠️ Whisper 실제 호출은 금지 범위입니다.
#
# TODO:
# - Whisper 모델 로딩/캐싱 전략 수립
# - audio 입력(file path/bytes) 받아 STT 텍스트로 변환하는 시그니처 확정

from __future__ import annotations

from typing import Optional


def transcribe_audio(audio_path: Optional[str] = None, audio_bytes: Optional[bytes] = None) -> str:
    """
    오디오를 STT 텍스트로 변환합니다(placeholder).

    TODO: Whisper 연동 후 구현
    """
    raise NotImplementedError("TODO: Whisper STT 연동 후 구현 예정")

