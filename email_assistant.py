import os
import requests
from dotenv import load_dotenv

# =========================
# Load environment variables
# =========================
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not found. Please set it in the .env file.")

MODEL_NAME = "gpt-3.5-turbo"
TEMPLATE_FOLDER = "templates"

# =========================
# Few-shot examples (Week 2)
# =========================
FEW_SHOT_EXAMPLES = {
    "formal": (
        "Dear Mr. Smith,\n"
        "I hope this email finds you well. I am writing to follow up on our last discussion.\n"
    ),
    "casual": (
        "Hey John!\n"
        "Just checking in to see if you had a chance to look at my previous message.\n"
    ),
    "professional": (
        "Hello Team,\n"
        "I wanted to follow up regarding the project update we discussed earlier.\n"
    )
}

# =========================
# Load email templates
# =========================
def load_templates():
    templates = {}
    for filename in os.listdir(TEMPLATE_FOLDER):
        if filename.endswith(".txt"):
            path = os.path.join(TEMPLATE_FOLDER, filename)
            with open(path, "r", encoding="utf-8") as f:
                templates[filename.replace(".txt", "")] = f.read().strip()
    return templates


TEMPLATES = load_templates()

# =========================
# Simple RAG-style retrieval
# =========================
def retrieve_relevant_templates(query, top_k=1):
    """
    Retrieve most relevant templates based on keyword overlap.
    """
    query_words = set(query.lower().split())
    scored_templates = []

    for name, content in TEMPLATES.items():
        content_words = set(content.lower().split())
        score = len(query_words.intersection(content_words))
        scored_templates.append((score, name, content))

    scored_templates.sort(reverse=True)
    return scored_templates[:top_k]

# =========================
# Prompt construction
# =========================
def build_prompt(user_request, tone, retrieved_templates):
    tone_example = FEW_SHOT_EXAMPLES.get(tone, "")
    template_context = "\n\n".join(
        f"Template ({name}):\n{content}"
        for _, name, content in retrieved_templates
    )

    prompt = f"""
You are an AI email drafting assistant.

Tone: {tone}

Example of tone:
{tone_example}

Relevant email template(s):
{template_context}

User request and context:
{user_request}

Instructions:
- Write a complete, polished email
- Keep the tone consistent
- Rephrase informal or short user requests into professional language
- Replace placeholders like [Recipient Name] and [Your Name]
  using the provided Recipient Name and Sender Name
- Include a clear and appropriate subject line
- Format the closing signature on separate lines, for example:
  Best regards,
  Sender Name
"""
    return prompt.strip()

# =========================
# OpenAI API call
# =========================
def generate_email(prompt):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": MODEL_NAME,
        "messages": [
            {
                "role": "system",
                "content": "You help users draft clear and professional emails."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.7
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        content = response.json()["choices"][0]["message"]["content"]

        # Enforce deterministic signature formatting
        content = content.replace(
            "Best regards, ",
            "Best regards,\n"
        ).replace(
            "Best regards , ",
            "Best regards,\n"
        )

        return content

    elif response.status_code == 429:
        return (
            "⚠️ OpenAI API quota exceeded.\n\n"
            "The application is correctly configured, but the API key "
            "has no available quota. Please check OpenAI billing or usage limits."
        )

    else:
        return f"Error {response.status_code}: {response.text}"
