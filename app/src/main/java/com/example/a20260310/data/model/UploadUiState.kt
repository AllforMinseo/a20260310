package com.example.a20260310.data.model

data class UploadUiState(
    val isUploading: Boolean = false,
    val isSuccess: Boolean = false,
    val meetingId: Long? = null,
    val transcriptText: String? = null,
    val errorMessage: String? = null,
)
