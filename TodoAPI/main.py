from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import List
import jwt
from datetime import datetime, timedelta
from supabase_client import supabase
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

JWT_SECRET = os.getenv("JWT_SECRET")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Database table name
TODO_TABLE = os.getenv("TODO_TABLE_NAME")

# User Model for creating users (depends on your Supabase auth setup)
class User(BaseModel):
    username: str
    password: str

# Task Model
class TodoItem(BaseModel):
    title: str
    description: str = ""
    completed: bool = False

# Register a new user
@app.post("/register")
def register_user(user: User):
    response = supabase.auth.sign_up(email=user.username, password=user.password)
    if response.error:
        raise HTTPException(status_code=400, detail=response.error.message)
    return {"message": "User registered successfully"}

# Generate a JWT token
@app.post("/token")
def generate_token(form_data: OAuth2PasswordRequestForm = Depends()):
    response = supabase.auth.sign_in(email=form_data.username, password=form_data.password)
    if response.error:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    token_data = {
        "sub": form_data.username,
        "exp": datetime.utcnow() + timedelta(minutes=30)
    }
    token = jwt.encode(token_data, JWT_SECRET, algorithm="HS256")
    return {"access_token": token, "token_type": "bearer"}

# Get current user from token
def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return username
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

# Create a new todo item
@app.post("/todos/", response_model=TodoItem)
def create_todo(todo: TodoItem, current_user: str = Depends(get_current_user)):
    data = {
        "title": todo.title,
        "description": todo.description,
        "completed": todo.completed,
        "user": current_user
    }
    response = supabase.table(TODO_TABLE).insert(data).execute()
    if response.error:
        raise HTTPException(status_code=400, detail=response.error.message)
    return todo

# Get all todo items
@app.get("/todos/", response_model=List[TodoItem])
def get_todos(current_user: str = Depends(get_current_user)):
    response = supabase.table(TODO_TABLE).select("*").eq("user", current_user).execute()
    if response.error:
        raise HTTPException(status_code=400, detail=response.error.message)
    return response.data

# Update a todo item
@app.put("/todos/{todo_id}", response_model=TodoItem)
def update_todo(todo_id: int, todo: TodoItem, current_user: str = Depends(get_current_user)):
    response = supabase.table(TODO_TABLE).update({
        "title": todo.title,
        "description": todo.description,
        "completed": todo.completed
    }).eq("id", todo_id).eq("user", current_user).execute()
    if response.error:
        raise HTTPException(status_code=400, detail=response.error.message)
    return todo

# Delete a todo item
@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int, current_user: str = Depends(get_current_user)):
    response = supabase.table(TODO_TABLE).delete().eq("id", todo_id).eq("user", current_user).execute()
    if response.error:
        raise HTTPException(status_code=400, detail=response.error.message)
    return {"message": "Todo deleted successfully"}

