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
