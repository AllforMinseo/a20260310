package com.example.a20260310.ui.add

import android.os.Bundle
import android.view.View
import android.widget.Toast
import androidx.fragment.app.Fragment
import androidx.navigation.fragment.findNavController
import com.example.a20260310.R
import com.google.android.material.button.MaterialButton

class MeetingCreateFragment : Fragment(R.layout.fragment_meeting_create) {
    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        view.findViewById<MaterialButton>(R.id.addInfoButton).setOnClickListener {
            Toast.makeText(requireContext(), "회의 정보 추가: 더미", Toast.LENGTH_SHORT).show()
        }

        view.findViewById<MaterialButton>(R.id.nextButton).setOnClickListener {
            findNavController().navigate(R.id.action_meetingCreateFragment_to_addMethodFragment)
        }
    }
}

