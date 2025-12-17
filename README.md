# AI Email Draft Assistant

This project is a simple Python-based Proof of Concept (POC) that demonstrates how a Large Language Model (LLM) can be used to generate professional emails using prompt engineering techniques.

The focus of this project is to apply the concepts learned during the GenAI sessions in a practical way.

## Features

- Drafts professional emails using an LLM
- Supports different tones: formal, professional, and casual
- Uses few-shot prompting to improve response quality
- Uses a basic RAG-style approach with local email templates
- Secure API key management using environment variables

## Concepts Demonstrated

- Interaction with LLMs using the OpenAI API
- Use of system and user roles in prompts
- Prompt templates and structured prompt construction
- Few-shot learning
- Basic Retrieval-Augmented Generation (RAG) using local data

## Project Structure
ai-email-draft/
├── email_assistant.py
├── streamlit_app.py
├── requirements.txt
├── README.md
├── .env
└── templates/
├── follow_up.txt
├── meeting_request.txt
├── thank_you.txt
└── apology.txt

## Installation

1. Create and activate a virtual environment:

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate

2. Install dependencies:
pip install -r requirements.txt

3. Set your OpenAI API key in a .env file:
OPENAI_API_KEY=your_openai_api_key_here

4. Run the application:
streamlit run streamlit_app.py
