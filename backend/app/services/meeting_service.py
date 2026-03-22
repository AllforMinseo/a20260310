"""
meeting_service.py

회의 관련 비즈니스 로직을 담당하는 서비스 계층

역할
- 회의 생성
- 회의 목록 조회
- 회의 단건 조회
- 회의 수정
- 회의 삭제
- transcript 기반 summary 생성
- 회의의 summary 조회

가정
- 현재 프로젝트에서는 회의당 summary를 1개로 관리
- summary 재생성 시 기존 summary를 삭제하고 새로 저장
"""

from __future__ import annotations

from sqlalchemy.orm import Session

from ai.meeting_summarizer import generate_meeting_summary
from repositories.meeting_repository import (
    create_meeting,
    delete_meeting,
    get_all_meetings,
    get_meeting_by_id,
    update_meeting,
)
from repositories.summary_repository import (
    create_summary,
    delete_summary,
    get_summary_by_meeting_id,
)
from repositories.transcript_repository import get_transcripts_by_meeting_id
from schemas.meeting_schema import (
    MeetingCreate,
    MeetingResponse,
    MeetingUpdate,
)
from schemas.summary_schema import (
    SummaryCreate,
    SummaryGenerateResponse,
    SummaryResponse,
)


def create_new_meeting(db: Session, meeting_data: MeetingCreate) -> MeetingResponse:
    """
    회의 생성 서비스
    """

    meeting = create_meeting(db, meeting_data)
    return MeetingResponse.model_validate(meeting)


def get_meeting_detail(db: Session, meeting_id: int) -> MeetingResponse | None:
    """
    회의 단건 조회 서비스
    """

    meeting = get_meeting_by_id(db, meeting_id)

    if meeting is None:
        return None

    return MeetingResponse.model_validate(meeting)


def get_meeting_list(
    db: Session,
    skip: int = 0,
    limit: int = 100,
) -> list[MeetingResponse]:
    """
    회의 목록 조회 서비스
    """

    meetings = get_all_meetings(db, skip=skip, limit=limit)
    return [MeetingResponse.model_validate(meeting) for meeting in meetings]


def update_meeting_detail(
    db: Session,
    meeting_id: int,
    meeting_data: MeetingUpdate,
) -> MeetingResponse | None:
    """
    회의 수정 서비스
    """

    meeting = get_meeting_by_id(db, meeting_id)

    if meeting is None:
        return None

    updated_meeting = update_meeting(db, meeting, meeting_data)
    return MeetingResponse.model_validate(updated_meeting)


def remove_meeting(db: Session, meeting_id: int) -> bool:
    """
    회의 삭제 서비스

    Returns
    -------
    bool
        삭제 성공 여부
    """

    meeting = get_meeting_by_id(db, meeting_id)

    if meeting is None:
        return False

    delete_meeting(db, meeting)
    return True


def create_summary_for_meeting(
    db: Session,
    meeting_id: int,
) -> SummaryGenerateResponse | None:
    """
    특정 회의의 전체 transcript를 기반으로 summary를 생성하고 저장

    동작 방식
    --------
    1. 회의 존재 확인
    2. 해당 회의의 transcript 전체 조회
    3. transcript 내용을 하나로 합침
    4. 기존 summary가 있으면 삭제
    5. 새 summary 생성 및 저장

    Returns
    -------
    SummaryGenerateResponse | None
        회의가 없거나 transcript가 없으면 None
    """

    # 1. 회의 존재 확인
    meeting = get_meeting_by_id(db, meeting_id)
    if meeting is None:
        return None

    # 2. transcript 전체 조회
    transcripts = get_transcripts_by_meeting_id(db, meeting_id)
    if not transcripts:
        return None

    # 3. transcript 내용을 하나의 텍스트로 합침
    transcript_text = "\n".join(
        transcript.content for transcript in reversed(transcripts)
    )

    # 4. 기존 summary가 있으면 삭제
    existing_summary = get_summary_by_meeting_id(db, meeting_id)
    if existing_summary is not None:
        delete_summary(db, existing_summary)

    # 5. OpenAI 요약 생성
    summary_text = generate_meeting_summary(transcript_text)

    # 6. 새 summary 저장
    summary_data = SummaryCreate(
        meeting_id=meeting_id,
        content=summary_text,
    )
    create_summary(db, summary_data)

    return SummaryGenerateResponse(
        meeting_id=meeting_id,
        summary=summary_text,
    )


def get_summary_for_meeting(
    db: Session,
    meeting_id: int,
) -> SummaryResponse | None:
    """
    특정 회의의 summary 조회 서비스
    """

    summary = get_summary_by_meeting_id(db, meeting_id)

    if summary is None:
        return None

    return SummaryResponse.model_validate(summary)