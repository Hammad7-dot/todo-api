import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)


def get_db():
    return SessionLocal()


def get_all_tasks(db):
    result = db.execute(text("SELECT id, title, done FROM tasks ORDER BY id")).fetchall()
    return [dict(row._mapping) for row in result]


def get_task(db, task_id):
    result = db.execute(text("SELECT id, title, done FROM tasks WHERE id = :id"), {"id": task_id}).fetchone()
    return dict(result._mapping) if result else None


def create_task(db, title):
    result = db.execute(
        text("INSERT INTO tasks (title, done) VALUES (:title, false) RETURNING id, title, done"),
        {"title": title}
    )
    db.commit()
    return dict(result.fetchone()._mapping)


def update_task(db, task_id, title, done):
    result = db.execute(
        text("UPDATE tasks SET title = :title, done = :done WHERE id = :id RETURNING id, title, done"),
        {"title": title, "done": done, "id": task_id}
    )
    db.commit()
    row = result.fetchone()
    return dict(row._mapping) if row else None


def delete_task(db, task_id):
    result = db.execute(text("DELETE FROM tasks WHERE id = :id RETURNING id"), {"id": task_id})
    db.commit()
    return result.fetchone() is not None