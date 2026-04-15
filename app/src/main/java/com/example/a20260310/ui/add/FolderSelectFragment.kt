package com.example.a20260310.ui.add

import android.os.Bundle
import android.view.View
import android.widget.Toast
import androidx.fragment.app.Fragment
import androidx.navigation.fragment.findNavController
import com.example.a20260310.R
import com.google.android.material.button.MaterialButton

class FolderSelectFragment : Fragment(R.layout.fragment_folder_select) {
    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        view.findViewById<MaterialButton>(R.id.nextButton).setOnClickListener {
            Toast.makeText(requireContext(), "폴더 선택: 더미", Toast.LENGTH_SHORT).show()
            findNavController().navigate(R.id.action_folderSelectFragment_to_meetingCreateFragment)
        }
    }
}
