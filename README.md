# Task API

Small CRUD API for a to-do list, built with FastAPI. Originally in-memory, then SQLite, now backed by Postgres running in Docker — data survives both app and container restarts.

**Week 4 update:** added Supabase Auth — sign up, log in, log out, and protected
routes guarded by JWT verification, documented with the Swagger "Authorize"
padlock. See the [Auth section](#auth--login--protect-week-4) below.

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

Requires a `.env` file with `DATABASE_URL` and Supabase credentials set (see
`.env.example`), a reachable Postgres instance, and a free Supabase project
(see [Auth setup](#auth--login--protect-week-4) below).

## Endpoints

| Method | Path                | Meaning                          | Auth header |
|--------|----------------------|-----------------------------------|-------------|
| GET    | /                    | API info                          | none |
| GET    | /health              | Health check                      | none |
| GET    | /tasks               | List all tasks                    | none |
| GET    | /tasks/{id}          | Get a single task                 | none |
| POST   | /tasks               | Create a new task                 | none |
| PUT    | /tasks/{id}          | Update a task's title/done        | none |
| DELETE | /tasks/{id}          | Delete a task                     | none |
| POST   | /auth/signup         | Create a new user account         | none |
| POST   | /auth/login          | Authenticate & return a JWT       | none |
| POST   | /auth/logout         | End the user's session            | `Bearer <token>` |
| GET    | /protected/profile   | Read private profile data         | `Bearer <token>` |
| GET    | /protected/dashboard | Second protected route (demo)     | `Bearer <token>` |
| GET    | /public/info         | Read public, open data            | none |

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

## Auth · Login & protect (Week 4)

Adds **Supabase Auth** as the Identity Provider: sign up, log in, log out,
and JWT-guarded protected routes — layered on top of the existing app
without touching the `/tasks` routes.

No password hashing or cryptography is written by hand — Supabase handles
that. This code only ever sends credentials to Supabase and verifies the
tokens it returns.

### Auth setup

1. Create a free project at [supabase.com](https://supabase.com).
2. In **Project Settings → API**, copy your **Project URL** and **anon key**
   (never the `service_role` key).
3. In **Authentication → Providers → Email**, turn **"Confirm email" off**
   for this practice project.
4. Add to your `.env` (see `.env.example`):
   ```
   SUPABASE_URL=your_project_url
   SUPABASE_KEY=your_anon_key
   ```
5. Install the new dependency (already in `requirements.txt`): `supabase`.
6. Run as usual: `uvicorn main:app --reload --port 8000`.

### New files

```
supabase_client.py     # initializes the Supabase client from env vars
security.py            # get_current_user — the reusable guard (FastAPI dependency)
routers/
  auth.py               # /auth/signup, /auth/login, /auth/logout
  public.py             # /public/info
  protected.py          # /protected/profile, /protected/dashboard
```

### Testing the auth flow

```bash
# Sign up
curl -i -X POST http://localhost:8000/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123"}'

# Log in
curl -i -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123"}'

# Call a protected route (paste your access_token)
curl -i http://localhost:8000/protected/profile \
  -H "Authorization: Bearer <PASTE_ACCESS_TOKEN>"

# Tamper with the token -> 401
curl -i http://localhost:8000/protected/profile \
  -H "Authorization: Bearer <PASTE_ACCESS_TOKEN>x"

# No token at all -> 401
curl -i http://localhost:8000/protected/profile
```

### Swagger UI

FastAPI serves Swagger at `/docs` automatically. The `HTTPBearer` scheme in
`security.py` makes the **Authorize** padlock appear on every protected
route — paste a token once, then use "Try it out" directly in the browser.

_Add your Swagger screenshot here (Authorize + successful `/protected/profile` call)._

### AI vs me (Stage 7 — fill in after the rematch)

_Write your own prompt from memory, generate a second version in
`ai-version/`, run the same checkpoints against it, and answer:_

1. **Token extraction** — did the AI correctly parse the `Bearer ` prefix?
2. **Security flaws** — did it safely reject invalid tokens, or trust
   `get_user` without checking for exceptions/errors?
3. **What your prompt forgot to specify** — what did the AI silently decide
   for you?