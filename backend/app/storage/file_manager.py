"""
file_manager.py

업로드 파일을 로컬 스토리지에 저장하는 모듈

역할
- 업로드된 오디오 파일 저장
- 업로드된 이미지 파일 저장
- 파일명을 UUID 기반으로 변경하여 중복 방지
- 저장 전 업로드 디렉토리 생성 보장

주의
- 이 모듈은 "파일 저장"만 담당
- 오디오/이미지 전처리는 utils.preprocess.py에서 담당
"""

from __future__ import annotations

import os
import shutil
import uuid
from pathlib import Path

from storage.upload_paths import (
    AUDIO_UPLOAD_DIR,
    IMAGE_UPLOAD_DIR,
    ensure_upload_dirs,
)


def _generate_unique_filename(original_filename: str | None) -> str:
    """
    원본 파일명을 기반으로 UUID를 붙여 고유 파일명 생성

    Parameters
    ----------
    original_filename : str | None
        업로드된 원본 파일명

    Returns
    -------
    str
        고유 파일명
    """

    # 원본 파일명에서 확장자 추출
    suffix = ""

    if original_filename:
        suffix = Path(original_filename).suffix.lower()

    # 확장자가 없는 경우 기본 확장자 없이 생성
    unique_name = f"{uuid.uuid4().hex}{suffix}"

    return unique_name


def save_audio_file(upload_file) -> str:
    """
    업로드된 오디오 파일을 로컬에 저장

    Parameters
    ----------
    upload_file : UploadFile
        FastAPI UploadFile 객체

    Returns
    -------
    str
        저장된 파일의 전체 경로
    """

    ensure_upload_dirs()

    filename = _generate_unique_filename(upload_file.filename)
    save_path = os.path.join(AUDIO_UPLOAD_DIR, filename)

    with open(save_path, "wb") as buffer:
        shutil.copyfileobj(upload_file.file, buffer)

    return save_path


def save_image_file(upload_file) -> str:
    """
    업로드된 이미지 파일을 로컬에 저장

    Parameters
    ----------
    upload_file : UploadFile
        FastAPI UploadFile 객체

    Returns
    -------
    str
        저장된 파일의 전체 경로
    """

    ensure_upload_dirs()

    filename = _generate_unique_filename(upload_file.filename)
    save_path = os.path.join(IMAGE_UPLOAD_DIR, filename)

    with open(save_path, "wb") as buffer:
        shutil.copyfileobj(upload_file.file, buffer)

    return save_path