package com.curio.thecurator

import android.content.Context
import android.content.Intent
import android.graphics.Color
import android.os.Build
import android.os.Environment
import android.os.VibrationEffect
import android.os.Vibrator
import android.os.VibratorManager
import android.util.Base64
import android.webkit.JavascriptInterface
import android.widget.Toast
import java.io.File
import java.io.FileOutputStream

class CurioAndroidBridge(private val activity: MainActivity) {

    private val vibrator: Vibrator? by lazy {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.S) {
            val vibratorManager = activity.getSystemService(Context.VIBRATOR_MANAGER_SERVICE) as? VibratorManager
            vibratorManager?.defaultVibrator
        } else {
            @Suppress("DEPRECATION")
            activity.getSystemService(Context.VIBRATOR_SERVICE) as? Vibrator
        }
    }

    @JavascriptInterface
    fun triggerHaptic(type: String?) {
        val v = vibrator ?: return
        if (!v.hasVibrator()) return

        activity.runOnUiThread {
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.Q) {
                val effect = when (type) {
                    "heavy" -> VibrationEffect.createPredefined(VibrationEffect.EFFECT_HEAVY_CLICK)
                    "medium" -> VibrationEffect.createPredefined(VibrationEffect.EFFECT_DOUBLE_CLICK)
                    "light" -> VibrationEffect.createPredefined(VibrationEffect.EFFECT_TICK)
                    else -> VibrationEffect.createPredefined(VibrationEffect.EFFECT_CLICK)
                }
                v.vibrate(effect)
            } else {
                @Suppress("DEPRECATION")
                val millis = when (type) {
                    "heavy" -> 50L
                    "medium" -> 30L
                    else -> 15L
                }
                v.vibrate(millis)
            }
        }
    }

    @JavascriptInterface
    fun showToast(message: String?) {
        if (message.isNullOrBlank()) return
        activity.runOnUiThread {
            Toast.makeText(activity, message, Toast.LENGTH_SHORT).show()
        }
    }

    @JavascriptInterface
    fun shareText(title: String?, text: String?, url: String?) {
        activity.runOnUiThread {
            val sendIntent = Intent().apply {
                action = Intent.ACTION_SEND
                val shareBody = buildString {
                    if (!title.isNullOrBlank()) appendLine(title)
                    if (!text.isNullOrBlank()) appendLine(text)
                    if (!url.isNullOrBlank()) appendLine(url)
                }.trim()
                putExtra(Intent.EXTRA_TEXT, shareBody)
                putExtra(Intent.EXTRA_TITLE, title ?: "CURIO")
                type = "text/plain"
            }
            val chooser = Intent.createChooser(sendIntent, title ?: "Share from CURIO")
            activity.startActivity(chooser)
        }
    }

    @JavascriptInterface
    fun saveZipExport(base64Data: String?, filename: String?) {
        if (base64Data.isNullOrBlank()) return
        val targetName = if (filename.isNullOrBlank()) "curio_backup_${System.currentTimeMillis()}.zip" else filename

        activity.runOnUiThread {
            try {
                val cleanBase64 = if (base64Data.contains(",")) base64Data.substringAfter(",") else base64Data
                val bytes = Base64.decode(cleanBase64, Base64.DEFAULT)

                val downloadsDir = Environment.getExternalStoragePublicDirectory(Environment.DIRECTORY_DOWNLOADS)
                val destFile = File(downloadsDir, targetName)
                FileOutputStream(destFile).use { it.write(bytes) }

                Toast.makeText(activity, "Saved to Downloads: $targetName", Toast.LENGTH_LONG).show()
            } catch (e: Exception) {
                Toast.makeText(activity, "Export error: ${e.message}", Toast.LENGTH_SHORT).show()
            }
        }
    }

    @JavascriptInterface
    fun updateSystemBars(hexColor: String?, isDark: Boolean) {
        if (hexColor.isNullOrBlank()) return
        activity.runOnUiThread {
            try {
                val color = Color.parseColor(hexColor)
                activity.window.statusBarColor = color
                activity.window.navigationBarColor = color
            } catch (e: Exception) {
                // Ignore parsing errors for unsupported theme gradients
            }
        }
    }
}
