"""
schemas 패키지 초기화 파일

역할
- 주요 스키마를 외부에서 쉽게 import 할 수 있도록 정리

예시
----
from schemas import MeetingCreate, MeetingResponse
"""

from schemas.image_schema import ImageCreate, ImageResponse, ImageUploadResponse
from schemas.meeting_schema import MeetingCreate, MeetingResponse, MeetingUpdate
from schemas.summary_schema import (
    SummaryCreate,
    SummaryDetailResponse,
    SummaryGenerateResponse,
    SummaryResponse,
)
from schemas.transcript_schema import (
    TranscriptCreate,
    TranscriptResponse,
    TranscriptSimpleResponse,
)

__all__ = [
    # meeting
    "MeetingCreate",
    "MeetingUpdate",
    "MeetingResponse",

    # transcript
    "TranscriptCreate",
    "TranscriptResponse",
    "TranscriptSimpleResponse",

    # summary
    "SummaryCreate",
    "SummaryResponse",
    "SummaryGenerateResponse",
    "SummaryDetailResponse",

    # image
    "ImageCreate",
    "ImageResponse",
    "ImageUploadResponse",
]