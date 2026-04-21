package com.example.a20260310.data.model

data class RecordingUiState(
    val isRecording: Boolean = false,
    val elapsedSeconds: Int = 0,
    val outputPath: String? = null,
)