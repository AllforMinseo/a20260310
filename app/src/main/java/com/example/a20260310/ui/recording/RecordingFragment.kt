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
import com.example.a20260310.viewmodel.SelectedSourceFile
import com.example.a20260310.viewmodel.MeetingSessionViewModel
import com.example.a20260310.viewmodel.RecordingViewModel
import com.google.android.material.button.MaterialButton
import java.io.File

class RecordingFragment : Fragment(R.layout.fragment_recording) {
    private val viewModel: RecordingViewModel by viewModels()
    private val sessionViewModel: MeetingSessionViewModel by activityViewModels()

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        val timer = view.findViewById<TextView>(R.id.timer)
        val title = view.findViewById<TextView>(R.id.title)
        val waveformView = view.findViewById<RecordingWaveformView>(R.id.waveformView)
        val recordBtn = view.findViewById<MaterialButton>(R.id.recordButton)
        val summarizeButton = view.findViewById<MaterialButton>(R.id.summarizeButton)

        ensureAudioPermission()

        sessionViewModel.meetingDraft.observe(viewLifecycleOwner) { d ->
            val t = d.title.trim()
            if (t.isNotEmpty()) title.text = t
        }

        viewModel.uiState.observe(viewLifecycleOwner) { state ->
            val h = state.elapsedSeconds / 3600
            val m = (state.elapsedSeconds % 3600) / 60
            val s = state.elapsedSeconds % 60
            timer.text = String.format("%02d:%02d:%02d", h, m, s)
            recordBtn.icon = null
            recordBtn.setIconResource(
                if (state.isRecording) R.drawable.moa_rectangle else R.drawable.moa_play,
            )
            waveformView.updateAmplitude(state.amplitude, state.isRecording)
        }

        val audioFile = File(
            requireContext().getExternalFilesDir(null),
            "moa_recording.m4a",
        )

        val finishRecordingAndBack = View.OnClickListener {
            if (!hasAudioPermission()) {
                ensureAudioPermission()
                return@OnClickListener
            }
            viewModel.stopRecording()
            if (!audioFile.exists() || audioFile.length() == 0L) {
                Toast.makeText(
                    requireContext(),
                    "녹음 파일이 없습니다. 녹음한 뒤 다시 시도해 주세요.",
                    Toast.LENGTH_SHORT,
                ).show()
                return@OnClickListener
            }
            sessionViewModel.addSelectedFile(
                SelectedSourceFile(
                    type = SelectedSourceFile.Type.AUDIO_RECORD,
                    displayName = "녹음",
                    localPath = audioFile.absolutePath,
                ),
            )
            Toast.makeText(requireContext(), "녹음 파일이 추가되었습니다.", Toast.LENGTH_SHORT).show()
            findNavController().popBackStack()
        }

        summarizeButton.setOnClickListener(finishRecordingAndBack)

        recordBtn.setOnClickListener {
            if (!hasAudioPermission()) {
                ensureAudioPermission()
                return@setOnClickListener
            }
            viewModel.toggleRecording(outputPath = audioFile.absolutePath)
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
