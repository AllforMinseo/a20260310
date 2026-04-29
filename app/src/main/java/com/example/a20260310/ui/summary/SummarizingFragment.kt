package com.example.a20260310.ui.summary

import android.os.Bundle
import android.view.View
import android.widget.Toast
import androidx.fragment.app.Fragment
import androidx.fragment.app.activityViewModels
import androidx.lifecycle.lifecycleScope
import androidx.navigation.fragment.findNavController
import com.example.a20260310.R
import com.example.a20260310.viewmodel.MeetingSessionViewModel
import kotlinx.coroutines.launch

class SummarizingFragment : Fragment(R.layout.fragment_summarizing) {
    private val sessionViewModel: MeetingSessionViewModel by activityViewModels()

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        if (!sessionViewModel.hasSelectedFilesForSummary()) {
            Toast.makeText(requireContext(), "요약할 파일이 없습니다.", Toast.LENGTH_SHORT).show()
            findNavController().popBackStack()
            return
        }

        viewLifecycleOwner.lifecycleScope.launch {
            try {
                sessionViewModel.awaitSummarizeSelectedFiles()
                findNavController().navigate(R.id.action_summarizingFragment_to_summaryFragment)
            } catch (e: Exception) {
                Toast.makeText(
                    requireContext(),
                    e.message ?: getString(R.string.summarizing_error_generic),
                    Toast.LENGTH_LONG,
                ).show()
                findNavController().popBackStack()
            }
        }
    }
}
