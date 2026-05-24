# 🎵 MusicApp

A full-stack music streaming application built with a **Flutter** cross-platform client and a **FastAPI + PostgreSQL** backend. Users can sign up, log in, upload songs with thumbnails, stream music with background playback and lock-screen controls, and manage their favorites library — all in a sleek dark-themed UI.

---

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│                   Flutter Client (Dart)                  │
│                                                          │
│  Auth Pages ──► AuthViewModel ──► AuthRemoteRepository  │
│  Home Pages ──► HomeViewModel ──► HomeRepository        │
│  Music Player ◄─ CurrentSongNotifier (just_audio)       │
│  Token Cache  ◄─ SharedPreferences                      │
│  Song Cache   ◄─ Hive (recently played)                 │
└────────────────────┬────────────────────────────────────┘
                     │  HTTP REST  (x-auth-token JWT header)
                     ▼
┌─────────────────────────────────────────────────────────┐
│               FastAPI Server (Python 3.11)               │
│                                                          │
│  /auth ──► bcrypt hash ──► PyJWT token                  │
│  /song ──► Cloudinary upload ──► PostgreSQL URL store   │
│  JWT auth_middleware on all protected routes             │
└──────────┬───────────────────────┬──────────────────────┘
           │                       │
           ▼                       ▼
   PostgreSQL DB            Cloudinary CDN
  (users, songs,           (audio files +
   favorites)               thumbnails)
```

---

## 📁 Repository Structure

```
musicapp/
├── client/                  # Flutter mobile app (Dart)
│   ├── android/             # Android manifest + AudioService config
│   └── lib/
│       ├── core/            # Theme, models, shared providers, constants
│       └── features/
│           ├── auth/        # Signup / Login pages, viewmodel, repositories
│           └── home/        # Songs, Upload, Library, Player widgets & logic
│
├── server/                  # FastAPI Python backend
│   ├── main.py              # App entry, router registration, DB table init
│   ├── database.py          # PostgreSQL engine & session factory
│   ├── requirements.txt     # Python dependencies
│   ├── models/              # SQLAlchemy ORM — User, Song, Favorite
│   ├── pydantic_schemas/    # Request validation — UserCreate, UserLogin, FavoriteSong
│   ├── routes/              # API handlers — auth.py, song.py
│   └── middleware/          # JWT auth_middleware
│
├── .gitignore               # Ignores server/.env
└── README.md
```

---

## ✨ Key Features

- 🔐 **JWT Authentication** — Signup/login with bcrypt-hashed passwords; token persisted on device across sessions
- 🎵 **Music Streaming** — Stream audio directly from Cloudinary CDN via `just_audio`
- ⬆️ **Song Upload** — Upload audio + thumbnail image with artist name and custom color; stored on Cloudinary
- ❤️ **Favorites** — Toggle favorites synced to the backend; viewable in a personal Library tab
- 🎧 **Background Playback** — Lock-screen media controls and persistent notification on Android via `just_audio_background` + `AudioService`
- 🕐 **Recently Played** — Last-played songs cached locally with Hive for instant offline access
- 🌙 **Dark UI** — Spotify-inspired dark theme with purple-to-pink gradient accents

---

## 🛠️ Full Tech Stack

| Layer | Technology |
|---|---|
| **Client Framework** | Flutter (Dart) |
| **State Management** | Riverpod (`riverpod_annotation`) |
| **Audio Playback** | `just_audio` + `just_audio_background` |
| **Client HTTP** | `http` package |
| **Local Storage** | `shared_preferences` (token), `hive` (song cache) |
| **Error Handling** | `fpdart` (`Either<AppFailure, T>`) |
| **Server Framework** | FastAPI (Python 3.11) |
| **Database** | PostgreSQL |
| **ORM** | SQLAlchemy |
| **Password Security** | bcrypt |
| **Auth Token** | PyJWT (HS256) |
| **Media Storage** | Cloudinary CDN |
| **ASGI Server** | Uvicorn |

---

## 📡 API Reference

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| `POST` | `/auth/signup` | ❌ | Register new user |
| `POST` | `/auth/login` | ❌ | Login → returns `{ token, user }` |
| `GET` | `/auth/` | ✅ | Get current user + favorites |
| `POST` | `/song/upload` | ✅ | Upload audio + thumbnail (multipart) |
| `GET` | `/song/list` | ✅ | List all songs |
| `POST` | `/song/favorite` | ✅ | Toggle favorite a song |
| `GET` | `/song/list/favorites` | ✅ | Get user's favorited songs |

> All protected routes require the `x-auth-token: <jwt>` header.

---

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/Strange-Leader/musicapp.git
cd musicapp
```

### 2. Start the Server

```bash
cd server
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
# Configure PostgreSQL URL in database.py and Cloudinary keys in routes/song.py
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

> Full setup details → [server/README.md](./server/README.md)

### 3. Run the Flutter Client

```bash
cd client
flutter pub get
dart run build_runner build --delete-conflicting-outputs
flutter run
```

> Full setup details → [client/README.md](./client/README.md)

---

## 📖 Detailed Documentation

| Document | Description |
|---|---|
| [client/README.md](./client/README.md) | Flutter architecture, folder structure, dependencies, Android permissions, running & building |
| [server/README.md](./server/README.md) | FastAPI setup, DB schema, Cloudinary config, all endpoints, auth flow, requirements |

---

## 📬 Author

Built by [Strange-Leader](https://github.com/Strange-Leader)

---

## 📝 License

This project is open source and available under the [MIT License](LICENSE).