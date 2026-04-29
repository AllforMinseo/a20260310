package com.example.a20260310.ui.home

import android.content.Context
import android.os.Bundle
import android.view.View
import android.widget.LinearLayout
import androidx.fragment.app.Fragment
import androidx.navigation.fragment.findNavController
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.example.a20260310.R
import com.example.a20260310.data.model.SimpleRow
import com.example.a20260310.ui.common.SimpleRowAdapter
import com.google.android.material.button.MaterialButton
import java.io.File
import java.text.SimpleDateFormat
import java.util.*

class HomeFragment : Fragment(R.layout.fragment_home) {

    private lateinit var recycler: RecyclerView
    private var selectedFolder = "전체"

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        recycler = view.findViewById(R.id.recycler)

        recycler.layoutManager = LinearLayoutManager(context)

        setupFolderTabs(view)

        loadList()

        view.findViewById<MaterialButton>(R.id.addMeetingButton).setOnClickListener {
            findNavController().navigate(R.id.action_homeFragment_to_folderSelectFragment)
        }
    }

    private fun setupFolderTabs(view: View) {
        val container = view.findViewById<LinearLayout>(R.id.folderTabs)
        container.removeAllViews()

        val folders = loadFolders(requireContext())

        folders.forEach { name ->
            val btn = MaterialButton(requireContext()).apply {
                text = name
                setOnClickListener {
                    selectedFolder = name
                    loadList()
                }
            }
            container.addView(btn)
        }
    }


    private fun loadFolders(context: Context): List<String> {
        val prefs = context.getSharedPreferences("moa_prefs", 0)
        val folders = prefs.getStringSet("folder_list", setOf()) ?: setOf()

        return listOf("전체") + folders
    }

    private fun loadList() {
        val items = if (selectedFolder == "전체") {
            getAllFiles(requireContext())
        } else {
            getFilesInFolder(requireContext(), selectedFolder)
        }

        recycler.adapter = SimpleRowAdapter(items)
    }
}

// 📁 폴더 목록
fun getFolders(context: Context): List<File> {
    val baseDir = File(context.filesDir, "MOA")
    return baseDir.listFiles()?.filter { it.isDirectory } ?: emptyList()
}

// 📁 폴더 내부 파일
fun getFilesInFolder(context: Context, folderName: String): List<SimpleRow> {

    val folder = File(context.filesDir, "MOA/$folderName")
    val prefs = context.getSharedPreferences("moa_prefs", 0)

    return folder.listFiles()
        ?.filter { it.name.endsWith(".m4a") }
        ?.sortedByDescending { it.lastModified() }
        ?.map {
            val title = prefs.getString(it.name, it.name)
            val date = SimpleDateFormat("yyyy년 M월 d일 a HH:mm", Locale.KOREA)
                .format(Date(it.lastModified()))

            SimpleRow(title ?: it.name, date)
        } ?: emptyList()
}

// 📁 전체 파일
fun getAllFiles(context: Context): List<SimpleRow> {

    val folders = getFolders(context)
    val prefs = context.getSharedPreferences("moa_prefs", 0)

    val allFiles = mutableListOf<File>()

    folders.forEach {
        it.listFiles()?.let { list -> allFiles.addAll(list) }
    }

    return allFiles
        .filter { it.name.endsWith(".m4a") }
        .sortedByDescending { it.lastModified() }
        .map {
            val title = prefs.getString(it.name, it.name)
            val date = SimpleDateFormat("yyyy년 M월 d일 a HH:mm", Locale.KOREA)
                .format(Date(it.lastModified()))

            SimpleRow(title ?: it.name, date)
        }
}