package com.example.a20260310.ui.add

import android.os.Bundle
import android.view.View
import android.widget.Toast
import androidx.fragment.app.Fragment
import androidx.navigation.fragment.findNavController
import com.example.a20260310.R
import com.google.android.material.button.MaterialButton
import com.google.android.material.card.MaterialCardView

class AddMethodFragment : Fragment(R.layout.fragment_add_method) {
    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        view.findViewById<MaterialCardView>(R.id.cardRecord).setOnClickListener {
            findNavController().navigate(R.id.action_addMethodFragment_to_recordingFragment)
        }
        view.findViewById<MaterialCardView>(R.id.cardUploadAudio).setOnClickListener {
            Toast.makeText(requireContext(), "녹음 파일 업로드: 더미", Toast.LENGTH_SHORT).show()
        }
        view.findViewById<MaterialCardView>(R.id.cardCapture).setOnClickListener {
            Toast.makeText(requireContext(), "촬영하기: 더미", Toast.LENGTH_SHORT).show()
        }
        view.findViewById<MaterialCardView>(R.id.cardUploadText).setOnClickListener {
            Toast.makeText(requireContext(), "텍스트 파일 업로드: 더미", Toast.LENGTH_SHORT).show()
        }

        view.findViewById<MaterialButton>(R.id.nextButton).setOnClickListener {
            Toast.makeText(requireContext(), "다음: 더미", Toast.LENGTH_SHORT).show()
        }
    }
}
