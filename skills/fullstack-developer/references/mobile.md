# Mobile apps (Android & iOS)

## Choose
- Default: **React Native + Expo (TypeScript) + Expo Router**.
- User asks for Flutter → Flutter + Dart (Riverpod/Bloc, go_router).
- Native only on request: Kotlin + Jetpack Compose (Android), Swift + SwiftUI (iOS).

## Expo scaffold
```
npx create-expo-app@latest my-app
cd my-app && npx expo start
```
Structure:
```
app/(tabs)/_layout.tsx, index.tsx, profile.tsx
app/(auth)/login.tsx, signup.tsx
components/, hooks/, lib/ (api.ts, supabase.ts), constants/theme.ts
```
- Styling: NativeWind (Tailwind for RN) or StyleSheet with a theme file.
- State/data: Zustand + TanStack Query. Forms: react-hook-form + zod.
- Storage: expo-secure-store for tokens, AsyncStorage/MMKV for cache, expo-sqlite for offline data.
- Backend: Supabase (auth + db + storage) or the project's own API.
- Common modules: expo-image-picker, expo-camera, expo-location, expo-notifications, expo-av.

## UX checklist
- Safe areas, keyboard-avoiding forms, pull-to-refresh, loading/empty/error states.
- Bottom tabs for main sections; stack navigation for details.
- Dark mode via `useColorScheme`. RTL: `I18nManager.forceRTL(true)` for Urdu/Arabic.
- Touch targets ≥ 44px; test on small (360px) and large screens.

## Build & publish
```
npm i -g eas-cli && eas login
eas build:configure
eas build -p android --profile preview     # APK for testing
eas build -p android --profile production  # AAB for Play Store
eas build -p ios --profile production      # needs Apple Developer account
eas submit -p android | ios
```
Set `app.json`: name, slug, icon, splash, `android.package`, `ios.bundleIdentifier`, permissions text.
