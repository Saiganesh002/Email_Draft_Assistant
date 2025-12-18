# AI Email Draft Assistant

This project demonstrates how to build an intelligent email drafting system using LangChain agents, tools, and RAG implementation. It generates professional emails by combining LLM capabilities with local template knowledge.

## Features

- Generates professional emails using LangChain agents
- Supports multiple tones: formal, professional, and casual
- Implements RAG with local email templates
- Shows template relevance scoring
- Automatic email formatting and signature handling
- Streamlit web interface

## Concepts Demonstrated

- **LLM Interaction**: Direct integration with OpenAI GPT-3.5-turbo
- **LangChain Usage**: Agents, tools, and prompt management
- **Agent Implementation**: Zero-shot ReAct agent with tool calling
- **Tool Calling**: Custom email template retrieval tool
- **RAG Implementation**: Template-based knowledge retrieval and augmentation

## Project Structure
```
ai-email-draft/
├── streamlit_app.py          # Main Streamlit application
├── app/
│   ├── __init__.py
│   ├── agent.py              # LangChain agent configuration
│   └── tools.py              # Custom tools for template retrieval
├── templates/                # Email template knowledge base
│   ├── follow_up.txt
│   ├── meeting_request.txt
│   ├── thank_you.txt
│   └── apology.txt
├── requirements.txt
├── README.md
└── .env                      # API keys
```

## Installation

1. Create and activate a virtual environment:
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

2. Install dependencies:
```bash
pip install streamlit langchain langchain-openai python-dotenv
```

3. Set your OpenAI API key in a .env file:
```
OPENAI_API_KEY=your_openai_api_key_here
```

4. Run the application:
```bash
streamlit run streamlit_app.py
```

## How It Works

1. **User Input**: Enter email request, tone, recipient, and sender details
2. **Agent Processing**: LangChain agent analyzes the request
3. **Tool Calling**: Agent calls `fetch_email_template` tool to retrieve relevant templates
4. **RAG Process**: Templates provide context to augment LLM knowledge
5. **Email Generation**: LLM generates professional email using retrieved context
6. **Template Scoring**: System shows relevance scores for all templates

## Technical Architecture

- **Agent**: Zero-shot ReAct agent with GPT-3.5-turbo
- **Tools**: Custom LangChain tool for template retrieval
- **RAG**: Local file-based knowledge retrieval system
- **UI**: Streamlit for interactive web interface