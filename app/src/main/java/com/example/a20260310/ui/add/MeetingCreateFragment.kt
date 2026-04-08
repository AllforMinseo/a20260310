package com.example.a20260310.ui.add

import android.os.Bundle
import android.view.View
import android.widget.Toast
import androidx.fragment.app.Fragment
import androidx.navigation.fragment.findNavController
import com.example.a20260310.R
import com.google.android.material.button.MaterialButton

import com.google.android.material.textfield.TextInputEditText
import java.text.SimpleDateFormat
import java.util.*


class MeetingCreateFragment : Fragment(R.layout.fragment_meeting_create) {
    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        val nameInput = view.findViewById<TextInputEditText>(R.id.nameInput)
        val dateInput = view.findViewById<TextInputEditText>(R.id.dateInput)
        val timeInput = view.findViewById<TextInputEditText>(R.id.timeInput)

        val currentDate = SimpleDateFormat("yyyy.MM.dd", Locale.getDefault()).format(Date())
        val currentTime = SimpleDateFormat("HH:mm", Locale.getDefault()).format(Date())

        nameInput.setText(currentDate)
        dateInput.setText(currentDate)
        timeInput.setText(currentTime)

        view.findViewById<MaterialButton>(R.id.addInfoButton).setOnClickListener {
            Toast.makeText(requireContext(), "회의 정보 추가: 더미", Toast.LENGTH_SHORT).show()
        }

        view.findViewById<MaterialButton>(R.id.nextButton).setOnClickListener {
            findNavController().navigate(R.id.action_meetingCreateFragment_to_addMethodFragment)
        }
    }
}

