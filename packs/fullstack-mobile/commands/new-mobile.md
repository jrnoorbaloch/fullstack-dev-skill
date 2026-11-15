---
description: Build a mobile app for Android and iOS (Expo / React Native or Flutter)
argument-hint: "<app idea, screens, backend>"
---
Use the fullstack-mobile skill to build this mobile app: $ARGUMENTS

1. Plan screens, navigation, data and backend. Default: Expo + Expo Router from `templates/expo-app`; use Flutter if asked.
2. Scaffold with `scripts/scaffold.py expo-app <dir>`, then build every screen with loading/empty/error states (`references/mobile.md`).
3. Run `npm install && npx expo install --fix && npx tsc --noEmit` and fix errors.
4. Explain how to test in Expo Go and how to build an APK / Play Store / App Store release with EAS.
