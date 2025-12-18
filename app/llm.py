from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_llm():
    return ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0.5,  # Balanced creativity and consistency
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )
