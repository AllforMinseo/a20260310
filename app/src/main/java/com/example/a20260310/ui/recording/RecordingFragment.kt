package com.example.a20260310.ui.recording

import android.Manifest
import android.content.pm.PackageManager
import android.media.AudioFormat
import android.media.AudioRecord
import android.media.MediaRecorder
import android.os.Bundle
import android.os.Handler
import android.os.Looper
import android.view.View
import android.widget.TextView
import androidx.fragment.app.Fragment
import androidx.core.app.ActivityCompat
import androidx.navigation.fragment.findNavController
import com.example.a20260310.R
import com.google.android.material.floatingactionbutton.FloatingActionButton
import com.google.android.material.button.MaterialButton
import java.io.File
import java.io.FileOutputStream

class RecordingFragment : Fragment(R.layout.fragment_recording) {
    private val handler = Handler(Looper.getMainLooper())
    private var seconds = 0
    //private var running = true
    private var ticker: Runnable? = null

    //private var audioRecord: AudioRecord? = null
    private var mediaRecorder: MediaRecorder? = null
    private var isRecording = false
    private lateinit var recordingThread: Thread

    private lateinit var filePath: String

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        val timer = view.findViewById<TextView>(R.id.timer)
        val recordBtn = view.findViewById<MaterialButton>(R.id.recordButton)
        val doneFab = view.findViewById<FloatingActionButton>(R.id.doneFab)

        //권한 체크
        if (ActivityCompat.checkSelfPermission(
                requireContext(),
                Manifest.permission.RECORD_AUDIO
            ) != PackageManager.PERMISSION_GRANTED
        ) {
            requestPermissions(arrayOf(Manifest.permission.RECORD_AUDIO), 0)
        }

        val tick = object : Runnable {
            override fun run() {
                if (isRecording) {
                    seconds += 1
                    val h = seconds / 3600
                    val m = (seconds % 3600) / 60
                    val s = seconds % 60
                    timer.text = String.format("%02d:%02d:%02d", h, m, s)
                }
                handler.postDelayed(this, 1000)
            }
        }
        ticker = tick
        handler.postDelayed(tick, 1000)

        // 파일 경로
        val pcmPath = "${requireContext().filesDir}/recording.pcm"
        val wavPath = "${requireContext().filesDir}/recording.wav"

        // ✅ 녹음 버튼
        recordBtn.setOnClickListener {
            if (ActivityCompat.checkSelfPermission(
                    requireContext(),
                    Manifest.permission.RECORD_AUDIO
                ) != PackageManager.PERMISSION_GRANTED
            ) {
                requestPermissions(arrayOf(Manifest.permission.RECORD_AUDIO), 0)
                return@setOnClickListener   // 🔥 여기 중요
            }
            if (!isRecording) {
                startRecording()
                recordBtn.text = "STOP"
            } else {
                stopRecording()
                recordBtn.text = "REC"
            }
        }

        // ✅ 완료 버튼
        doneFab.setOnClickListener {
            findNavController().navigate(R.id.action_recordingFragment_to_summaryFragment)
        }

//        view.findViewById<FloatingActionButton>(R.id.doneFab).setOnClickListener {
//            findNavController().navigate(R.id.action_recordingFragment_to_summaryFragment)
//        }
    }

    // 🎙 녹음 시작
    private fun startRecording() {
        filePath = "/sdcard/Download/recording.m4a"

        mediaRecorder = MediaRecorder().apply {
            setAudioSource(MediaRecorder.AudioSource.MIC)
            setOutputFormat(MediaRecorder.OutputFormat.MPEG_4)
            setAudioEncoder(MediaRecorder.AudioEncoder.AAC)
            setOutputFile(filePath)
            prepare()
            start()
        }

        isRecording = true
    }

//    // 📁 PCM 저장
//    private fun writeAudioDataToFile(filePath: String, bufferSize: Int) {
//        val data = ByteArray(bufferSize)
//        val outputStream = FileOutputStream(filePath)
//
//        while (isRecording) {
//            val read = audioRecord?.read(data, 0, bufferSize) ?: 0
//            if (read > 0) {
//                outputStream.write(data, 0, read)
//            }
//        }
//
//        outputStream.close()
//    }

    // ⏹ 녹음 종료 + WAV 변환
    private fun stopRecording() {
        try {
            mediaRecorder?.apply {
                stop()
                release()
            }
        } catch (e: Exception) {
            e.printStackTrace()
        }

        mediaRecorder = null
        isRecording = false

        println("녹음 종료됨, 저장 위치: $filePath")
    }

//    // 🔥 PCM → WAV 변환
//    private fun convertPcmToWav(pcmPath: String, wavPath: String) {
//        val pcmFile = File(pcmPath)
//        val wavFile = File(wavPath)
//
//        val pcmData = pcmFile.readBytes()
//        val wavOutput = FileOutputStream(wavFile)
//
//        val totalDataLen = pcmData.size + 36
//        val byteRate = 44100 * 2
//
//        val header = ByteArray(44)
//
//        header[0] = 'R'.code.toByte()
//        header[1] = 'I'.code.toByte()
//        header[2] = 'F'.code.toByte()
//        header[3] = 'F'.code.toByte()
//
//        header[4] = (totalDataLen and 0xff).toByte()
//        header[5] = ((totalDataLen shr 8) and 0xff).toByte()
//
//        header[8] = 'W'.code.toByte()
//        header[9] = 'A'.code.toByte()
//        header[10] = 'V'.code.toByte()
//        header[11] = 'E'.code.toByte()
//
//        header[12] = 'f'.code.toByte()
//        header[13] = 'm'.code.toByte()
//        header[14] = 't'.code.toByte()
//        header[15] = ' '.code.toByte()
//
//        header[16] = 16
//        header[20] = 1
//        header[22] = 1
//
//        val sampleRate = 44100
//        header[24] = (sampleRate and 0xff).toByte()
//        header[25] = ((sampleRate shr 8) and 0xff).toByte()
//
//        header[28] = (byteRate and 0xff).toByte()
//        header[29] = ((byteRate shr 8) and 0xff).toByte()
//
//        header[32] = 2
//        header[34] = 16
//
//        header[36] = 'd'.code.toByte()
//        header[37] = 'a'.code.toByte()
//        header[38] = 't'.code.toByte()
//        header[39] = 'a'.code.toByte()
//
//        val dataSize = pcmData.size
//        header[40] = (dataSize and 0xff).toByte()
//        header[41] = ((dataSize shr 8) and 0xff).toByte()
//
//        wavOutput.write(header)
//        wavOutput.write(pcmData)
//        wavOutput.close()
//    }

    override fun onDestroyView() {
        ticker?.let { handler.removeCallbacks(it) }
        ticker = null
        super.onDestroyView()
    }
}

