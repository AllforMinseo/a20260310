"""
image_repository.py

Image 테이블에 대한 DB 접근 로직을 담당하는 Repository

역할
- 이미지 생성
- 이미지 단건 조회
- 회의별 이미지 목록 조회
- image_type 기준 조회
- 이미지 삭제

주의
- 일반 이미지와 화이트보드 이미지를 image_type으로 구분
"""

from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session

from models.image_model import Image
from schemas.image_schema import ImageCreate


def create_image(db: Session, image_data: ImageCreate) -> Image:
    """
    이미지 생성
    """

    image = Image(
        meeting_id=image_data.meeting_id,
        file_path=image_data.file_path,
        image_type=image_data.image_type,
        ocr_text=image_data.ocr_text,
        analysis_text=image_data.analysis_text,
    )

    db.add(image)
    db.commit()
    db.refresh(image)

    return image


def get_image_by_id(db: Session, image_id: int) -> Optional[Image]:
    """
    이미지 ID로 단건 조회
    """

    return (
        db.query(Image)
        .filter(Image.id == image_id)
        .first()
    )


def get_images_by_meeting_id(
    db: Session,
    meeting_id: int,
    skip: int = 0,
    limit: int = 100,
) -> list[Image]:
    """
    특정 회의의 이미지 목록 조회
    """

    return (
        db.query(Image)
        .filter(Image.meeting_id == meeting_id)
        .order_by(Image.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_images_by_type(
    db: Session,
    meeting_id: int,
    image_type: str,
    skip: int = 0,
    limit: int = 100,
) -> list[Image]:
    """
    특정 회의에서 특정 image_type의 이미지 목록 조회

    image_type 예시
    --------------
    - image
    - whiteboard
    """

    return (
        db.query(Image)
        .filter(
            Image.meeting_id == meeting_id,
            Image.image_type == image_type,
        )
        .order_by(Image.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def delete_image(db: Session, image: Image) -> None:
    """
    이미지 삭제
    """

    db.delete(image)
    db.commit()