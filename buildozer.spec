[app]
title = "Panel Aim Pro"
package.name = panelaimpro
package.domain = com.panelaim.pro
source.dir = .
source.include_exts = py,png,jpg,kv,json
version = 1.0.2

requirements = python3,kivy==2.2.1
android.permissions = INTERNET,FOREGROUND_SERVICE,SYSTEM_ALERT_WINDOW
android.api = 31
android.minapi = 26
android.ndk = "25b"
android.sdk = 33
android.ndk_api = 26

orientation = sensor
fullscreen = 0
android.arch = arm64-v8a

[buildozer]
build_dir = ./.buildozer
log_level = 2
warn_on_root = 0
build_timeout = 1800
