# 🎵 MusicApp — Flutter Client

A cross-platform **Flutter** music streaming client for Android (and desktop). Lets users sign up, log in, browse all songs, upload their own tracks, favorite songs, and stream music — all with a persistent background audio player and lock-screen controls.

---

## 📁 Project Structure

```
client/
├── android/
│   └── app/src/main/AndroidManifest.xml   # Permissions + AudioService config
├── lib/
│   ├── main.dart                           # App entry point & provider bootstrapping
│   ├── core/
│   │   ├── constants/
│   │   │   └── server_constant.dart        # Base server URL config
│   │   ├── failure/
│   │   │   └── failure.dart               # AppFailure error model
│   │   ├── models/
│   │   │   └── user_model.dart            # UserModel (name, email, token, favorites)
│   │   ├── providers/
│   │   │   ├── current_user_notifier.dart  # Global logged-in user state
│   │   │   └── current_song_notifier.dart  # Global now-playing state + AudioPlayer
│   │   ├── theme/
│   │   │   ├── app_pallete.dart           # App color palette (dark Spotify-like theme)
│   │   │   └── theme.dart                 # MaterialApp dark theme config
│   │   ├── utils.dart                     # Utility helpers (e.g. rgbToHex)
│   │   └── widgets/
│   │       ├── custom_field.dart          # Reusable styled text field
│   │       └── loader.dart               # Loading spinner widget
│   └── features/
│       ├── auth/
│       │   ├── repositories/
│       │   │   ├── auth_remote_repository.dart  # signup / login / getCurrentUser API
│       │   │   └── auth_local_repository.dart   # JWT token persistence (SharedPreferences)
│       │   ├── view/pages/
│       │   │   ├── login_page.dart
│       │   │   └── signup_page.dart
│       │   ├── view/widgets/
│       │   │   └── auth_gradient_button.dart
│       │   └── viewmodel/
│       │       └── auth_viewmodel.dart          # signUp / login / getData logic
│       └── home/
│           ├── models/
│           │   ├── song_model.dart              # SongModel (id, name, artist, urls, hex_code)
│           │   └── fav_song_model.dart          # FavSongModel (id, song_id, user_id)
│           ├── repositories/
│           │   ├── home_repository.dart         # uploadSong / getAllSongs / favSong / getFavSongs API
│           │   └── home_local_repository.dart   # Recently played songs cache (Hive)
│           ├── view/pages/
│           │   ├── home_page.dart              # Root page with bottom nav
│           │   ├── songs_page.dart             # All songs grid + player
│           │   ├── library_page.dart           # Favorites library
│           │   └── upload_song_page.dart       # Upload audio + thumbnail form
│           ├── view/widgets/
│           │   ├── music_player.dart           # Full-screen music player widget
│           │   ├── music_slab.dart             # Mini player slab (bottom bar)
│           │   └── audio_wave.dart             # Animated audio waveform
│           └── viewmodel/
│               └── home_viewmodel.dart         # uploadSong / getAllSongs / favSong logic
└── pubspec.yaml
```

---

## ✨ Features

- 🔐 **Authentication** — Sign up and log in with JWT token; token persisted across app restarts via `SharedPreferences`
- 🎵 **Browse Songs** — Fetch and display the full music catalog from the server
- ⬆️ **Upload Songs** — Upload an audio file + thumbnail image with song name, artist, and a custom color picker
- ❤️ **Favorites** — Toggle favorite on any song; favorites synced to the backend and shown in the Library tab
- 🕐 **Recently Played** — Last-played songs stored locally using Hive for instant offline access
- 🎧 **Background Playback** — Full background audio via `just_audio` + `just_audio_background` with Android lock-screen media controls
- 🔊 **Play / Pause / Seek** — Full player controls including seek bar and animated waveform
- 🌙 **Dark Theme** — Spotify-inspired dark UI with purple-to-pink gradient accents

---

## 🛠️ Tech Stack

| Concern | Technology |
|---|---|
| Framework | Flutter (Dart) |
| State Management | Riverpod (`riverpod_annotation`, code-generated) |
| Audio Playback | `just_audio` + `just_audio_background` |
| HTTP Client | `http` package |
| Local Storage (token) | `shared_preferences` |
| Local Storage (songs cache) | `hive` |
| Error Handling | `fpdart` (`Either<AppFailure, T>`) |
| Architecture | MVVM — View → ViewModel → Repository |

---

## 🏗️ Architecture

The app follows a clean **MVVM + Repository** pattern:

```
View (Pages & Widgets)
    │
    ▼
ViewModel (Riverpod Notifiers)   ←──  Manages async state (AsyncValue)
    │
    ▼
Repository
    ├── Remote Repository   ──────►  Python Backend API (HTTP)
    └── Local Repository    ──────►  Hive / SharedPreferences
```

- **`fpdart`** `Either` type is used across all repository calls — errors return `Left(AppFailure)`, success returns `Right(data)` — keeping the ViewModel clean with Dart's `switch` pattern.
- **Riverpod** providers are code-generated via `riverpod_annotation` (`.g.dart` files).
- **`CurrentSongNotifier`** holds the global `AudioPlayer` instance and drives the mini slab + full player.
- **`CurrentUserNotifier`** holds the logged-in `UserModel` (including the favorites list) globally.

---

## 🌐 API Consumed

The client talks to a Python backend at `http://10.0.2.2:8000` (Android emulator) or `http://127.0.0.1:8000` (other platforms).

| Method | Endpoint | Description | Auth |
|---|---|---|---|
| `POST` | `/auth/signup` | Register a new user | ❌ |
| `POST` | `/auth/login` | Login and receive JWT token | ❌ |
| `GET` | `/auth/` | Get current user data | ✅ `x-auth-token` |
| `POST` | `/song/upload` | Upload audio + thumbnail (multipart) | ✅ |
| `GET` | `/song/list` | Get all songs | ✅ |
| `POST` | `/song/favorite` | Toggle favorite a song | ✅ |
| `GET` | `/song/list/favorites` | Get user's favorited songs | ✅ |

> Auth is handled via a custom `x-auth-token` header containing the JWT returned at login.

---

## 🚀 Getting Started

### Prerequisites

- Android Studio + Android Emulator **or** a physical Android device
- The [MusicApp server](../server/README.md) running on port `8000`

### Installation

```bash
# Clone the repo and navigate to the client
cd client

# Install all Flutter dependencies
flutter pub get

# Generate Riverpod boilerplate (run if .g.dart files are missing)
dart run build_runner build --delete-conflicting-outputs
```

### Server URL Configuration

The base URL is defined in `lib/core/constants/server_constant.dart`:

```dart
class ServerConstant {
  static String serverURL =
      Platform.isAndroid ? 'http://10.0.2.2:8000' : 'http://127.0.0.1:8000';
}
```

- **Android Emulator** → `10.0.2.2` maps to your host machine's `localhost`
- **Physical device** → Replace with your machine's local IP (e.g. `http://192.168.1.5:8000`)

### Running the App

```bash
# Run on Android emulator or connected device
flutter run

# Run on a specific device
flutter run -d <device-id>

# List available devices
flutter devices
```

### Building for Release

```bash
# Android APK
flutter build apk --release

# Android App Bundle (recommended for Play Store)
flutter build appbundle --release
```

---

## 📱 Android Permissions

Declared in `AndroidManifest.xml`:

| Permission | Purpose |
|---|---|
| `INTERNET` | API communication with the server |
| `READ_MEDIA_AUDIO` | Picking audio files from device storage |
| `READ_EXTERNAL_STORAGE` | Legacy storage access |
| `FOREGROUND_SERVICE` | Keeping audio alive in the background |
| `FOREGROUND_SERVICE_MEDIA_PLAYBACK` | Media-type foreground service |
| `WAKE_LOCK` | Prevent CPU sleep during playback |
| `RECORD_AUDIO` | Audio-related native plugin requirement |

The app uses `com.ryanheise.audioservice` for the Android `MediaBrowserService` and `MediaButtonReceiver`, enabling lock-screen controls and headphone button support.

---

## 📦 Key Dependencies

| Package | Purpose |
|---|---|
| `flutter_riverpod` + `riverpod_annotation` | State management + code generation |
| `just_audio` | Audio playback engine |
| `just_audio_background` | Background playback + media notifications |
| `http` | REST API calls |
| `hive` | Local NoSQL cache for recently played songs |
| `shared_preferences` | Persistent JWT token storage |
| `fpdart` | Functional `Either` type for error handling |
| `path_provider` | App documents directory (Hive setup) |

> See `pubspec.yaml` for exact versions.

---

## 🔗 Related

- [Server README](../server/README.md) — Python backend setup
- [Root README](../README.md) — Full project overview