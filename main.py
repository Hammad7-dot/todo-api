from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from database import get_db, get_all_tasks, get_task, create_task, update_task, delete_task
from routers import auth, public, protected

app = FastAPI()

app.include_router(auth.router)
app.include_router(public.router)
app.include_router(protected.router)

class TaskCreate(BaseModel):
    title: str

class TaskUpdate(BaseModel):
    title: str
    done: bool

@app.get("/tasks")
def list_tasks():
    db = get_db()
    tasks = get_all_tasks(db)
    db.close()
    return tasks

@app.get("/tasks/{task_id}")
def read_task(task_id: int):
    db = get_db()
    task = get_task(db, task_id)
    db.close()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.get("/")
def read_root():
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks"]
    }

@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/tasks", status_code=201)
def add_task(task: TaskCreate):
    if not task.title or not task.title.strip():
        raise HTTPException(status_code=400, detail="Title is required")
    db = get_db()
    new_task = create_task(db, task.title)
    db.close()
    return new_task

@app.put("/tasks/{task_id}")
def edit_task(task_id: int, task: TaskUpdate):
    if not task.title or not task.title.strip():
        raise HTTPException(status_code=400, detail="Title is required")
    db = get_db()
    updated = update_task(db, task_id, task.title, task.done)
    db.close()
    if updated is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated

@app.delete("/tasks/{task_id}", status_code=204)
def remove_task(task_id: int):
    db = get_db()
    success = delete_task(db, task_id)
    db.close()
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")