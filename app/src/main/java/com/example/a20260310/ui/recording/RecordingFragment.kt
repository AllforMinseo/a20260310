package com.example.a20260310.ui.recording

import android.os.Bundle
import android.os.Handler
import android.os.Looper
import android.view.View
import android.widget.TextView
import androidx.fragment.app.Fragment
import androidx.navigation.fragment.findNavController
import com.example.a20260310.R
import com.google.android.material.floatingactionbutton.FloatingActionButton

class RecordingFragment : Fragment(R.layout.fragment_recording) {
    private val handler = Handler(Looper.getMainLooper())
    private var seconds = 8 * 60 + 25
    private var running = true
    private var ticker: Runnable? = null

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        val timer = view.findViewById<TextView>(R.id.timer)
        val tick = object : Runnable {
            override fun run() {
                if (running) {
                    seconds += 1
                    val h = seconds / 3600
                    val m = (seconds % 3600) / 60
                    val s = seconds % 60
                    timer.text = String.format("%02d:%02d:%02d", h, m, s)
                }
                handler.postDelayed(this, 1000)
            }
        }
        ticker = tick
        handler.postDelayed(tick, 1000)

        view.findViewById<FloatingActionButton>(R.id.doneFab).setOnClickListener {
            findNavController().navigate(R.id.action_recordingFragment_to_summaryFragment)
        }
    }

    override fun onDestroyView() {
        ticker?.let { handler.removeCallbacks(it) }
        ticker = null
        super.onDestroyView()
    }
}

