"""
summary_schema.py

회의 요약(Summary) 관련 요청/응답 스키마 정의

역할
- 요약 생성 요청/응답 형식 정의
- 회의 요약 조회 API 응답 형식 정의

주의
- 실제 요약 생성은 ai/meeting_summarizer.py에서 수행
- DB 저장 구조는 models/summary_model.py에서 관리
"""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class SummaryCreate(BaseModel):
    """
    summary 생성 요청 스키마

    실제 서비스에서는 transcript를 바탕으로 자동 생성되는 경우가 많지만,
    테스트나 수동 생성 시 사용할 수 있음
    """

    meeting_id: int = Field(..., gt=0, description="회의 ID")
    content: str = Field(..., min_length=1, description="회의 요약 텍스트")


class SummaryResponse(BaseModel):
    """
    summary 응답 스키마
    """

    model_config = ConfigDict(from_attributes=True)

    id: int
    meeting_id: int
    content: str
    created_at: datetime
    updated_at: datetime


class SummaryGenerateResponse(BaseModel):
    """
    요약 생성 API 전용 응답 스키마

    예:
    POST /meetings/{meeting_id}/summary
    """

    meeting_id: int
    summary: str