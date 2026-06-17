# VisionBook Android App

This folder wraps the static HTML book as a bundled Capacitor Android WebView app.

## Build

```powershell
cd mobile
npm install
npm run build:apk
```

The generated APK is copied to:

```text
dist/android/visionbook.apk
```

The APK is debug-signed for sideload testing. The GitHub release workflow builds the same artifact and attaches it to a release.
