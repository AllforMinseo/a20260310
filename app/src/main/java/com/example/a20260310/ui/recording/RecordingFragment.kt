package com.example.a20260310.ui.recording

import android.Manifest
import android.content.pm.PackageManager
import android.os.Bundle
import android.util.Log
import android.view.View
import android.widget.TextView
import androidx.core.app.ActivityCompat
import androidx.fragment.app.Fragment
import androidx.fragment.app.viewModels
import androidx.navigation.fragment.findNavController
import com.example.a20260310.R
<<<<<<< Updated upstream
=======
import com.example.a20260310.viewmodel.MeetingSessionViewModel
>>>>>>> Stashed changes
import com.example.a20260310.viewmodel.RecordingViewModel
import com.google.android.material.button.MaterialButton
import com.google.android.material.floatingactionbutton.FloatingActionButton
import java.io.File
import java.text.SimpleDateFormat
<<<<<<< Updated upstream
import java.util.Date
import java.util.Locale
=======
import java.util.*

fun getCurrentFileName(): String {
    val sdf = SimpleDateFormat("yyyyMMdd_HHmmss", Locale.getDefault())
    return "moa_${sdf.format(Date())}.m4a"
}
>>>>>>> Stashed changes

fun getCurrentFileName(): String {
    val sdf = SimpleDateFormat("yyyyMMdd_HHmmss", Locale.getDefault())
    val currentTime = sdf.format(Date())
    return "moa_$currentTime.m4a"
}
class RecordingFragment : Fragment(R.layout.fragment_recording) {

    private val viewModel: RecordingViewModel by viewModels()

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        val timer = view.findViewById<TextView>(R.id.timer)
<<<<<<< Updated upstream
        val recordBtn = view.findViewById<MaterialButton>(R.id.recordButton)
        val doneFab = view.findViewById<FloatingActionButton>(R.id.doneFab)

        ensureAudioPermission()

=======
        val title = view.findViewById<TextView>(R.id.title)
        val recordBtn = view.findViewById<MaterialButton>(R.id.recordButton)

        ensureAudioPermission()

        // ✅ 회의 제목 표시 (ViewModel)
        sessionViewModel.meetingDraft.observe(viewLifecycleOwner) {
            title.text = it.title
        }

>>>>>>> Stashed changes
        viewModel.uiState.observe(viewLifecycleOwner) { state ->
            val h = state.elapsedSeconds / 3600
            val m = (state.elapsedSeconds % 3600) / 60
            val s = state.elapsedSeconds % 60
            timer.text = String.format("%02d:%02d:%02d", h, m, s)
            recordBtn.text = if (state.isRecording) "STOP" else "REC"
        }

        recordBtn.setOnClickListener {

            if (!hasAudioPermission()) {
                ensureAudioPermission()
                return@setOnClickListener
            }

<<<<<<< Updated upstream
            val prefs = requireContext().getSharedPreferences("moa_prefs", 0)
            val meetingName = prefs.getString("current_meeting_name", null)
            //Log.d("MOA_DEBUG", "회의 이름: $meetingName")
=======
            val meetingName = sessionViewModel.meetingDraft.value?.title ?: "회의"
>>>>>>> Stashed changes

            val fileName = getCurrentFileName()
            val file = File(requireContext().filesDir, fileName)

<<<<<<< Updated upstream
            //파일명 → 회의이름 매핑 저장
            prefs.edit().putString(fileName, meetingName).apply()

            viewModel.toggleRecording(outputPath = file.absolutePath)
        }

        doneFab.setOnClickListener {
            viewModel.stopRecording()
            findNavController().navigate(R.id.action_recordingFragment_to_summaryFragment)
=======
            // 🔥 파일명 → 회의이름 매핑
            val prefs = requireContext().getSharedPreferences("moa_prefs", 0)
            prefs.edit().putString(fileName, meetingName).apply()

            viewModel.toggleRecording(outputPath = file.absolutePath)
>>>>>>> Stashed changes
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