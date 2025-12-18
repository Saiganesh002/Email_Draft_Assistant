from langchain.tools import tool
import os

TEMPLATE_FOLDER = "templates"


@tool
def fetch_email_template(query: str) -> str:
    """
    Fetch a relevant email template based on the user's email request.
    Use this tool when drafting an email that may benefit from a predefined template.
    """
    templates = {}

    for file in os.listdir(TEMPLATE_FOLDER):
        if file.endswith(".txt"):
            with open(os.path.join(TEMPLATE_FOLDER, file), "r", encoding="utf-8") as f:
                templates[file] = f.read()

    query_lower = query.lower()
    
    # Priority matching for specific phrases
    if "follow up" in query_lower or "follow-up" in query_lower:
        return templates.get("follow_up.txt", "No relevant template found.")
    elif "meeting" in query_lower or "schedule" in query_lower:
        return templates.get("meeting_request.txt", "No relevant template found.")
    elif "thank" in query_lower:
        return templates.get("thank_you.txt", "No relevant template found.")
    elif "apolog" in query_lower or "sorry" in query_lower:
        return templates.get("apology.txt", "No relevant template found.")
    
    # Fallback to original matching
    query_words = query_lower.split()
    for name, content in templates.items():
        content_lower = content.lower()
        if any(word in content_lower for word in query_words):
            return content

    return "No relevant email template was found."
