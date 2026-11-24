# NC plus one

NC Plus One manages events, venues, users, and RSVPs. The repository is organized into a FastAPI backend and a React frontend.

## Backend setup

From the repository root:

```sh
cd backend
python -m pip install -r requirements.txt
```

Copy `backend/.env.example` to `backend/.env.dev` and set your PostgreSQL connection variables. Create the database tables with:

```sh
cd backend
psql -f app/db/setup.sql
```

Run the API from `backend/`:

```sh
uvicorn main:app --reload --port 8000
```

For local development, the API allows browser requests from any origin. Restrict `allow_origins` in `backend/main.py` to trusted frontend origins before deploying.

## Frontend

```sh
cd frontend
npm install
npm run dev
```

## Tests

Run the backend tests from `backend/` after configuring `.env.test` and the test database:

```sh
pytest
```

