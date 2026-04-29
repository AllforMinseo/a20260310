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
- 회의의 전체 transcript(전문) 조회

가정
- 현재 프로젝트에서는 회의당 summary를 1개로 관리
- summary 재생성 시 기존 summary를 삭제하고 새로 저장
- summary는 DB에는 JSON 문자열로 저장하고,
  API 응답에서는 dict 형태로 반환
"""

from __future__ import annotations

import json

from sqlalchemy.orm import Session

from ai.meeting_summarizer import summarize_meeting_from_text
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
from repositories.image_repository import get_images_by_meeting_id
from repositories.transcript_repository import get_transcripts_by_meeting_id
from schemas.meeting_schema import (
    MeetingCreate,
    MeetingResponse,
    MeetingUpdate,
)
from schemas.summary_schema import (
    SummaryCreate,
    SummaryDetailResponse,
    SummaryGenerateResponse,
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


def get_full_transcript_for_meeting(
    db: Session,
    meeting_id: int,
) -> str | None:
    """
    특정 회의의 전체 transcript(전문)를 하나의 문자열로 반환

    동작 방식
    --------
    1. 회의 존재 여부 확인
    2. 해당 회의의 transcript 전체 조회
    3. 시간 순서대로 transcript 내용을 이어 붙여 하나의 문자열 생성

    Returns
    -------
    str | None
        회의가 없으면 None
        transcript가 없으면 빈 문자열("")
    """

    # 1. 회의 존재 확인
    meeting = get_meeting_by_id(db, meeting_id)
    if meeting is None:
        return None

    # 2. transcript 전체 조회
    transcripts = get_transcripts_by_meeting_id(db, meeting_id)

    if not transcripts:
        return ""

    # 3. 저장된 transcript를 시간 순서대로 이어 붙임
    full_text = "\n".join(
        transcript.content for transcript in reversed(transcripts)
    )

    return full_text


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
    5. 구조화된 summary(dict) 생성
    6. DB 저장용 JSON 문자열로 변환 후 저장
    7. API 응답은 dict 그대로 반환

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
    transcript_text = "\n".join(
        transcript.content for transcript in reversed(transcripts)
    ) if transcripts else ""

    # 3. 이미지 OCR/분석 텍스트 수집
    images = get_images_by_meeting_id(db, meeting_id, skip=0, limit=1000)
    ocr_chunks: list[str] = []
    for image in reversed(images):
        if image.ocr_text and image.ocr_text.strip():
            ocr_chunks.append(image.ocr_text.strip())
        if image.analysis_text and image.analysis_text.strip():
            ocr_chunks.append(image.analysis_text.strip())
    ocr_text = "\n".join(ocr_chunks)

    # 4. STT/OCR 둘 다 비어 있으면 요약할 근거가 없음
    if not transcript_text.strip() and not ocr_text.strip():
        return None

    # 5. 기존 summary가 있으면 삭제
    existing_summary = get_summary_by_meeting_id(db, meeting_id)
    if existing_summary is not None:
        delete_summary(db, existing_summary)

    # 6. 구조화된 JSON summary 생성
    summary_result = summarize_meeting_from_text(
        stt_text=transcript_text,
        ocr_text=ocr_text,
        title=meeting.title,
    )
    # 최소 필드 보정
    summary_result.setdefault("summary", "")
    summary_result.setdefault("decisions", [])
    summary_result.setdefault("action_items", [])

    # 7. DB 저장용 문자열(JSON) 변환
    summary_content = json.dumps(summary_result, ensure_ascii=False)

    # 8. 새 summary 저장
    summary_data = SummaryCreate(
        meeting_id=meeting_id,
        content=summary_content,
    )
    create_summary(db, summary_data)

    # 9. 응답은 dict 그대로 반환
    return SummaryGenerateResponse(
        meeting_id=meeting_id,
        summary=summary_result,
    )


def get_summary_for_meeting(
    db: Session,
    meeting_id: int,
) -> SummaryDetailResponse | None:
    """
    특정 회의의 summary 조회 서비스

    동작 방식
    --------
    1. meeting_id로 summary 조회
    2. DB에 저장된 JSON 문자열(content)을 dict로 파싱
    3. 프론트엔드가 사용하기 쉬운 구조로 반환
    """

    summary = get_summary_by_meeting_id(db, meeting_id)

    if summary is None:
        return None

    try:
        parsed_summary = json.loads(summary.content)
    except json.JSONDecodeError:
        # 예외 상황에서는 최소 구조로 보정
        parsed_summary = {
            "summary": summary.content,
            "decisions": [],
            "action_items": [],
        }

    parsed_summary.setdefault("summary", "")
    parsed_summary.setdefault("decisions", [])
    parsed_summary.setdefault("action_items", [])

    return SummaryDetailResponse(
        id=summary.id,
        meeting_id=summary.meeting_id,
        summary=parsed_summary,
        created_at=summary.created_at,
        updated_at=summary.updated_at,
    )