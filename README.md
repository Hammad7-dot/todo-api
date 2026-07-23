# Task API

Small CRUD API for a to-do list, built with FastAPI. Tasks are stored in memory — data resets when the server restarts.

## Run it
pip install -r requirements.txt

uvicorn main:app --reload --port 8000

## Swagger UI — full CRUD cycle

![Create task](swagger-create.png)
![List tasks](swagger-list.png)
![Get single task](swagger-get-one.png)
![Update task](swagger-update.png)
![Delete task](swagger-delete.png)

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
curl.exe -i -X POST http://localhost:8000/tasks -H "Content-Type: application/json" -d '{"title":"Buy milk"}'
```
```
HTTP/1.1 422 Unprocessable Content
date: Thu, 23 Jul 2026 20:25:01 GMT
server: uvicorn
content-length: 158
content-type: application/json
{"detail":[{"type":"json_invalid","loc":["body",1],"msg":"JSON decode error","input":{},"ctx":{"error":"Expecting property name enclosed in double quotes"}}]}
```
