package com.example.a20260310.viewmodel

import android.os.Handler
import android.os.Looper
import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.ViewModel
import com.example.a20260310.data.model.RecordingUiState
import com.example.a20260310.data.repository.RecordingRepository
import com.example.a20260310.data.repository.RecordingRepositoryImpl

class RecordingViewModel(
    private val recordingRepository: RecordingRepository = RecordingRepositoryImpl(),
) : ViewModel() {
    private val mainHandler = Handler(Looper.getMainLooper())
    private var elapsedTickCount = 0

    private val _uiState = MutableLiveData(RecordingUiState())
    val uiState: LiveData<RecordingUiState> = _uiState

    private val ticker = object : Runnable {
        override fun run() {
            val current = _uiState.value ?: RecordingUiState()
            if (current.isRecording) {
                elapsedTickCount += 1
                _uiState.value = current.copy(
                    elapsedSeconds = elapsedTickCount / 10,
                    amplitude = recordingRepository.getMaxAmplitude(),
                )
            } else if (current.amplitude != 0) {
                _uiState.value = current.copy(amplitude = 0)
            }
            mainHandler.postDelayed(this, 100L)
        }
    }

    init {
        mainHandler.postDelayed(ticker, 100L)
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
        elapsedTickCount = 0
        _uiState.value = RecordingUiState(
            isRecording = true,
            elapsedSeconds = 0,
            outputPath = outputPath,
            amplitude = 0,
        )
    }

    fun stopRecording() {
        recordingRepository.stop()
        val current = _uiState.value ?: RecordingUiState()
        _uiState.value = current.copy(isRecording = false, amplitude = 0)
    }

    override fun onCleared() {
        mainHandler.removeCallbacks(ticker)
        recordingRepository.stop()
        super.onCleared()
    }
}
