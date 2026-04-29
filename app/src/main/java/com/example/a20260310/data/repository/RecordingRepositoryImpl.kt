package com.example.a20260310.data.repository

import android.media.MediaRecorder

class RecordingRepositoryImpl : RecordingRepository {
    private var mediaRecorder: MediaRecorder? = null

    override fun start(outputPath: String) {
        mediaRecorder = MediaRecorder().apply {
            setAudioSource(MediaRecorder.AudioSource.MIC)
            setOutputFormat(MediaRecorder.OutputFormat.MPEG_4)
            setAudioEncoder(MediaRecorder.AudioEncoder.AAC)
            setOutputFile(outputPath)
            prepare()
            start()
        }
    }

    override fun stop() {
        try {
            mediaRecorder?.apply {
                stop()
                release()
            }
        } catch (_: Exception) {
            // stop() can throw when recorder was not fully initialized.
        } finally {
            mediaRecorder = null
        }
    }

    override fun getMaxAmplitude(): Int {
        return try {
            mediaRecorder?.maxAmplitude ?: 0
        } catch (_: Exception) {
            0
        }
    }
}
