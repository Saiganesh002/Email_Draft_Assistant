import os

TEMPLATE_FOLDER = "templates"

def get_rag_context(user_query: str) -> str:
    """
    RAG implementation: Retrieve relevant email template based on user query.
    This function implements the Retrieval part of RAG.
    """
    templates = {}

    # Load all templates from the knowledge base
    for file in os.listdir(TEMPLATE_FOLDER):
        if file.endswith(".txt"):
            with open(os.path.join(TEMPLATE_FOLDER, file), "r", encoding="utf-8") as f:
                templates[file] = f.read()

    query_lower = user_query.lower()
    
    # Priority matching for specific phrases (semantic matching)
    if "follow up" in query_lower or "follow-up" in query_lower:
        return templates.get("follow_up.txt", "No relevant template found.")
    elif "meeting" in query_lower or "schedule" in query_lower:
        return templates.get("meeting_request.txt", "No relevant template found.")
    elif "thank" in query_lower:
        return templates.get("thank_you.txt", "No relevant template found.")
    elif "apolog" in query_lower or "sorry" in query_lower:
        return templates.get("apology.txt", "No relevant template found.")
    
    # Fallback to keyword matching
    query_words = query_lower.split()
    for name, content in templates.items():
        content_lower = content.lower()
        if any(word in content_lower for word in query_words):
            return content

    return "No relevant email template was found."