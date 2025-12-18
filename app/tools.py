from langchain.tools import tool
from app.rag import get_rag_context

@tool
def fetch_email_template(query: str) -> str:
    """
    Fetch a relevant email template based on the user's email request.
    Use this tool when drafting an email that may benefit from a predefined template.
    """
    return get_rag_context(query)
