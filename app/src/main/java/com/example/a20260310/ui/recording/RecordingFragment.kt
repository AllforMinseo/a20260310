package com.example.a20260310.ui.recording

import android.Manifest
import android.content.pm.PackageManager
import android.os.Bundle
import android.view.View
import android.widget.TextView
import android.widget.Toast
import androidx.core.app.ActivityCompat
import androidx.fragment.app.Fragment
import androidx.fragment.app.activityViewModels
import androidx.fragment.app.viewModels
import androidx.navigation.fragment.findNavController
import com.example.a20260310.R
import com.example.a20260310.viewmodel.MeetingSessionViewModel
import com.example.a20260310.viewmodel.RecordingViewModel
import com.example.a20260310.viewmodel.SelectedSourceFile
import com.google.android.material.button.MaterialButton
import java.io.File
import java.text.SimpleDateFormat
import java.util.*

fun getCurrentFileName(): String {
    val sdf = SimpleDateFormat("yyyyMMdd_HHmmss", Locale.getDefault())
    return "moa_${sdf.format(Date())}.m4a"
}

class RecordingFragment : Fragment(R.layout.fragment_recording) {

    private val viewModel: RecordingViewModel by viewModels()
    private val sessionViewModel: MeetingSessionViewModel by activityViewModels()
    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        val timer = view.findViewById<TextView>(R.id.timer)
        val title = view.findViewById<TextView>(R.id.title)
        val recordBtn = view.findViewById<MaterialButton>(R.id.recordButton)
        val waveformView = view.findViewById<RecordingWaveformView>(R.id.waveformView)

        ensureAudioPermission()

        // ✅ 회의 제목 표시 (ViewModel)
        sessionViewModel.meetingDraft.observe(viewLifecycleOwner) {
            title.text = it.title
        }

        viewModel.uiState.observe(viewLifecycleOwner) { state ->
            val h = state.elapsedSeconds / 3600
            val m = (state.elapsedSeconds % 3600) / 60
            val s = state.elapsedSeconds % 60
            timer.text = String.format("%02d:%02d:%02d", h, m, s)
            //recordBtn.text = if (state.isRecording) "STOP" else "REC"
            waveformView.updateAmplitude(state.amplitude, state.isRecording)
        }

        var currentRecordingFile: File? = null

        recordBtn.setOnClickListener {

            if (!hasAudioPermission()) {
                ensureAudioPermission()
                return@setOnClickListener
            }

            val isRecording = viewModel.uiState.value?.isRecording == true

            if (isRecording) {
                // 🔴 녹음 종료
                viewModel.stopRecording()

                val file = currentRecordingFile

                if (file != null && file.exists()) {

                    sessionViewModel.addSelectedFile(
                        SelectedSourceFile(
                            type = SelectedSourceFile.Type.AUDIO_RECORD,
                            displayName = sessionViewModel.meetingDraft.value?.title ?: "녹음",
                            localPath = file.absolutePath
                        )
                    )

                    findNavController().navigate(
                        R.id.action_recordingFragment_to_summarizingFragment
                    )
                } else {
                    Toast.makeText(requireContext(), "녹음 파일이 없습니다", Toast.LENGTH_SHORT).show()
                }

            } else {
                // 🟢 녹음 시작
                val meetingName = sessionViewModel.meetingDraft.value?.title ?: "회의"

                val fileName = getCurrentFileName()
                val file = File(requireContext().filesDir, fileName)

                currentRecordingFile = file  // 🔥 중요

                val prefs = requireContext().getSharedPreferences("moa_prefs", 0)
                prefs.edit().putString(fileName, meetingName).apply()

                viewModel.toggleRecording(outputPath = file.absolutePath)
            }
        }
    }

    private fun hasAudioPermission() =
        ActivityCompat.checkSelfPermission(
            requireContext(),
            Manifest.permission.RECORD_AUDIO
        ) == PackageManager.PERMISSION_GRANTED

    private fun ensureAudioPermission() {
        if (!hasAudioPermission()) {
            requestPermissions(arrayOf(Manifest.permission.RECORD_AUDIO), 0)
        }
    }
}