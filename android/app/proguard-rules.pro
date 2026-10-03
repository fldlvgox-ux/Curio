# Proguard rules for CURIO
-keepattributes JavascriptInterface
-keepclassmembers class * {
    @android.webkit.JavascriptInterface <methods>;
}
-keepclassmembers class com.curio.thecurator.CurioAndroidBridge {
    <methods>;
}
