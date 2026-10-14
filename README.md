# Task Tracker

A beginner-friendly full-stack task tracker built to practise **FastAPI**, **PostgreSQL**, **SQLAlchemy**, and **React**.

Users can register, log in, and manage their own tasks. Each task supports a title, description, status, priority, and optional due date.

## Features

- JWT authentication with securely hashed passwords
- User-owned tasks: users cannot view or change another user's tasks
- Create, read, update, and delete tasks
- Task status: `todo`, `in_progress`, and `done`
- Task priority: `low`, `medium`, and `high`
- Search, filtering, sorting, and pagination on the API
- Task dashboard with todo, in-progress, done, and overdue counts
- Responsive React interface
- Alembic migrations for PostgreSQL
- MVC-style backend organization
- Automated backend tests

## Tech stack

| Area | Technology |
| --- | --- |
| Backend | FastAPI, SQLAlchemy 2.0, Pydantic v2 |
| Database | PostgreSQL, Alembic |
| Authentication | JWT, pwdlib |
| Frontend | React, Vite, TypeScript |

## Project structure

```text
Tracker/
├── backend/
│   ├── alembic/                 # Database migration scripts
│   ├── app/
│   │   ├── controllers/         # API endpoint handlers
│   │   ├── models/              # SQLAlchemy database entities
│   │   ├── views/               # Pydantic request and response models
│   │   ├── services/            # Password and JWT helpers
│   │   ├── dependencies/        # Authentication dependencies
│   │   ├── config.py
│   │   ├── database.py
│   │   └── main.py
│   ├── tests/
│   ├── requirements.txt
│   └── alembic.ini
├── frontend/
│   ├── src/
│   └── package.json
└── README.md
```

## Prerequisites

- Python 3.12+
- Node.js 20+
- PostgreSQL

## Backend setup

Create a PostgreSQL database, for example named `tracker`.

Create `backend/.env` with your own values:

```env
APP_NAME=Task Tracker
DATABASE_URL=postgresql+psycopg://POSTGRES_USER:POSTGRES_PASSWORD@localhost:5432/tracker
SECRET_KEY=replace-with-a-long-random-secret
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
FRONTEND_ORIGIN=http://localhost:5173
```

From the project root, create and activate a virtual environment if you do not already have one:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install backend dependencies and run the migration:

```powershell
cd backend
pip install -r requirements.txt
alembic upgrade head
```

Start the API:

```powershell
uvicorn app.main:app --reload
```

The API runs at `http://127.0.0.1:8000`. Interactive API documentation is available at `http://127.0.0.1:8000/docs`.

## Frontend setup

Open a second terminal from the project root:

```powershell
cd frontend
Copy-Item .env.example .env
npm install
npm run dev
```

Open the URL printed by Vite, usually `http://localhost:5173`.

The frontend reads the API address from `frontend/.env`:

```env
VITE_API_BASE_URL=http://127.0.0.1:8000
```

## Running tests

The backend tests use a temporary SQLite database, so they do not modify your PostgreSQL database.

```powershell
cd backend
pytest -q
```

Build the frontend for production:

```powershell
cd frontend
npm run build
```

## API endpoints

| Method | Endpoint | Description |
| --- | --- | --- |
| `POST` | `/api/auth/register` | Create an account |
| `POST` | `/api/auth/login` | Log in and receive a JWT |
| `GET` | `/api/users/me` | Get the authenticated user |
| `POST` | `/api/tasks` | Create a task |
| `GET` | `/api/tasks` | List the authenticated user's tasks |
| `GET` | `/api/tasks/summary` | Get task summary counts |
| `GET` | `/api/tasks/{task_id}` | Get one owned task |
| `PATCH` | `/api/tasks/{task_id}` | Update one owned task |
| `DELETE` | `/api/tasks/{task_id}` | Delete one owned task |

Protected endpoints require this header:

```http
Authorization: Bearer YOUR_ACCESS_TOKEN
```

Example task payload:

```json
{
  "title": "Learn FastAPI",
  "description": "Build a task tracker API",
  "status": "todo",
  "priority": "high",
  "due_date": "2026-10-20T18:00:00+06:00"
}
```

## Learning notes

The backend follows a lightweight MVC structure:

- **Models** define the PostgreSQL tables and relationships.
- **Views** validate incoming requests and shape outgoing responses.
- **Controllers** implement HTTP endpoints and connect views, models, and services.

This is intentionally a small project. Possible future improvements include frontend pagination, additional test coverage, password reset, task labels, and deployment.
