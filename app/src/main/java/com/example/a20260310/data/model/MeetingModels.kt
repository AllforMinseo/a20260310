package com.example.a20260310.data.model

data class ActionItem(
    val id: Long? = null,
    val content: String,
    val owner: String? = null,
    val dueDate: String? = null,
)

data class MeetingSummary(
    val title: String,
    val summary: String,
    val actionItems: List<ActionItem> = emptyList(),
)

data class AnalyzeResponse(
    val meetingId: Long,
    val summary: MeetingSummary,
)

data class MeetingRecord(
    val meetingId: Long,
    val title: String,
    val durationMinutes: Int? = null,
    val createdAt: String? = null,
)
