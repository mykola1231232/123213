from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import sessionmaker, declarative_base
import logging

DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

app = FastAPI()
logging.basicConfig(level=logging.INFO)

# SQLAlchemy модель
class Animal(Base):
    __tablename__ = "animals"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    age = Column(Integer)
    adopted = Column(Boolean)
    health_status = Column(String, default="healthy")

Base.metadata.create_all(bind=engine)

# Pydantic модель
class AnimalResponse(BaseModel):
    id: int
    name: str
    age: int
    adopted: bool
    health_status: Optional[str] = "healthy"

    class Config:
        orm_mode = True

@app.get("/animals/{animal_id}", response_model=AnimalResponse)
def get_animal(animal_id: int):
    db = SessionLocal()
    animal = db.query(Animal).filter(Animal.id == animal_id).first()
    if not animal:
        logging.error(f"Animal with ID {animal_id} not found")
        raise HTTPException(status_code=404, detail="Animal not found")
    if animal.age < 0:
        logging.error(f"Animal with negative age: {animal.age}")
        raise HTTPException(status_code=400, detail="Age cannot be negative")
    return animal

# Tasks

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)

class TaskResponse(BaseModel):
    id: int
    title: str

    class Config:
        orm_mode = True

@app.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: int):
    if task_id > 1000:
        logging.error(f"Task ID too large: {task_id}")
        raise HTTPException(status_code=422, detail="Task ID exceeds maximum allowed value")
    db = SessionLocal()
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        logging.error(f"Task with ID {task_id} not found")
        raise HTTPException(status_code=404, detail="Task not found")
    return task