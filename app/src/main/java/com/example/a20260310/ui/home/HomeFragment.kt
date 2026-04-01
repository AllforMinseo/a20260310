package com.example.a20260310.ui.home

import android.os.Bundle
import android.view.View
import androidx.fragment.app.Fragment
import androidx.navigation.fragment.findNavController
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.example.a20260310.R
import com.example.a20260310.ui.common.SimpleRow
import com.example.a20260310.ui.common.SimpleRowAdapter
import com.google.android.material.button.MaterialButton

class HomeFragment : Fragment(R.layout.fragment_home) {
    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        val items = listOf(
            SimpleRow(title = "2026.03.04 주간 회의", subtitle = "2026-03-04 • 30분 • 더미"),
            SimpleRow(title = "2026.03.10 주간 회의", subtitle = "2026-03-10 • 42분 • 더미"),
            SimpleRow(title = "2026.03.17 주간 회의", subtitle = "2026-03-17 • 25분 • 더미"),
        )

        view.findViewById<RecyclerView>(R.id.recycler).apply {
            layoutManager = LinearLayoutManager(context)
            adapter = SimpleRowAdapter(items)
        }

        view.findViewById<MaterialButton>(R.id.addMeetingButton).setOnClickListener {
            findNavController().navigate(R.id.action_homeFragment_to_folderSelectFragment)
        }
    }
}

