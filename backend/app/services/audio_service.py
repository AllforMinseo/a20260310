"""
audio_service.py

오디오 처리 서비스 계층

역할
- 업로드된 오디오 파일 저장
- 오디오 전처리
- STT 수행
- transcript DB 저장

흐름
upload_router
    ↓
audio_service
    ↓
file_manager
    ↓
preprocess
    ↓
stt_service
    ↓
transcript_repository
"""

from __future__ import annotations

from sqlalchemy.orm import Session

from repositories.transcript_repository import create_transcript
from schemas.transcript_schema import TranscriptCreate, TranscriptResponse
from services.stt_service import transcribe_audio_file
from storage.file_manager import save_audio_file
from utils.preprocess import preprocess_audio_file


def process_uploaded_audio(
    db: Session,
    meeting_id: int,
    upload_file,
) -> TranscriptResponse:
    """
    업로드된 오디오 파일을 저장하고 STT를 수행한 뒤 transcript를 DB에 저장

    Parameters
    ----------
    db : Session
        SQLAlchemy DB 세션

    meeting_id : int
        이 오디오가 연결될 회의 ID

    upload_file : UploadFile
        FastAPI UploadFile 객체

    Returns
    -------
    TranscriptResponse
        저장된 transcript 응답 스키마
    """

    # 1. 오디오 파일 저장
    saved_path = save_audio_file(upload_file)

    # 2. 오디오 전처리
    processed_path = preprocess_audio_file(saved_path)

    # 3. STT 실행
    transcript_text = transcribe_audio_file(processed_path)

    # 4. transcript 생성 스키마 작성
    transcript_data = TranscriptCreate(
        meeting_id=meeting_id,
        content=transcript_text,
    )

    # 5. DB 저장
    transcript = create_transcript(db, transcript_data)

    # 6. 응답 스키마 변환
    return TranscriptResponse.model_validate(transcript)