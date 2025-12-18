import os
from dotenv import load_dotenv

from langchain.agents import initialize_agent, AgentType
from langchain_openai import ChatOpenAI
from app.tools import fetch_email_template

# Load environment variables
load_dotenv()


def get_email_agent():
    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0.5,  # slightly lower = less overthinking
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )

    tools = [fetch_email_template]

    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=False,
        handle_parsing_errors=True,
        max_iterations=5,          
        early_stopping_method="generate"  
    )

    return agent
