import os
from dotenv import load_dotenv
from fastapi import FastAPI
from supabase import create_client, Client
from langchain_community.document_loaders import TextLoader
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI()

# Initialize Supabase client
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
USER_PREF_TABLE = os.getenv("USER_PREF_TABLE")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


# LangChain setup
openai_api_key = os.getenv('OPENAI_API_KEY')
llm = ChatOpenAI(openai_api_key=openai_api_key)
prompt_template = PromptTemplate(input_variables=["user_preferences"], template="Based on the preferences {user_preferences}, suggest personalized content.")
chain = prompt_template | llm

# home page
@app.get("/")
def home():
    return {"message": "Welcome to Content Recommendation Agent"}

# recommendations endpoint
@app.get("/recommendations")
async def get_recommendations(user_id: str):
    # Fetch user preferences from Supabase
    response = supabase.table(USER_PREF_TABLE).select("preferences").eq("user_id", user_id).execute()
    if response.data:
        user_preferences = response.data[0]["preferences"]
    else:
        return {"error": "User preferences not found"}

    # Generate recommendations (hypothetical example)
    recommended_content = chain.run(user_preferences=user_preferences)

    return {
        "recommended_content": recommended_content
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

