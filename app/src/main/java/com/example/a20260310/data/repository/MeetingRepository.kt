package com.example.a20260310.data.repository

import com.example.a20260310.data.model.UploadedTranscript
import com.example.a20260310.data.remote.MeetingRemoteDataSource
import java.io.File

class MeetingRepository(
    private val remoteDataSource: MeetingRemoteDataSource = MeetingRemoteDataSource(),
) {
    fun uploadRecordedAudio(filePath: String): Result<UploadedTranscript> {
        return runCatching {
            val audioFile = File(filePath)
            require(audioFile.exists() && audioFile.length() > 0L) {
                "녹음 파일이 없거나 비어 있습니다: $filePath"
            }

            val meetingId = remoteDataSource.createMeeting(
                title = "앱 녹음 ${System.currentTimeMillis()}",
                description = "모바일 앱에서 업로드된 녹음",
            )

            remoteDataSource.uploadAudio(
                meetingId = meetingId,
                audioFile = audioFile,
            )
        }
    }
}
