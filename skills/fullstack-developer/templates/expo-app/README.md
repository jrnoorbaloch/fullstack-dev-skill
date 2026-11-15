# Expo (React Native) App Starter

Tabs navigation (Expo Router), light/dark theme, offline list stored on device, Supabase client ready.

## Setup
```bash
npm install
npx expo install --fix      # aligns native package versions with your Expo SDK
cp .env.example .env        # optional: Supabase keys
npx expo start              # scan the QR code with Expo Go
```

## Build
```bash
npm i -g eas-cli && eas login
eas build -p android --profile preview      # installable APK
eas build -p android --profile production   # AAB for Play Store
eas build -p ios --profile production       # needs Apple Developer account
```
Change `name`, `slug`, `android.package` and `ios.bundleIdentifier` in `app.json` first.
