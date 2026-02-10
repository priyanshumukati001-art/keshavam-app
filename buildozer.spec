name: Build APK
on: [push, pull_request]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

    - name: Build APK with Buildozer
        uses: ArtemSBulgakov/buildozer-action@v1
        with:
          save_buildozer_config: false
      - name: Upload APK
        uses: actions/upload-artifact@v4
        with:
          name: Keshavam-Mobile-App
          path: bin/*.apk
