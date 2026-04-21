package com.example.a20260310.ui.summary

import android.os.Bundle
import android.view.View
import android.widget.TextView
import androidx.fragment.app.Fragment
import androidx.navigation.fragment.findNavController
import com.example.a20260310.R
import com.google.android.material.button.MaterialButton

class SummaryFragment : Fragment(R.layout.fragment_summary) {
    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        val titleView = view.findViewById<TextView>(R.id.title)
        val summaryTextView = view.findViewById<TextView>(R.id.summaryText)

        val meetingId = arguments?.getLong("meeting_id", -1L) ?: -1L
        val transcript = arguments?.getString("transcript_text").orEmpty()

        if (meetingId > 0L) {
            titleView.text = "회의 요약 #$meetingId"
        }

        if (transcript.isNotBlank()) {
            summaryTextView.text = buildSegmentedText(transcript)
        }

        view.findViewById<MaterialButton>(R.id.closeButton).setOnClickListener {
            findNavController().navigate(R.id.action_summaryFragment_to_addCompleteFragment)
        }
    }

    private fun buildSegmentedText(transcript: String): String {
        val segments = transcript
            .replace("\n", " ")
            .split(Regex("(?<=[.!?])\\s+"))
            .map { it.trim() }
            .filter { it.isNotBlank() }

        if (segments.isEmpty()) return transcript

        return buildString {
            append("세그먼트 (${segments.size})\n\n")
            segments.forEachIndexed { index, segment ->
                append("${index + 1}. $segment\n\n")
            }
        }.trim()
    }
}
