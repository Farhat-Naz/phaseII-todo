from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# Add CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage (temporary - no authentication)
todos_db = []
todo_id_counter = 1

class TodoCreate(BaseModel):
    title: str
    description: Optional[str] = ""

class TodoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

class Todo(BaseModel):
    id: int
    title: str
    description: str
    completed: bool

@app.get("/")
def read_root():
    return {"Hello": "World", "status": "working", "message": "Todo API - No Authentication"}

@app.get("/api/test")
def test():
    return {"message": "API working", "todos_count": len(todos_db)}

@app.get("/api/todos", response_model=List[Todo])
def get_todos():
    """Get all todos (no authentication)"""
    return todos_db

@app.post("/api/todos", response_model=Todo)
def create_todo(todo: TodoCreate):
    """Create a new todo (no authentication)"""
    global todo_id_counter
    new_todo = Todo(
        id=todo_id_counter,
        title=todo.title,
        description=todo.description or "",
        completed=False
    )
    todos_db.append(new_todo)
    todo_id_counter += 1
    return new_todo

@app.patch("/api/todos/{todo_id}", response_model=Todo)
def update_todo(todo_id: int, update: TodoUpdate):
    """Update a todo (no authentication)"""
    for todo in todos_db:
        if todo.id == todo_id:
            if update.title is not None:
                todo.title = update.title
            if update.description is not None:
                todo.description = update.description
            if update.completed is not None:
                todo.completed = update.completed
            return todo
    raise HTTPException(status_code=404, detail="Todo not found")

@app.delete("/api/todos/{todo_id}")
def delete_todo(todo_id: int):
    """Delete a todo (no authentication)"""
    global todos_db
    todos_db = [t for t in todos_db if t.id != todo_id]
    return {"message": "Todo deleted", "id": todo_id}
