# 📝 Markdown Notes API

A comprehensive RESTful API for managing Markdown notes with advanced features including grammar checking, revision history, and rendered content delivery.


## 📑 Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Database Setup](#database-setup)
- [Running the Application](#running-the-application)
- [Features Guide](#features-guide)
  - [3.1 Notes CRUD & Revision History](#31-notes-crud--revision-history)
  - [3.2 Grammar & Style Checking](#32-grammar--style-checking)
  - [3.3 Rendered Content Delivery](#33-rendered-content-delivery)
- [API Documentation](#api-documentation)
- [Testing](#testing)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

---

## ✨ Features

### ✅ Core Features
- **User Authentication**: JWT-based authentication system
- **Notes Management**: Full CRUD operations for Markdown notes
- **Tagging System**: Organize notes with custom tags
- **Soft Delete**: Restore deleted notes
- **Search & Filter**: Find notes by tags and content

### 🚀 Advanced Features

#### **3.1 Revision History**
- Automatic versioning on note updates
- Browse complete revision history
- Restore previous versions
- Track all changes over time

#### **3.2 Grammar & Style Checking**
- Integration with LanguageTool API
- Detect spelling, grammar, and style issues
- Selective fix application
- Store and retrieve issue history

#### **3.3 Rendered Content Delivery**
- Markdown to HTML conversion
- XSS protection with HTML sanitization
- HTTP caching with ETag support
- Content negotiation (HTML/JSON)
- Raw HTML endpoint for embedding

---

## 🛠 Tech Stack

### Backend
- **Framework**: FastAPI 0.104+
- **Database**: PostgreSQL 14+
- **ORM**: SQLAlchemy 2.0 (Async)
- **Migrations**: Alembic
- **Authentication**: JWT (python-jose)
- **Password Hashing**: bcrypt

### Features
- **Grammar Checking**: LanguageTool API
- **Markdown Processing**: python-markdown 3.5.1
- **HTML Sanitization**: bleach 6.1.0
- **HTTP Client**: httpx 0.25.2

### Development
- **API Testing**: Swagger UI (built-in)
- **Code Style**: Python 3.12+
- **Environment**: python-dotenv

---

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.12+** ([Download](https://www.python.org/downloads/))
- **PostgreSQL 14+** ([Download](https://www.postgresql.org/download/))
- **pip** (comes with Python)
- **Git** ([Download](https://git-scm.com/downloads))

---

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/markdown-notes-api.git
cd markdown-notes-api
```

### 2. Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

**Core Dependencies:**
```
fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy==2.0.23
asyncpg==0.29.0
alembic==1.12.1
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6
python-dotenv==1.0.0
pydantic==2.5.0

# Advanced Features
markdown==3.5.1
bleach==6.1.0
httpx==0.25.2
```

### 4. Environment Configuration

Create a `.env` file in the project root:

```bash
# Database
DATABASE_URL=postgresql+asyncpg://postgres:your_password@localhost:5432/markdown_notes

# Security
SECRET_KEY=your-secret-key-here-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Optional: API Keys
OPENAI_API_KEY=your-openai-key-here
```

**Generate a secure SECRET_KEY:**
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

---

## 💾 Database Setup

### 1. Create PostgreSQL Database

**Using psql:**
```bash
psql -U postgres
```

```sql
CREATE DATABASE markdown_notes;
\q
```

**Or using pgAdmin:**
1. Open pgAdmin
2. Right-click on "Databases" → Create → Database
3. Name: `markdown_notes`
4. Click "Save"

### 2. Run Migrations

```bash
# Initialize Alembic (only if not done)
alembic init alembic

# Run all migrations
alembic upgrade head
```

**Expected Output:**
```
INFO  [alembic.runtime.migration] Running upgrade -> abc123, create users table
INFO  [alembic.runtime.migration] Running upgrade abc123 -> def456, create notes table
INFO  [alembic.runtime.migration] Running upgrade def456 -> ghi789, create note_revisions table
INFO  [alembic.runtime.migration] Running upgrade ghi789 -> jkl012, create grammar_issues table
```

### 3. Verify Database

```bash
# Connect to database
psql -U postgres -d markdown_notes

# List tables
\dt

# Expected tables:
# users
# notes
# tags
# note_tags
# note_revisions
# grammar_issues
```

---

## 🏃 Running the Application

### Development Server

```bash
uvicorn main:app --reload
```

**Output:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [12345] using watchfiles
INFO:     Started server process [12346]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### Access Points

- **API**: http://localhost:8000
- **Interactive Docs (Swagger)**: http://localhost:8000/docs
- **Alternative Docs (ReDoc)**: http://localhost:8000/redoc

### Production Server

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

---

## 📖 Features Guide

## 3.1 Notes CRUD & Revision History

### Overview
Complete note management with automatic revision tracking.

### Setup
✅ Already included in base installation

### Features
- Create, Read, Update, Delete notes
- Tag management
- Automatic revision creation on updates
- Restore previous versions
- Soft delete with restore capability

### API Endpoints

#### **Create Note**
```http
POST /notes/
Authorization: Bearer {token}
Content-Type: application/json

{
  "title": "My First Note",
  "content": "# Welcome\n\nThis is **Markdown** content!",
  "tags": ["personal", "welcome"]
}
```

#### **Get All Notes**
```http
GET /notes/
Authorization: Bearer {token}
```

#### **Get Single Note**
```http
GET /notes/{note_id}
Authorization: Bearer {token}
```

#### **Update Note** (Creates Revision)
```http
PUT /notes/{note_id}
Authorization: Bearer {token}
Content-Type: application/json

{
  "title": "Updated Title",
  "content": "# Updated Content"
}
```

**📝 Note**: Every update automatically creates a revision with the OLD content

#### **Get Revision History**
```http
GET /notes/{note_id}/revisions
Authorization: Bearer {token}
```

**Response:**
```json
[
  {
    "id": "revision-uuid",
    "note_id": "note-uuid",
    "title": "Previous Title",
    "content": "Previous content...",
    "created_at": "2024-01-15T10:30:00"
  }
]
```

#### **Restore Previous Version**
```http
POST /notes/{note_id}/revisions/{revision_id}/restore
Authorization: Bearer {token}
```

#### **Delete Note** (Soft Delete)
```http
DELETE /notes/{note_id}
Authorization: Bearer {token}
```

#### **Get Notes by Tag**
```http
GET /tags/{tag_name}/notes
Authorization: Bearer {token}
```

### Testing Example

```bash
# 1. Create a note
curl -X POST "http://localhost:8000/notes/" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Test Note",
    "content": "Original content",
    "tags": ["test"]
  }'

# 2. Update the note (creates revision)
curl -X PUT "http://localhost:8000/notes/{note_id}" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Test Note",
    "content": "Updated content"
  }'

# 3. Get revisions
curl -X GET "http://localhost:8000/notes/{note_id}/revisions" \
  -H "Authorization: Bearer YOUR_TOKEN"

# 4. Restore previous version
curl -X POST "http://localhost:8000/notes/{note_id}/revisions/{revision_id}/restore" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

## 3.2 Grammar & Style Checking

### Overview
Automated grammar checking using LanguageTool API with selective fix application.

### Setup

#### 1. Dependencies
```bash
pip install httpx==0.25.2
```

#### 2. Files Required
- `app/models/grammar_issue.py` - Database model
- `app/schemas/grammar.py` - Pydantic schemas
- `app/services/grammar_service.py` - LanguageTool integration
- `app/api/grammar.py` - API routes

#### 3. Database Migration
```bash
alembic revision -m "create grammar_issues table"
alembic upgrade head
```

#### 4. Register Router
Add to `main.py`:
```python
from app.api import grammar
app.include_router(grammar.router)
```

### Features
- Detect spelling mistakes
- Identify grammar errors
- Find style issues
- Get correction suggestions
- Selective fix application
- Issue history tracking

### API Endpoints

#### **Check Grammar**
```http
POST /notes/{note_id}/revisions/{revision_id}/grammar-check
Authorization: Bearer {token}
```

**Response:**
```json
{
  "revision_id": "uuid",
  "total_issues": 3,
  "issues": [
    {
      "id": "issue-uuid",
      "message": "Possible spelling mistake found.",
      "offset": 15,
      "length": 5,
      "replacements": ["error", "errors"],
      "issue_type": "misspelling",
      "is_applied": false
    }
  ]
}
```

#### **Get Stored Issues**
```http
GET /notes/{note_id}/revisions/{revision_id}/grammar-issues
Authorization: Bearer {token}
```

#### **Apply Fixes**
```http
POST /notes/{note_id}/revisions/{revision_id}/apply-fixes
Authorization: Bearer {token}
Content-Type: application/json

{
  "issue_ids": ["issue-uuid-1", "issue-uuid-2"]
}
```

**Response:**
```json
{
  "applied_count": 2,
  "new_content": "Corrected text here...",
  "message": "Applied 2 grammar fixes."
}
```

### Complete Workflow Example

```bash
# Step 1: Create note with errors
curl -X POST "http://localhost:8000/notes/" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Test",
    "content": "This is an erorr. Their are mistakes here."
  }'

# Step 2: Update note (creates revision)
curl -X PUT "http://localhost:8000/notes/{note_id}" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"content": "This is an erorr. Their are mistakes here."}'

# Step 3: Get revision ID
curl -X GET "http://localhost:8000/notes/{note_id}/revisions" \
  -H "Authorization: Bearer YOUR_TOKEN"

# Step 4: Check grammar
curl -X POST "http://localhost:8000/notes/{note_id}/revisions/{revision_id}/grammar-check" \
  -H "Authorization: Bearer YOUR_TOKEN"

# Response will show detected issues:
# - "erorr" → "error" (spelling)
# - "Their" → "There" (confused words)

# Step 5: Apply selected fixes
curl -X POST "http://localhost:8000/notes/{note_id}/revisions/{revision_id}/apply-fixes" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"issue_ids": ["issue-uuid-1", "issue-uuid-2"]}'

# Response: "This is an error. There are mistakes here."

# Step 6: Update note with corrected content
curl -X PUT "http://localhost:8000/notes/{note_id}" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"content": "This is an error. There are mistakes here."}'
```

### Third-Party Integration: LanguageTool

**API Used:** https://api.languagetool.org/v2/check

**Features:**
- 30+ languages supported
- No API key required (free tier)
- 20 requests/minute limit

**For Production:**
Self-host LanguageTool for unlimited requests:
```bash
docker run -d -p 8010:8010 erikvl87/languagetool
```

Then update `grammar_service.py`:
```python
LANGUAGETOOL_URL = "http://localhost:8010/v2/check"
```

### Testing in Swagger

1. Go to http://localhost:8000/docs
2. Expand `POST /notes/{note_id}/revisions/{revision_id}/grammar-check`
3. Click "Try it out"
4. Enter note_id and revision_id
5. Click "Execute"
6. Review detected issues
7. Copy issue IDs
8. Use "Apply Fixes" endpoint with selected issue IDs

---

## 3.3 Rendered Content Delivery

### Overview
Convert Markdown notes to sanitized HTML with HTTP caching and content negotiation.

### Setup

#### 1. Dependencies
```bash
pip install markdown==3.5.1 bleach==6.1.0
```

#### 2. Files Required
- `app/services/markdown_service.py` - Markdown conversion & sanitization
- `app/api/render.py` - Rendering endpoints

#### 3. Enable CORS
Add to `main.py`:
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

#### 4. Register Router
Add to `main.py`:
```python
from app.api import render
app.include_router(render.router)
```

### Features
- Markdown → HTML conversion
- XSS protection (HTML sanitization)
- ETag caching (HTTP 304)
- Content negotiation (HTML/JSON)
- Raw HTML endpoint
- Syntax highlighting for code
- Table support
- Blockquote styling

### API Endpoints

#### **Render Note (HTML)**
```http
GET /notes/{note_id}/render
Authorization: Bearer {token}
Accept: text/html
```

**Response:**
```html
HTTP/1.1 200 OK
Content-Type: text/html; charset=utf-8
ETag: "5f2a3b4c7d8e9f0a1b2c3d4e5f6a7b8c"
Cache-Control: private, max-age=3600

<!DOCTYPE html>
<html>
  <head>
    <title>My Note</title>
    <style>...</style>
  </head>
  <body>
    <h1>My Note</h1>
    <p><strong>Bold</strong> and <em>italic</em></p>
  </body>
</html>
```

#### **Render Note (JSON)**
```http
GET /notes/{note_id}/render
Authorization: Bearer {token}
Accept: application/json
```

**Response:**
```json
{
  "note_id": "uuid",
  "title": "My Note",
  "html": "<h1>My Note</h1><p><strong>Bold</strong>...</p>",
  "markdown": "# My Note\n\n**Bold** and *italic*"
}
```

#### **Raw HTML (No Wrapper)**
```http
GET /notes/{note_id}/render/raw
Authorization: Bearer {token}
```

**Response:**
```html
<h1>My Note</h1>
<p><strong>Bold</strong> and <em>italic</em></p>
```

### HTTP Caching with ETag

**First Request:**
```http
GET /notes/{note_id}/render
Authorization: Bearer {token}
```

**Response:**
```http
HTTP/1.1 200 OK
ETag: "abc123..."
Cache-Control: private, max-age=3600

<html>...</html>
```

**Second Request (With ETag):**
```http
GET /notes/{note_id}/render
Authorization: Bearer {token}
If-None-Match: "abc123..."
```

**Response:**
```http
HTTP/1.1 304 Not Modified
ETag: "abc123..."

(Empty body - use cached version)
```

### Complete Workflow Example

```bash
# Step 1: Create note with Markdown
curl -X POST "http://localhost:8000/notes/" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "My Note",
    "content": "# Welcome\n\n**Bold** text\n\n- Item 1\n- Item 2"
  }'

# Step 2: Render as HTML
curl -X GET "http://localhost:8000/notes/{note_id}/render" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Accept: text/html"

# Step 3: Render as JSON
curl -X GET "http://localhost:8000/notes/{note_id}/render" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Accept: application/json"

# Step 4: Test ETag caching
curl -i -X GET "http://localhost:8000/notes/{note_id}/render" \
  -H "Authorization: Bearer YOUR_TOKEN"
# Copy ETag from response headers

curl -i -X GET "http://localhost:8000/notes/{note_id}/render" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H 'If-None-Match: "etag-value-here"'
# Should return 304 Not Modified

# Step 5: Get raw HTML
curl -X GET "http://localhost:8000/notes/{note_id}/render/raw" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Supported Markdown Features

- **Headers**: `# H1` through `###### H6`
- **Bold**: `**bold**` or `__bold__`
- **Italic**: `*italic*` or `_italic_`
- **Lists**: Ordered and unordered
- **Links**: `[text](url)`
- **Images**: `![alt](url)`
- **Code**: Inline `` `code` `` and blocks ` ```language ```
- **Tables**: GitHub-flavored tables
- **Blockquotes**: `> quote`
- **Horizontal Rules**: `---` or `***`

### Security: XSS Protection

All HTML output is sanitized using the `bleach` library:

**Input (Malicious):**
```html
<script>alert('XSS')</script>
<img src=x onerror="alert('XSS')">
```

**Output (Safe):**
```html
&lt;script&gt;alert('XSS')&lt;/script&gt;
&lt;img src=x onerror="alert('XSS')"&gt;
```

### Testing in Swagger

1. Go to http://localhost:8000/docs
2. Find `GET /notes/{note_id}/render`
3. Click "Try it out"
4. Enter note_id
5. Select response type:
   - `text/html` for HTML
   - `application/json` for JSON
6. Click "Execute"
7. View rendered output

### Testing with Browser

Use the provided HTML viewer (`note-viewer.html`):

1. Open `note-viewer.html` in browser
2. Enter JWT token
3. Enter note ID
4. Click format buttons:
   - **📄 HTML** - Full HTML page
   - **📋 JSON** - JSON format
   - **📝 Raw HTML** - HTML without wrapper

---

## 📚 API Documentation

### Authentication

#### **Register**
```http
POST /auth/register
Content-Type: application/json

{
  "username": "user123",
  "email": "user@example.com",
  "password": "securepass123"
}
```

#### **Login**
```http
POST /auth/login
Content-Type: application/x-www-form-urlencoded

username=user123&password=securepass123
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer"
}
```

#### **Get Current User**
```http
GET /auth/me
Authorization: Bearer {token}
```

### Complete API Reference

Access interactive documentation at:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## 🧪 Testing

### Manual Testing with Swagger

1. Start the server: `uvicorn main:app --reload`
2. Open http://localhost:8000/docs
3. Click "Authorize" button
4. Register and login to get token
5. Use token for authenticated endpoints

### Testing with cURL

See examples in each feature section above.

### Testing with Postman

1. Import the API into Postman
2. Set base URL: `http://localhost:8000`
3. Add Authorization header: `Bearer {token}`
4. Test endpoints

### Automated Tests (Optional)

Create `tests/test_api.py`:
```python
import pytest
from httpx import AsyncClient
from main import app

@pytest.mark.asyncio
async def test_create_note():
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Test code here
        pass
```

Run tests:
```bash
pytest
```

---

## 📁 Project Structure

```
markdown-notes-api/
├── app/
│   ├── api/
│   │   ├── __init__.py
│   │   ├── auth.py           # Authentication endpoints
│   │   ├── notes.py          # Notes CRUD endpoints
│   │   ├── grammar.py        # Grammar checking endpoints
│   │   └── render.py         # Rendering endpoints
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py         # Configuration
│   │   ├── database.py       # Database connection
│   │   └── security.py       # JWT & password hashing
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py           # User model
│   │   ├── note.py           # Note model
│   │   ├── tag.py            # Tag model
│   │   ├── note_revision.py  # Revision model
│   │   └── grammar_issue.py  # Grammar issue model
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user.py           # User schemas
│   │   ├── note.py           # Note schemas
│   │   ├── grammar.py        # Grammar schemas
│   │   └── render.py         # Render schemas
│   └── services/
│       ├── __init__.py
│       ├── authorization_service.py  # JWT handling
│       ├── grammar_service.py        # LanguageTool integration
│       └── markdown_service.py       # Markdown processing
├── alembic/
│   ├── versions/             # Database migrations
│   └── env.py
├── .env                      # Environment variables
├── .gitignore
├── alembic.ini
├── main.py                   # Application entry point
├── requirements.txt          # Dependencies
└── README.md                 # This file
```

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -am 'Add feature'`
4. Push to branch: `git push origin feature-name`
5. Submit a Pull Request

### Development Guidelines

- Follow PEP 8 style guide
- Add docstrings to functions
- Write tests for new features
- Update documentation

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🆘 Support

### Common Issues

**Issue: Database connection error**
```
Solution: Check DATABASE_URL in .env and verify PostgreSQL is running
```

**Issue: Module not found**
```
Solution: Activate virtual environment and run pip install -r requirements.txt
```

**Issue: LanguageTool rate limit**
```
Solution: Self-host LanguageTool or implement request throttling
```

### Getting Help

- **Documentation**: http://localhost:8000/docs
- **Issues**: https://github.com/RaghadThawabi/MarkDown_Notes_Project2/issues
- **Discussions**: https://github.com/RaghadThawabi/MarkDown_Notes_Project2/discussions

---

## 🙏 Acknowledgments

- **FastAPI**: Modern Python web framework
- **LanguageTool**: Grammar checking API
- **python-markdown**: Markdown processing
- **SQLAlchemy**: SQL toolkit and ORM

---

## 📊 Project Status

- ✅ User Authentication
- ✅ Notes CRUD Operations
- ✅ Revision History (3.1)
- ✅ Grammar Checking (3.2)
- ✅ Rendered Content Delivery (3.3)
- 🚧 AI Summarization (Optional)
- 🚧 Cloud Storage Integration (Optional)

---

**Made with ❤️ using FastAPI and PostgreSQL**
