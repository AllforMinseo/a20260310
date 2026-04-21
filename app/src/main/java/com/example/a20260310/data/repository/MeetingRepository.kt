package com.example.a20260310.data.repository

import com.example.a20260310.data.model.AnalyzeResponse
import com.example.a20260310.data.remote.MeetingRemoteDataSource

class MeetingRepository(
    private val remoteDataSource: MeetingRemoteDataSource = MeetingRemoteDataSource(),
) {
    fun requestAnalyze(meetingId: Long): Result<AnalyzeResponse> {
        return remoteDataSource.requestAnalyze(meetingId)
    }
}
