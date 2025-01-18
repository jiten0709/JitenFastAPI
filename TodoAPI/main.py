from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import List
import jwt
from datetime import datetime, timedelta
from supabase_client import supabase
import os
from dotenv import load_dotenv
from passlib.context import CryptContext

load_dotenv()

app = FastAPI()

JWT_SECRET = os.getenv("JWT_SECRET")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Database table name
TODO_TABLE = os.getenv("TODO_TABLE_NAME")
USERS_TABLE = os.getenv("USER_TABLE_NAME")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# User Model for creating users
class User(BaseModel):
    username: str
    password: str

# Task Model
class TodoItem(BaseModel):
    title: str
    description: str = ""
    completed: bool = False

# Function to hash passwords
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Function to verify hashed passwords
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# Function to create JWT token
def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=30)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm="HS256")
    return encoded_jwt

# Home page
@app.get("/")
def home():
    return {"message": "Welcome to Todo API"}

# check db connection
@app.get("/test-db-connection")
def test_db_connection():
    try:
        response = supabase.table(TODO_TABLE).select("*").limit(1).execute()
        print(response)
        if response.data:
            return {"status": "success", "data": response.data}
        else:
            raise HTTPException(status_code=500, detail="Connection failed: No data found")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Connection failed: {str(e)}")
    
# Register a new user
@app.post("/register")
def register_user(user: User):
    hashed_password = hash_password(user.password)
    try:
        response = supabase.table(USERS_TABLE).insert({
            "username": user.username,
            "password": hashed_password
        }).execute()

        if response.data is None:  # Check if response is empty
            raise HTTPException(status_code=400, detail="Failed to register user")
        
        # Generate JWT token
        access_token = create_access_token(data={"sub": user.username})
        return {"message": "User registered successfully", "access_token": access_token}
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

# Login and generate a JWT token
@app.post("/login")
def login_user(form_data: OAuth2PasswordRequestForm = Depends()):
    response = supabase.table(USERS_TABLE).select("password").eq("username", form_data.username).execute()
    if response.data is None or not response.data:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    stored_password = response.data[0]["password"]
    if not verify_password(form_data.password, stored_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": form_data.username})
    return {"access_token": access_token, "token_type": "bearer"}

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
    if response.data is None:  # Check if the insert failed
        raise HTTPException(status_code=400, detail="Failed to create todo")
    return todo

# Get all todo items
@app.get("/todos/", response_model=List[TodoItem])
def get_todos(current_user: str = Depends(get_current_user)):
    response = supabase.table(TODO_TABLE).select("*").eq("user", current_user).execute()
    if response.data is None:  # Check if the query failed
        raise HTTPException(status_code=400, detail="Failed to fetch todos")
    return response.data

# Update a todo item
@app.put("/todos/{todo_id}", response_model=TodoItem)
def update_todo(todo_id: int, todo: TodoItem, current_user: str = Depends(get_current_user)):
    response = supabase.table(TODO_TABLE).update({
        "title": todo.title,
        "description": todo.description,
        "completed": todo.completed
    }).eq("id", todo_id).eq("user", current_user).execute()
    if response.data is None:  # Check if the update failed
        raise HTTPException(status_code=400, detail="Failed to update todo")
    return todo

# Delete a todo item
@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int, current_user: str = Depends(get_current_user)):
    response = supabase.table(TODO_TABLE).delete().eq("id", todo_id).eq("user", current_user).execute()
    if response.data is None:  # Check if the delete failed
        raise HTTPException(status_code=400, detail="Failed to delete todo")
    return {"message": "Todo deleted successfully"}
