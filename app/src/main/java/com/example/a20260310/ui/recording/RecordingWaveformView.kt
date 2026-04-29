package com.example.a20260310.ui.recording

import android.content.Context
import android.graphics.Canvas
import android.graphics.Paint
import android.util.AttributeSet
import android.view.View
import kotlin.math.max
import kotlin.math.min

class RecordingWaveformView @JvmOverloads constructor(
    context: Context,
    attrs: AttributeSet? = null,
) : View(context, attrs) {

    private val barPaint = Paint(Paint.ANTI_ALIAS_FLAG).apply {
        color = 0xFFEFB26EL.toInt()
        style = Paint.Style.FILL
        strokeCap = Paint.Cap.ROUND
    }

    private val centerLinePaint = Paint(Paint.ANTI_ALIAS_FLAG).apply {
        color = 0xFFF45B5EL.toInt()
        style = Paint.Style.FILL
    }

    private val amplitudes = ArrayDeque<Float>()
    private val maxBars = 42

    fun updateAmplitude(amplitude: Int, isRecording: Boolean) {
        val normalized = if (isRecording) {
            min(1f, max(0f, amplitude / 32767f))
        } else {
            0f
        }

        if (amplitudes.size >= maxBars) {
            amplitudes.removeFirst()
        }
        amplitudes.addLast(normalized)
        invalidate()
    }

    override fun onDraw(canvas: Canvas) {
        super.onDraw(canvas)
        if (width == 0 || height == 0) return

        val centerX = width / 2f
        canvas.drawRect(centerX - 2f, 0f, centerX + 2f, height.toFloat(), centerLinePaint)

        val list = amplitudes.toList()
        val count = list.size
        if (count == 0) return

        val barWidth = 6f
        val gap = 6f
        val padFromCenter = 8f

        // 최신 샘플이 기준선 바로 왼쪽에 붙고, 과거 샘플만 왼쪽으로 흐름
        var x = centerX - padFromCenter - barWidth
        for (i in count - 1 downTo 0) {
            val amp = list[i]
            val minBar = 12f
            val maxBar = height * 0.85f
            val barHeight = minBar + (maxBar - minBar) * amp
            val top = (height - barHeight) / 2f
            val bottom = top + barHeight

            if (x + barWidth > 0f) {
                canvas.drawRoundRect(x, top, x + barWidth, bottom, 4f, 4f, barPaint)
            }
            x -= (barWidth + gap)
            if (x + barWidth < 0f) break
        }
    }
}
