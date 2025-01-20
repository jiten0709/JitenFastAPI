# Content Recommendation Agent

This is a FastAPI-based service that provides personalized content recommendations using LangChain and Supabase. It leverages OpenAI’s GPT models to generate recommendations based on user preferences stored in a Supabase database.

---

## **Features**

- Fetch user preferences from a Supabase database.
- Use LangChain’s `PromptTemplate` and OpenAI’s `ChatOpenAI` model for content generation.
- Generate concise, actionable recommendations in bullet-point format.
- FastAPI for building and exposing RESTful endpoints.

---

## **Technologies Used**

- Python
- FastAPI
- Supabase
- LangChain
- OpenAI API
- dotenv for environment variable management
- Postman for API testing

---

## **Installation**

1. Clone the repository:

2. Create and activate a virtual environment:

   ```bash
   source .venv/bin/activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root and refer the .env.sample file:

---

## **Usage**

1. Start the FastAPI server:

   ```bash
   python main.py
   ```

2. Access the API:
   - Home endpoint:
     ```
     GET http://127.0.0.1:8000/
     ```
   - Recommendations endpoint with query parameter:
     ```
     GET http://127.0.0.1:8000/recommendations?user_id=1
     ```

---

## **API Endpoints**

### **1. Home Endpoint**

- **URL**: `/`
- **Method**: `GET`
- **Description**: Returns a welcome message.
- **Response**:
  ```json
  {
    "message": "Welcome to Content Recommendation Agent"
  }
  ```

### **2. Recommendations Endpoint**

- **URL**: `/recommendations`
- **Method**: `GET`
- **Query Parameter**: `user_id` (string)
- **Description**: Fetches user preferences from Supabase and generates personalized recommendations.
- **Example Request**:
  ```
  GET /recommendations?user_id=12345
  ```
- **Example Response**:
  ```json
  {
    "recommended_content": "- Latest AI research articles\n- Top machine learning tutorials\n- Upcoming technology webinars"
  }
  ```

---
