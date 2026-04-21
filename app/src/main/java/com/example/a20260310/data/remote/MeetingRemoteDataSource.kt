package com.example.a20260310.data.remote

import com.example.a20260310.data.model.AnalyzeResponse

class MeetingRemoteDataSource {
    fun requestAnalyze(meetingId: Long): Result<AnalyzeResponse> {
        return Result.failure(UnsupportedOperationException("Remote API is not wired yet."))
    }
}
