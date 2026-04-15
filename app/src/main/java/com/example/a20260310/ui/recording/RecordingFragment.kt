package com.example.a20260310.ui.recording

import android.Manifest
import android.content.pm.PackageManager
import android.os.Bundle
import android.view.View
import android.widget.TextView
import android.widget.Toast
import androidx.core.app.ActivityCompat
import androidx.fragment.app.Fragment
import androidx.fragment.app.viewModels
import androidx.navigation.fragment.findNavController
import com.example.a20260310.R
import com.example.a20260310.viewmodel.RecordingViewModel
import com.google.android.material.button.MaterialButton
import com.google.android.material.floatingactionbutton.FloatingActionButton

class RecordingFragment : Fragment(R.layout.fragment_recording) {
    private val viewModel: RecordingViewModel by viewModels()
    private var recordingFilePath: String? = null

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        val timer = view.findViewById<TextView>(R.id.timer)
        val recordBtn = view.findViewById<MaterialButton>(R.id.recordButton)
        val doneFab = view.findViewById<FloatingActionButton>(R.id.doneFab)
        recordingFilePath = "${requireContext().filesDir}/recording.m4a"

        ensureAudioPermission()

        viewModel.uiState.observe(viewLifecycleOwner) { state ->
            val h = state.elapsedSeconds / 3600
            val m = (state.elapsedSeconds % 3600) / 60
            val s = state.elapsedSeconds % 60
            timer.text = String.format("%02d:%02d:%02d", h, m, s)
            recordBtn.text = if (state.isRecording) "STOP" else "REC"
            doneFab.isEnabled = !state.isRecording
        }

        viewModel.uploadUiState.observe(viewLifecycleOwner) { uploadState ->
            if (uploadState.isUploading) {
                doneFab.isEnabled = false
                doneFab.alpha = 0.5f
                return@observe
            }

            doneFab.alpha = 1.0f
            doneFab.isEnabled = true

            if (uploadState.isSuccess) {
                Toast.makeText(
                    requireContext(),
                    "업로드 완료 (meeting_id=${uploadState.meetingId})",
                    Toast.LENGTH_SHORT,
                ).show()
                val args = Bundle().apply {
                    putLong("meeting_id", uploadState.meetingId ?: -1L)
                    putString("transcript_text", uploadState.transcriptText ?: "")
                }
                viewModel.consumeUploadState()
                findNavController().navigate(
                    R.id.action_recordingFragment_to_summaryFragment,
                    args,
                )
            } else if (!uploadState.errorMessage.isNullOrBlank()) {
                Toast.makeText(requireContext(), uploadState.errorMessage, Toast.LENGTH_LONG).show()
                viewModel.consumeUploadState()
            }
        }

        recordBtn.setOnClickListener {
            if (!hasAudioPermission()) {
                ensureAudioPermission()
                return@setOnClickListener
            }
            val path = recordingFilePath ?: return@setOnClickListener
            viewModel.toggleRecording(outputPath = path)
        }

        doneFab.setOnClickListener {
            val path = recordingFilePath
            if (path.isNullOrBlank()) {
                Toast.makeText(requireContext(), "녹음 파일 경로를 찾을 수 없습니다.", Toast.LENGTH_SHORT).show()
                return@setOnClickListener
            }
            viewModel.stopAndUploadRecording(path)
        }
    }

    private fun hasAudioPermission(): Boolean {
        return ActivityCompat.checkSelfPermission(
            requireContext(),
            Manifest.permission.RECORD_AUDIO,
        ) == PackageManager.PERMISSION_GRANTED
    }

    private fun ensureAudioPermission() {
        if (!hasAudioPermission()) {
            requestPermissions(arrayOf(Manifest.permission.RECORD_AUDIO), 0)
        }
    }
}
