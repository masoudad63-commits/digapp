[app]
title = DigApp
package.name = digapp
package.domain = org.example
source.dir = .
source.include_exts = py,png,jpg,kv,ttf
version = 1.0
requirements = python3,kivy,pillow
orientation = portrait
fullscreen = 0
android.permissions = WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
android.api = 33
android.minapi = 21
android.sdk = 33
android.ndk = 25b
android.arch = arm64-v8a,armeabi-v7a
source.include_patterns = assets/**/*,Vazir.ttf
log_level = 2
warn_on_root = 1

[buildozer]
bin_dir = bin
