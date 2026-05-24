# 🎵 MusicApp — Python Backend Server

A **FastAPI** backend server that powers the MusicApp Flutter client. Handles user authentication, song uploads to **Cloudinary**, music catalog management, and favorites — all backed by a **PostgreSQL** database via **SQLAlchemy**.

---

## 📁 Project Structure

```
server/
├── main.py                          # FastAPI app entry point, router registration, DB init
├── database.py                      # PostgreSQL connection, SQLAlchemy engine & session
├── requirements.txt                 # All Python dependencies
├── .env                             # Environment variables (not committed)
│
├── models/                          # SQLAlchemy ORM table definitions
│   ├── base.py                      # declarative_base() shared by all models
│   ├── user.py                      # User table (id, name, email, hashed password)
│   ├── song.py                      # Song table (id, song_url, thumbnail_url, artist, song_name, hex_code)
│   └── favorite.py                  # Favorites join table (user_id FK → users, song_id FK → songs)
│
├── pydantic_schemas/                # Request body validation schemas
│   ├── user_create.py               # { name, email, password }
│   ├── user_login.py                # { email, password }
│   └── favorite_song.py             # { song_id }
│
├── routes/                          # API route handlers
│   ├── auth.py                      # /auth — signup, login, get current user
│   └── song.py                      # /song — upload, list, favorite, list favorites
│
└── middleware/
    └── auth_middleware.py           # JWT token verification (x-auth-token header)
```

---

## ✨ Features

- 🔐 **User Auth** — Signup with bcrypt-hashed passwords; login returns a signed JWT token
- 🛡️ **JWT Middleware** — All protected routes validated via `x-auth-token` header using `PyJWT`
- ☁️ **Cloudinary Upload** — Audio files and thumbnail images uploaded directly to Cloudinary; public URLs stored in PostgreSQL
- 🎵 **Song Catalog** — Full CRUD-style song management with artist name, hex color code, and media URLs
- ❤️ **Favorites** — Toggle-based favorite system; adds or removes a row in the `favorites` join table
- 🗄️ **PostgreSQL + SQLAlchemy** — Relational data with ORM models, relationships, and `joinedload` for efficient querying
- ⚡ **FastAPI** — Auto-generated `/docs` (Swagger UI) and `/redoc` out of the box

---

## 🛠️ Tech Stack

| Concern | Technology |
|---|---|
| Web Framework | **FastAPI** |
| Database | **PostgreSQL** |
| ORM | **SQLAlchemy** |
| Data Validation | **Pydantic** v2 |
| Password Hashing | **bcrypt** |
| Authentication | **PyJWT** (HS256) |
| File / Media Storage | **Cloudinary** |
| Server | **Uvicorn** (ASGI) |
| Python Version | **3.11** |

---

## 🗄️ Database Schema

```
┌─────────────┐        ┌──────────────────┐        ┌──────────────┐
│    users     │        │    favorites      │        │    songs     │
│─────────────│        │──────────────────│        │──────────────│
│ id (PK, TEXT)│◄──────│ user_id (FK)      │        │ id (PK, TEXT)│
│ name        │        │ id (PK, TEXT)     │───────►│ song_name    │
│ email       │        │ song_id (FK)      │        │ artist       │
│ password    │        └──────────────────┘        │ song_url     │
│ (LargeBinary│                                     │ thumbnail_url│
│  bcrypt)    │                                     │ hex_code     │
└─────────────┘                                     └──────────────┘
```

- `User` ↔ `Favorite` → one-to-many (`User.favorites` relationship)
- `Favorite` ↔ `Song` → many-to-one (`Favorite.song` relationship)
- All primary keys are **UUID v4** strings

---

## 📡 API Endpoints

### Auth Routes — `/auth`

| Method | Endpoint | Auth Required | Description |
|---|---|---|---|
| `POST` | `/auth/signup` | ❌ | Register new user; hashes password with bcrypt; returns `User` object |
| `POST` | `/auth/login` | ❌ | Validates email + bcrypt password; returns `{ token, user }` |
| `GET` | `/auth/` | ✅ | Returns current user data with favorites (eager-loaded via `joinedload`) |

### Song Routes — `/song`

| Method | Endpoint | Auth Required | Description |
|---|---|---|---|
| `POST` | `/song/upload` | ✅ | Multipart upload: audio file + thumbnail → Cloudinary; saves URLs to DB |
| `GET` | `/song/list` | ✅ | Returns all songs in the catalog |
| `POST` | `/song/favorite` | ✅ | Toggle favorite: creates or deletes a `Favorite` row; returns `{ message: true/false }` |
| `GET` | `/song/list/favorites` | ✅ | Returns current user's favorited songs with song details eager-loaded |

> **Authentication:** Pass the JWT in the `x-auth-token` request header.

---

## 🔐 Auth Flow

```
Client                          Server
  │                               │
  │── POST /auth/signup ─────────►│  bcrypt.hashpw(password)
  │                               │  INSERT INTO users
  │◄── 201 { user } ─────────────│
  │                               │
  │── POST /auth/login ──────────►│  bcrypt.checkpw(password, hash)
  │                               │  jwt.encode({ id: user.id }, 'password_key')
  │◄── 200 { token, user } ──────│
  │                               │
  │── GET /auth/  ───────────────►│  auth_middleware: jwt.decode(x_auth_token)
  │   x-auth-token: <jwt>         │  → extract uid → query user + favorites
  │◄── 200 { user + favorites } ─│
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.11+
- PostgreSQL (running locally or remote)
- A [Cloudinary](https://cloudinary.com/) account (free tier works)

### 1. Clone & Navigate

```bash
git clone https://github.com/Strange-Leader/musicapp.git
cd musicapp/server
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate        # macOS / Linux
venv\Scripts\activate           # Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up PostgreSQL

Create the database:

```sql
CREATE DATABASE fluttermusicapp;
```

### 5. Configure the Database URL

Update `database.py` with your PostgreSQL credentials:

```python
DATABASE_URL = 'postgresql://<user>:<password>@localhost:5432/fluttermusicapp'
```

> ⚠️ For production, move this to a `.env` file and load it with `python-dotenv`. Never commit credentials.

### 6. Configure Cloudinary

Update the config block in `routes/song.py` with your own Cloudinary credentials:

```python
cloudinary.config(
    cloud_name = "your_cloud_name",
    api_key    = "your_api_key",
    api_secret = "your_api_secret",
    secure=True
)
```

> ⚠️ Move these to environment variables before deploying.

### 7. Run the Server

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

SQLAlchemy will auto-create all tables (`users`, `songs`, `favorites`) on startup via:

```python
Base.metadata.create_all(engine)
```

The API will be live at **`http://localhost:8000`**

---

## 📖 Auto-Generated API Docs

FastAPI provides interactive documentation out of the box — no setup needed:

| UI | URL |
|---|---|
| Swagger UI | `http://localhost:8000/docs` |
| ReDoc | `http://localhost:8000/redoc` |

---

## 📦 Requirements (`requirements.txt`)

| Package | Purpose |
|---|---|
| `fastapi` | Web framework — routing, dependency injection, request validation |
| `uvicorn` | ASGI server to run FastAPI |
| `sqlalchemy` | ORM — models, relationships, sessions, queries |
| `psycopg2-binary` | PostgreSQL database driver for SQLAlchemy |
| `bcrypt` | Password hashing for secure credential storage |
| `PyJWT` | JWT creation (`jwt.encode`) and verification (`jwt.decode`) |
| `cloudinary` | SDK for uploading audio and thumbnail files to Cloudinary CDN |
| `python-multipart` | Required by FastAPI to handle `multipart/form-data` file uploads |
| `pydantic` | Request body validation schemas (`UserCreate`, `UserLogin`, `FavoriteSong`) |

Install all with:

```bash
pip install -r requirements.txt
```

---

## 📂 Cloudinary Storage Structure

When a song is uploaded, both files are stored under a shared folder keyed by UUID:

```
cloudinary/
└── songs/
    └── <song_uuid>/
        ├── <audio_file>       ← resource_type='auto'
        └── <thumbnail_image>  ← resource_type='image'
```

The public URLs returned by Cloudinary are stored directly in the `songs` table (`song_url`, `thumbnail_url`) and streamed by the Flutter client.

---

## 🔗 Related

- [Client README](../client/README.md) — Flutter app setup and architecture
- [Root README](../README.md) — Full project overview