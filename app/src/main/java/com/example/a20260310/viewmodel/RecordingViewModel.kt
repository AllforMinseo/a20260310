package com.example.a20260310.viewmodel

import android.os.Handler
import android.os.Looper
import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.ViewModel
import com.example.a20260310.data.model.RecordingUiState
import com.example.a20260310.data.model.UploadUiState
import com.example.a20260310.data.repository.MeetingRepository
import com.example.a20260310.data.repository.RecordingRepository
import com.example.a20260310.data.repository.RecordingRepositoryImpl

class RecordingViewModel(
    private val recordingRepository: RecordingRepository = RecordingRepositoryImpl(),
    private val meetingRepository: MeetingRepository = MeetingRepository(),
) : ViewModel() {
    private val mainHandler = Handler(Looper.getMainLooper())

    private val _uiState = MutableLiveData(RecordingUiState())
    val uiState: LiveData<RecordingUiState> = _uiState

    private val _uploadUiState = MutableLiveData(UploadUiState())
    val uploadUiState: LiveData<UploadUiState> = _uploadUiState

    private val ticker = object : Runnable {
        override fun run() {
            val current = _uiState.value ?: RecordingUiState()
            if (current.isRecording) {
                _uiState.value = current.copy(elapsedSeconds = current.elapsedSeconds + 1)
            }
            mainHandler.postDelayed(this, 1000L)
        }
    }

    init {
        mainHandler.postDelayed(ticker, 1000L)
    }

    fun toggleRecording(outputPath: String) {
        val current = _uiState.value ?: RecordingUiState()
        if (current.isRecording) {
            stopRecording()
        } else {
            startRecording(outputPath)
        }
    }

    private fun startRecording(outputPath: String) {
        recordingRepository.start(outputPath)
        _uiState.value = RecordingUiState(
            isRecording = true,
            elapsedSeconds = 0,
            outputPath = outputPath,
        )
    }

    fun stopRecording() {
        recordingRepository.stop()
        val current = _uiState.value ?: RecordingUiState()
        _uiState.value = current.copy(isRecording = false)
    }

    fun stopAndUploadRecording(filePath: String) {
        stopRecording()
        _uploadUiState.value = UploadUiState(isUploading = true)

        Thread {
            val result = meetingRepository.uploadRecordedAudio(filePath)
            result.onSuccess { uploaded ->
                _uploadUiState.postValue(
                    UploadUiState(
                        isUploading = false,
                        isSuccess = true,
                        meetingId = uploaded.meetingId,
                        transcriptText = uploaded.content,
                    )
                )
            }.onFailure { error ->
                _uploadUiState.postValue(
                    UploadUiState(
                        isUploading = false,
                        isSuccess = false,
                        errorMessage = error.message ?: "오디오 업로드에 실패했습니다.",
                    )
                )
            }
        }.start()
    }

    fun consumeUploadState() {
        _uploadUiState.value = UploadUiState()
    }

    override fun onCleared() {
        mainHandler.removeCallbacks(ticker)
        recordingRepository.stop()
        super.onCleared()
    }
}
