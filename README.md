# Task API

Small CRUD API for a to-do list, built with FastAPI. Tasks are now stored in SQLite — data survives a server restart.

## Run it
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

## Endpoints

| Method | Path          | Meaning                       |
|--------|---------------|--------------------------------|
| GET    | /             | API info                      |
| GET    | /health       | Health check                  |
| GET    | /tasks        | List all tasks                |
| GET    | /tasks/{id}   | Get a single task              |
| POST   | /tasks        | Create a new task              |
| PUT    | /tasks/{id}   | Update a task's title/done     |
| DELETE | /tasks/{id}   | Delete a task                  |

## Example request

```bash
'{"title":"Buy milk"}' | Out-File -Encoding utf8 body.json
curl.exe -i -X POST http://localhost:8000/tasks -H "Content-Type: application/json" --data "@body.json"
```

HTTP/1.1 201 Created
date: Thu, 23 Jul 2026 20:27:51 GMT
server: uvicorn
content-length: 40
content-type: application/json

{"id":4,"title":"Buy milk","done":false}

## Database

Tasks are stored in SQLite (`tasks.db`) instead of in memory.

**Why SQLite:** single file, zero setup, no separate server to install — and unlike the in-memory version from A1, data now survives a server restart.

**Database file:** `tasks.db`, created automatically on first run. It's git-ignored so each clone starts fresh with 3 seeded example tasks.

**Example SQL query (run in DB Browser):**
```sql
DELETE FROM tasks WHERE done = 1;
```
Deleted the completed task; confirmed instantly via `GET /tasks` with no server restart needed, proving the API and DB Browser read the same file.

## Database Browser screenshot

![DB Browser](db-browser.png)