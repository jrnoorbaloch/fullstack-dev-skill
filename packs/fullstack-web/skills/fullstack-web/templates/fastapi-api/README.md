# FastAPI REST API Starter

JWT auth (register / login / me), per-user CRUD for items with pagination and search, SQLModel (SQLite or Postgres), CORS, OpenAPI docs and tests.

## Setup
```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env        # set SECRET_KEY
uvicorn app.main:app --reload
```
Docs: http://localhost:8000/docs

## Test
`pytest -q`

## Postgres
Set `DATABASE_URL=postgresql+psycopg://user:pass@host:5432/db` and `pip install "psycopg[binary]"`.
