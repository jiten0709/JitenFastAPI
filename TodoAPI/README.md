# To-Do List API

A simple RESTful API for managing to-do lists using **FastAPI** and **Supabase** with **JWT-based authentication**.

---

## Features

- User registration and login with JWT authentication
- CRUD operations for to-do items
- Uses Supabase as the backend database

---

## Setup Instructions

### 1. Clone the Repository

```bash
# Clone the repository
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

### 3. Activate the Virtual Environment

- **macOS/Linux**:
  ```bash
  source venv/bin/activate
  ```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Set Up Environment Variables

Create a `.env` file in the project root and add refer the given .env.sample file.

---

## Project Structure

```
my-todo-api/
|-- venv/
|-- supabase_client.py
|-- main.py
|-- .env
```

- `main.py`: Contains the FastAPI routes and logic.
- `supabase_client.py`: Handles the Supabase client initialization.
- `.env`: Stores environment variables.

---

## Running the Project

Run the FastAPI application with Uvicorn:

```bash
uvicorn main:app --reload
```

- The API will be available at: `http://127.0.0.1:8000`

---

## API Endpoints

### 1. **User Registration and Login**

**POST** `/register`

Request Body:

```json
{
  "username": "user@example.com",
  "password": "password123"
}
```

**POST** `/login`

Request Body:

```json
{
  "username": "user@example.com",
  "password": "password123"
}
```

### 2. **Generate a Token**

**POST** `/token`

Form Data:

- `username`: `user@example.com`
- `password`: `password123`

### 3. **Create a Todo Item**

**POST** `/todos/`

Authorization: Bearer Token

Request Body:

```json
{
  "title": "Buy groceries",
  "description": "Milk, Bread, Eggs",
  "completed": false
}
```

### 4. **Get Todo Items**

**GET** `/todos/`

Authorization: Bearer Token

### 5. **Update a Todo Item**

**PUT** `/todos/{todo_id}`

Authorization: Bearer Token

### 6. **Delete a Todo Item**

**DELETE** `/todos/{todo_id}`

Authorization: Bearer Token

---

## Deactivating the Virtual Environment

```bash
deactivate
```
