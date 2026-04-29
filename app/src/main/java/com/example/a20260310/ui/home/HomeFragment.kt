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
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale

class HomeFragment : Fragment(R.layout.fragment_home) {
    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        fun getRecordingList(context: Context): List<SimpleRow> {

            val dir = context.filesDir
            val prefs = context.getSharedPreferences("moa_prefs", 0)

            val sdf = SimpleDateFormat("yyyy년 M월 d일 a HH:mm", Locale.KOREA)

            return dir.listFiles()
                ?.filter { it.name.endsWith(".m4a") }
                ?.sortedByDescending { it.lastModified() }
                ?.map { file ->

                    val meetingName = prefs.getString(file.name, file.name)
                    val date = sdf.format(Date(file.lastModified()))

                    SimpleRow(
                        title = meetingName ?: file.name,
                        subtitle = date
                    )
                } ?: emptyList()
        }

        // 🔥 이거 추가해야 함
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
