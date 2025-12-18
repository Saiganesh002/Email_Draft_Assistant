from app.tools import fetch_email_template

def get_rag_context(user_query: str) -> str:
    """
    Get contextual template data for the query.
    """
    return fetch_email_template.run(user_query)
