package com.mirzamirror.app.ui.theme

import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.darkColorScheme
import androidx.compose.material3.lightColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.ui.graphics.Color

private val DarkColorScheme = darkColorScheme(
    primary = Color(0xFF90CAF9),
    secondary = Color(0xFF81D4FA),
    tertiary = Color(0xFFB39DDB),
    background = Color(0xFF121212),
    surface = Color(0xFF1E1E1E),
    onPrimary = Color(0xFF000000),
    onSecondary = Color(0xFF000000),
    onTertiary = Color(0xFF000000),
    onBackground = Color(0xFFFFFFFF),
    onSurface = Color(0xFFFFFFFF),
)

private val LightColorScheme = lightColorScheme(
    primary = Color(0xFF2196F3),
    secondary = Color(0xFF03A9F4),
    tertiary = Color(0xFF673AB7),
    background = Color(0xFFFAFAFA),
    surface = Color(0xFFFFFFFF),
    onPrimary = Color(0xFFFFFFFF),
    onSecondary = Color(0xFFFFFFFF),
    onTertiary = Color(0xFFFFFFFF),
    onBackground = Color(0xFF000000),
    onSurface = Color(0xFF000000),
)

@Composable
fun MirzaMirrorTheme(
    darkTheme: Boolean = isSystemInDarkTheme(),
    content: @Composable () -> Unit
) {
    val colorScheme = if (darkTheme) {
        DarkColorScheme
    } else {
        LightColorScheme
    }

    MaterialTheme(
        colorScheme = colorScheme,
        typography = Typography,
        content = content
    )
}
