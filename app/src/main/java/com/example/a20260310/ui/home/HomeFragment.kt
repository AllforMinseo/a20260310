package com.example.a20260310.ui.home

import android.content.Context
import android.os.Bundle
import android.view.View
import androidx.fragment.app.Fragment
import androidx.fragment.app.activityViewModels
import androidx.navigation.fragment.findNavController
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.example.a20260310.R
import com.example.a20260310.data.model.MeetingDraft
import com.example.a20260310.data.model.SimpleRow
import com.example.a20260310.ui.common.SimpleRowAdapter
import com.example.a20260310.viewmodel.MeetingSessionViewModel
import com.google.android.material.button.MaterialButton
<<<<<<< Updated upstream
import java.text.SimpleDateFormat
import java.util.*
import java.io.File

fun getRecordingList(context: Context): List<SimpleRow> {
    val dir = context.filesDir
    val files = dir.listFiles()
    val prefs = context.getSharedPreferences("moa_prefs", 0)

    val list = mutableListOf<SimpleRow>()

    val sdf = SimpleDateFormat("yyyy년 M월 d일         a HH:mm", Locale.KOREA)

    files?.filter { it.name.endsWith(".m4a") }?.forEach { file ->

        val meetingName = prefs.getString(file.name, file.name)

        val date = Date(file.lastModified())
        val formattedDate = sdf.format(date)

        list.add(
            SimpleRow(
                title = meetingName ?: file.name,
                subtitle = "file name : "+file.name +"\n"+ "file size : "+"${file.length() / 1024} KB"
            )
        )
    }

    return files
        ?.filter { it.name.endsWith(".m4a") }
        ?.sortedByDescending { it.lastModified() }
        ?.map { file ->
            val meetingName = prefs.getString(file.name, file.name)
            val formattedDate = sdf.format(Date(file.lastModified()))

            SimpleRow(
                title = meetingName ?: file.name,
                subtitle = formattedDate
            )
        } ?: emptyList()
}
=======
import com.google.android.material.textfield.TextInputEditText
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale

class MeetingCreateFragment : Fragment(R.layout.fragment_meeting_create) {

    private val sessionViewModel: MeetingSessionViewModel by activityViewModels()
>>>>>>> Stashed changes

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

<<<<<<< Updated upstream
        val items = getRecordingList(requireContext())
=======
        val nameInput = view.findViewById<TextInputEditText>(R.id.nameInput)
        val dateInput = view.findViewById<TextInputEditText>(R.id.dateInput)
        val timeInput = view.findViewById<TextInputEditText>(R.id.timeInput)
>>>>>>> Stashed changes

        val currentDate = SimpleDateFormat("yyyy.MM.dd", Locale.getDefault()).format(Date())
        val currentTime = SimpleDateFormat("HH:mm", Locale.getDefault()).format(Date())

        if (nameInput.text.isNullOrEmpty()) {
            nameInput.setText(currentDate)
        }

        dateInput.setText(currentDate)
        timeInput.setText(currentTime)

        view.findViewById<MaterialButton>(R.id.nextButton).setOnClickListener {

            sessionViewModel.setDraft(
                MeetingDraft(
                    title = nameInput.text.toString(),
                    date = dateInput.text.toString(),
                    time = timeInput.text.toString()
                )
            )

            findNavController().navigate(R.id.action_meetingCreateFragment_to_addMethodFragment)
        }
    }
}
