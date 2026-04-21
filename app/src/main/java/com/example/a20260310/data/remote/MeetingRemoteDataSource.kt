package com.example.a20260310.data.remote

import com.example.a20260310.BuildConfig
import com.example.a20260310.data.model.UploadedTranscript
import org.json.JSONObject
import java.io.DataOutputStream
import java.io.File
import java.net.HttpURLConnection
import java.net.URL

class MeetingRemoteDataSource {
    private val baseUrl = BuildConfig.BASE_URL

    fun createMeeting(title: String, description: String? = null): Long {
        val url = URL("$baseUrl/meetings")
        val conn = (url.openConnection() as HttpURLConnection).apply {
            requestMethod = "POST"
            connectTimeout = 10000
            readTimeout = 15000
            doOutput = true
            setRequestProperty("Content-Type", "application/json; charset=utf-8")
        }

        return try {
            val payload = JSONObject().apply {
                put("title", title)
                put("description", description ?: "앱에서 업로드한 녹음")
            }
            conn.outputStream.use { it.write(payload.toString().toByteArray(Charsets.UTF_8)) }

            val code = conn.responseCode
            val body = readResponseBody(conn, code)
            if (code !in 200..299) {
                throw IllegalStateException("회의 생성 실패(code=$code): $body")
            }

            JSONObject(body).getLong("id")
        } finally {
            conn.disconnect()
        }
    }

    fun uploadAudio(meetingId: Long, audioFile: File): UploadedTranscript {
        val boundary = "----MOA${System.currentTimeMillis()}"
        val url = URL("$baseUrl/upload/audio/$meetingId")
        val conn = (url.openConnection() as HttpURLConnection).apply {
            requestMethod = "POST"
            connectTimeout = 10000
            readTimeout = 30000
            doOutput = true
            doInput = true
            useCaches = false
            setRequestProperty("Content-Type", "multipart/form-data; boundary=$boundary")
        }

        return try {
            DataOutputStream(conn.outputStream).use { out ->
                out.writeBytes("--$boundary\r\n")
                out.writeBytes("Content-Disposition: form-data; name=\"file\"; filename=\"${audioFile.name}\"\r\n")
                out.writeBytes("Content-Type: audio/mp4\r\n\r\n")
                audioFile.inputStream().use { input ->
                    input.copyTo(out)
                }
                out.writeBytes("\r\n--$boundary--\r\n")
                out.flush()
            }

            val code = conn.responseCode
            val body = readResponseBody(conn, code)
            if (code !in 200..299) {
                throw IllegalStateException("오디오 업로드 실패(code=$code): $body")
            }

            val json = JSONObject(body)
            val content = json.optString("content", "")
            UploadedTranscript(
                meetingId = json.optLong("meeting_id", meetingId),
                content = content,
            )
        } finally {
            conn.disconnect()
        }
    }

    private fun readResponseBody(conn: HttpURLConnection, code: Int): String {
        val stream = if (code in 200..299) conn.inputStream else conn.errorStream
        return stream?.bufferedReader(Charsets.UTF_8)?.use { it.readText() } ?: ""
    }
}
