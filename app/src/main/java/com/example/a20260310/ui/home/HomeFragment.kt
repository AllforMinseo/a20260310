package com.example.a20260310.ui.home

import android.content.Context
import android.os.Bundle
import android.view.View
import androidx.fragment.app.Fragment
import androidx.navigation.fragment.findNavController
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.example.a20260310.R
import com.example.a20260310.data.model.SimpleRow
import com.example.a20260310.ui.common.SimpleRowAdapter
import com.google.android.material.button.MaterialButton

import java.io.File

fun getRecordingList(context: Context): List<SimpleRow> {
    val dir = context.filesDir
    val files = dir.listFiles()
    val prefs = context.getSharedPreferences("moa_prefs", 0)

    val list = mutableListOf<SimpleRow>()

    files?.filter { it.name.endsWith(".m4a") }?.forEach { file ->

        val meetingName = prefs.getString(file.name, file.name)

        list.add(
            SimpleRow(
                title = meetingName ?: file.name,
                subtitle = "file name : "+file.name +"\n"+ "file size : "+"${file.length() / 1024} KB"
            )
        )
    }

    return list.sortedByDescending { it.title }
}

class HomeFragment : Fragment(R.layout.fragment_home) {
    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        val items = getRecordingList(requireContext())

        view.findViewById<RecyclerView>(R.id.recycler).apply {
            layoutManager = LinearLayoutManager(context)
            adapter = SimpleRowAdapter(items)
        }

        view.findViewById<MaterialButton>(R.id.addMeetingButton).setOnClickListener {
            findNavController().navigate(R.id.action_homeFragment_to_folderSelectFragment)
        }
    }
}
