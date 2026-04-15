package com.example.a20260310.data.repository

interface RecordingRepository {
    fun start(outputPath: String)
    fun stop()
}
