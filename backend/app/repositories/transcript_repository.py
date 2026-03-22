"""
transcript_repository.py

Transcript 테이블에 대한 DB 접근 로직을 담당하는 Repository

역할
- transcript 생성
- transcript 단건 조회
- 회의별 transcript 목록 조회
- 가장 최근 transcript 조회
- transcript 삭제
"""

from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session

from models.transcript_model import Transcript
from schemas.transcript_schema import TranscriptCreate


def create_transcript(db: Session, transcript_data: TranscriptCreate) -> Transcript:
    """
    transcript 생성
    """

    transcript = Transcript(
        meeting_id=transcript_data.meeting_id,
        content=transcript_data.content,
    )

    db.add(transcript)
    db.commit()
    db.refresh(transcript)

    return transcript


def get_transcript_by_id(db: Session, transcript_id: int) -> Optional[Transcript]:
    """
    transcript ID로 단건 조회
    """

    return (
        db.query(Transcript)
        .filter(Transcript.id == transcript_id)
        .first()
    )


def get_transcripts_by_meeting_id(
    db: Session,
    meeting_id: int,
    skip: int = 0,
    limit: int = 100,
) -> list[Transcript]:
    """
    특정 회의의 transcript 목록 조회
    """

    return (
        db.query(Transcript)
        .filter(Transcript.meeting_id == meeting_id)
        .order_by(Transcript.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_latest_transcript_by_meeting_id(
    db: Session,
    meeting_id: int,
) -> Optional[Transcript]:
    """
    특정 회의의 가장 최근 transcript 조회
    """

    return (
        db.query(Transcript)
        .filter(Transcript.meeting_id == meeting_id)
        .order_by(Transcript.created_at.desc())
        .first()
    )


def delete_transcript(db: Session, transcript: Transcript) -> None:
    """
    transcript 삭제
    """

    db.delete(transcript)
    db.commit()