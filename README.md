# Task API

Small CRUD API for a to-do list, built with FastAPI. Originally in-memory, then SQLite, now backed by Postgres running in Docker — data survives both app and container restarts.

## Run it (full stack, recommended)

```bash
docker compose up
```

This starts Postgres and the FastAPI app together, creates the `tasks` table via `init.sql`, and seeds 3 example tasks on first run. API available at `http://localhost:8000`.

## Run it (app only, local Postgres)

```bash
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

Requires a `.env` file with `DATABASE_URL` set (see `.env.example`) and a reachable Postgres instance.

## Endpoints

| Method | Path          | Meaning                        |
|--------|---------------|---------------------------------|
| GET    | /             | API info                       |
| GET    | /health       | Health check                   |
| GET    | /tasks        | List all tasks                 |
| GET    | /tasks/{id}   | Get a single task               |
| POST   | /tasks        | Create a new task               |
| PUT    | /tasks/{id}   | Update a task's title/done      |
| DELETE | /tasks/{id}   | Delete a task                   |

## Example request

```bash
'{"title":"Buy milk"}' | Out-File -Encoding utf8 body.json
curl.exe -i -X POST http://localhost:8000/tasks -H "Content-Type: application/json" --data "@body.json"
```

```
HTTP/1.1 201 Created
content-type: application/json

{"id":4,"title":"Buy milk","done":false}
```

## Swagger UI — full CRUD cycle

![Create task](swagger-create.png)
![List tasks](swagger-list.png)
![Get single task](swagger-get-one.png)
![Update task](swagger-update.png)
![Delete task](swagger-delete.png)

## Database — Postgres via Docker

Tasks are stored in Postgres, running in Docker with a persistent volume (`pgdata`), defined in `docker-compose.yml`.

**Architecture:** the Postgres repository (`database.py`) replaced the earlier in-memory and SQLite versions. The routes in `main.py` did not change — same function signatures, same status codes — proving the storage layer is genuinely swappable without touching the service layer.

**Environment:** the connection string lives in `.env` (git-ignored). `.env.example` is committed showing the expected shape:
```
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/todo
```
Note: inside `docker-compose.yml`, the app connects to the Postgres service using the hostname `db` (Docker's internal networking), not `localhost`.

**Schema:** created via `init.sql`, run automatically by Postgres on first container start. Seeds 3 example tasks only if the table is empty.

**Persistence proven:** created a task via `POST /tasks`, then ran:
```bash
docker compose down
docker compose up
```
`GET /tasks` afterward still showed the created task — confirming the volume preserves data across a full stack restart, not just an app restart.

## Database Browser screenshot (SQLite era, kept for history)

![DB Browser](db-browser.png)
