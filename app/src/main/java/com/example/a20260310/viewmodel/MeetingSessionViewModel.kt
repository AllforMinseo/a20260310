package com.example.a20260310.viewmodel

import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.ViewModel
import com.example.a20260310.data.model.MeetingDraft
import com.example.a20260310.data.model.MinutesUiMapper
import com.example.a20260310.data.model.MinutesUiModel
import com.example.a20260310.data.repository.MeetingRepository
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import java.io.File
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale
import java.util.UUID

data class SelectedSourceFile(
    val id: String = UUID.randomUUID().toString(),
    val type: Type,
    val displayName: String,
    val localPath: String,
) {
    enum class Type { AUDIO_RECORD, AUDIO_UPLOAD, IMAGE, DOCUMENT }
}

class MeetingSessionViewModel(
    private val repository: MeetingRepository = MeetingRepository(),
) : ViewModel() {
    @Volatile
    private var draft: MeetingDraft = MeetingDraft()

    private val _meetingDraft = MutableLiveData(MeetingDraft())
    val meetingDraft: LiveData<MeetingDraft> = _meetingDraft

    private val _minutes = MutableLiveData<MinutesUiModel?>(null)
    val minutes: LiveData<MinutesUiModel?> = _minutes

    private val _isPipelineRunning = MutableLiveData(false)
    val isPipelineRunning: LiveData<Boolean> = _isPipelineRunning

    private val _pipelineError = MutableLiveData<String?>(null)
    val pipelineError: LiveData<String?> = _pipelineError

    private val _selectedFiles = MutableLiveData<List<SelectedSourceFile>>(emptyList())
    val selectedFiles: LiveData<List<SelectedSourceFile>> = _selectedFiles

    fun setDraft(newDraft: MeetingDraft) {
        draft = newDraft
        _meetingDraft.value = newDraft
    }

    fun clearPipelineError() {
        _pipelineError.value = null
    }

    fun clearMinutes() {
        _minutes.value = null
    }

    fun addSelectedFile(file: SelectedSourceFile) {
        val current = _selectedFiles.value.orEmpty()
        _selectedFiles.value = current + file
    }

    fun removeSelectedFile(id: String) {
        _selectedFiles.value = _selectedFiles.value.orEmpty().filterNot { it.id == id }
    }

    fun hasSelectedFilesForSummary(): Boolean = _selectedFiles.value.orEmpty().isNotEmpty()

    suspend fun awaitSummarizeSelectedFiles() {
        _pipelineError.value = null
        _isPipelineRunning.value = true
        try {
            val snapshot = draft
            val selected = _selectedFiles.value.orEmpty()
            try {
                val created = withContext(Dispatchers.IO) {
                    repository.createMeeting(
                        title = snapshot.title.ifBlank { "무제 회의" },
                        description = snapshot.toDescription(),
                    )
                }
                var latestTranscriptText = ""
                withContext(Dispatchers.IO) {
                    selected.forEach { file ->
                        val local = File(file.localPath)
                        if (!local.exists() || local.length() == 0L) return@forEach
                        when (file.type) {
                            SelectedSourceFile.Type.AUDIO_RECORD,
                            SelectedSourceFile.Type.AUDIO_UPLOAD -> {
                                val transcript = repository.uploadAudio(created.id, local)
                                latestTranscriptText = transcript.content
                            }
                            SelectedSourceFile.Type.IMAGE,
                            SelectedSourceFile.Type.DOCUMENT -> {
                                repository.uploadImage(created.id, local, imageType = "image")
                            }
                        }
                    }
                }
                val summary = withContext(Dispatchers.IO) {
                    repository.generateSummary(created.id)
                }
                val ui = MinutesUiMapper.build(snapshot, latestTranscriptText, summary)
                _minutes.value = ui
            } catch (_: Exception) {
                // STT/요약 서버가 닫혀 있어도 화면 테스트를 이어갈 수 있도록 더미 데이터로 대체한다.
                _pipelineError.value = null
                _minutes.value = buildDummyMinutes(snapshot, selected)
            }
        } finally {
            _isPipelineRunning.value = false
        }
    }

    private fun buildDummyMinutes(snapshot: MeetingDraft, files: List<SelectedSourceFile>): MinutesUiModel {
        val now = SimpleDateFormat("yyyy.MM.dd HH:mm", Locale.getDefault()).format(Date())
        val title = snapshot.title.trim().ifBlank { "더미 회의" }
        val summaryBody =
            "서버 비연결 상태로 더미 요약을 생성했습니다. 실제 연동 시에는 STT·요약 API 결과가 표시됩니다."
        val usedSources = files.joinToString(", ") { it.displayName }
        return MinutesUiModel(
            subject = title,
            datetime = snapshot.displayDatetime().takeIf { it != "—" } ?: now,
            attendees = "김모아, 이기록, 박요약",
            summaryText = summaryBody,
            agenda = "• 앱 UI 검증\n• 더미 파이프라인 점검\n• 서버 재연결 전 체크리스트 정리",
            discussion = buildString {
                append(summaryBody)
                append("\n\n선택 소스: ${usedSources.ifBlank { "없음" }}")
            },
            note = "현재 STT 서버가 닫혀 있어 로컬 더미 모드로 동작 중입니다.",
            followup = "• 서버 오픈 후 실데이터 리그레션 테스트\n• 공유/저장 기능 QA",
            writerLabel = "작성자: MOA (DUMMY)",
        )
    }
}
