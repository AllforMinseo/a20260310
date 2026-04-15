package com.example.a20260310.ui.summary

import android.os.Bundle
import android.view.View
import androidx.fragment.app.Fragment
import androidx.navigation.fragment.findNavController
import com.example.a20260310.R
import com.google.android.material.button.MaterialButton

class SummaryFragment : Fragment(R.layout.fragment_summary) {
    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        view.findViewById<MaterialButton>(R.id.closeButton).setOnClickListener {
            findNavController().navigate(R.id.action_summaryFragment_to_addCompleteFragment)
        }
    }
}
