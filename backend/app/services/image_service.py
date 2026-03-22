"""
image_service.py

이미지 처리 서비스 계층

역할
- 업로드된 이미지 파일 저장
- 이미지 전처리
- OCR 수행
- 화이트보드 이미지는 추가 분석
- image DB 저장

흐름
upload_router
    ↓
image_service
    ↓
file_manager
    ↓
preprocess
    ↓
image_ocr
    ↓
image_repository
"""

from __future__ import annotations

from sqlalchemy.orm import Session

from ai.image_ocr import process_image_by_type
from repositories.image_repository import create_image
from schemas.image_schema import ImageCreate, ImageResponse, ImageUploadResponse
from storage.file_manager import save_image_file
from utils.preprocess import preprocess_image_file


def process_uploaded_image(
    db: Session,
    meeting_id: int,
    upload_file,
    image_type: str = "image",
) -> ImageUploadResponse:
    """
    업로드된 이미지를 저장하고 OCR/분석 후 DB에 저장

    Parameters
    ----------
    db : Session
        SQLAlchemy DB 세션

    meeting_id : int
        연결될 회의 ID

    upload_file : UploadFile
        FastAPI UploadFile 객체

    image_type : str
        이미지 종류
        - image
        - whiteboard

    Returns
    -------
    ImageUploadResponse
        업로드 후 OCR/분석 결과를 포함한 응답
    """

    # 1. 이미지 파일 저장
    saved_path = save_image_file(upload_file)

    # 2. 이미지 전처리
    processed_path = preprocess_image_file(saved_path)

    # 3. 이미지 종류에 따라 OCR / 분석 수행
    image_result = process_image_by_type(
        image_path=processed_path,
        image_type=image_type,
    )

    # 4. DB 저장용 스키마 생성
    image_data = ImageCreate(
        meeting_id=meeting_id,
        file_path=processed_path,
        image_type=image_type,
        ocr_text=image_result.get("ocr_text"),
        analysis_text=image_result.get("analysis_text"),
    )

    image = create_image(db, image_data)

    # 5. 업로드 응답 반환
    return ImageUploadResponse(
        meeting_id=image.meeting_id,
        file_path=image.file_path,
        image_type=image.image_type,
        ocr_text=image.ocr_text,
        analysis_text=image.analysis_text,
    )


def get_meeting_images(
    db: Session,
    meeting_id: int,
) -> list[ImageResponse]:
    """
    특정 회의의 이미지 목록을 조회하는 서비스

    Parameters
    ----------
    db : Session
        SQLAlchemy DB 세션

    meeting_id : int
        회의 ID
    """

    from repositories.image_repository import get_images_by_meeting_id

    images = get_images_by_meeting_id(db, meeting_id)

    return [ImageResponse.model_validate(image) for image in images]
