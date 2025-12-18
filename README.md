# AI Email Draft Assistant

An intelligent email drafting system built with **LangChain agents**, **custom tools**, and **RAG implementation**. This project demonstrates how to combine LLM capabilities with local knowledge bases to generate professional emails.

---

## Features

- **LangChain Agent Integration** - Zero-shot ReAct agent with GPT-3.5-turbo
- **Custom Tool Calling** - Intelligent template retrieval system
- **RAG Implementation** - Local email template knowledge base
- **Template Relevance Scoring** - Shows which templates match your request
- **Professional Email Generation** - Multiple tones (formal, professional, casual)
- **Streamlit Web Interface** - Clean, interactive user experience

---

## Core Concepts Demonstrated

| Concept | Implementation | Location |
|---------|---------------|----------|
| **LLM Interaction** | Direct OpenAI GPT-3.5-turbo integration | `app/llm.py` |
| **LangChain Usage** | Agents, tools, and prompt management | `app/agent.py` |
| **Agent Implementation** | Zero-shot ReAct agent with tool calling | `app/agent.py` |
| **Tool Calling** | Custom email template retrieval tool | `app/tools.py` |
| **RAG Implementation** | Template-based knowledge retrieval | `app/rag.py` |

---

## Project Architecture

```
ai-email-draft/
├── streamlit_app.py          # Main Streamlit application & UI
├── app/
│   ├── __init__.py           # Package initialization
│   ├── agent.py              # LangChain agent configuration
│   ├── llm.py                # LLM configuration & setup
│   ├── rag.py                # RAG implementation logic
│   └── tools.py              # Custom LangChain tools
├── templates/                # Email template knowledge base
│   ├── follow_up.txt         # Follow-up email template
│   ├── meeting_request.txt   # Meeting request template
│   ├── thank_you.txt         # Thank you email template
│   └── apology.txt           # Apology email template
├── requirements.txt          # Python dependencies
└── .env                      # API keys (create this)
```

---

## Quick Start

### 1. Setup Environment
```bash
# Clone or download the project
cd ai-email-draft

# Create virtual environment
python -m venv venv312

# Activate virtual environment
# Windows:
venv312\Scripts\activate
# macOS/Linux:
source venv312/bin/activate
```

### 2. Install Dependencies
```bash
pip install streamlit langchain langchain-openai python-dotenv
```

### 3. Configure API Key
Create a `.env` file in the project root:
```env
OPENAI_API_KEY=your_openai_api_key_here
```

### 4. Run the Application
```bash
streamlit run streamlit_app.py
```

The app will open in your browser at `http://localhost:8501`

---

## How It Works

### User Journey
1. **Input**: Enter email request, select tone, add recipient/sender names
2. **Agent Processing**: LangChain agent analyzes the request
3. **Tool Execution**: Agent calls `fetch_email_template` tool
4. **RAG Retrieval**: System finds relevant templates from knowledge base
5. **Email Generation**: LLM creates professional email using template context
6. **Relevance Display**: Shows template matching scores

### Technical Flow
```
User Input → streamlit_app.py
                ↓
            app/agent.py → app/llm.py
                ↓
            app/tools.py → app/rag.py → templates/
                ↓
            Generated Email
```

---

## Architecture Details

### Modular Design
- **`streamlit_app.py`** - UI layer and user interaction
- **`app/agent.py`** - LangChain agent orchestration
- **`app/llm.py`** - Centralized LLM configuration
- **`app/tools.py`** - LangChain tool wrapper
- **`app/rag.py`** - Core RAG retrieval logic
- **`templates/`** - Local knowledge base

### RAG Implementation
1. **Retrieval** - `rag.py` searches templates based on user query
2. **Augmentation** - Retrieved templates provide context to the LLM
3. **Generation** - LLM creates emails using template-augmented knowledge

### Agent Workflow
1. Agent receives user prompt
2. Decides to use `fetch_email_template` tool (ReAct reasoning)
3. Tool calls RAG system to retrieve relevant templates
4. Agent generates email using retrieved context
5. Output is processed and formatted

---

## Example Usage

**Input:**
- Request: "Follow up on project status"
- Tone: Professional
- Recipient: John Smith
- Sender: Sarah Johnson

**Output:**
```
Subject: Follow-Up on Project Status

Dear John Smith,

I hope this email finds you well. I wanted to follow up regarding 
our previous discussion on the project status and see if there 
have been any recent developments.

Could you please provide an update on the current progress and 
let me know if there are any next steps that require my attention?

Best regards,
Sarah Johnson
```

**Template Scores:**
- Follow Up: 87.5%
- Meeting Request: 15.2%
- Thank You: 8.1%
- Apology: 12.3%

---

## Customization

### Add New Templates
1. Create new `.txt` file in `templates/` folder
2. Update `app/rag.py` keyword matching if needed
3. Templates automatically become available

### Modify LLM Settings
Edit `app/llm.py` to change:
- Model (GPT-4, Claude, etc.)
- Temperature
- Other parameters

### Extend Functionality
- Add new tools in `app/tools.py`
- Enhance RAG logic in `app/rag.py`
- Customize UI in `streamlit_app.py`

---

## Learning Outcomes

This project demonstrates:
- **LLM Integration** with OpenAI API
- **LangChain Framework** usage
- **Agent-based Architecture** design
- **Custom Tool Development** for LangChain
- **RAG System Implementation** with local data
- **Modular Code Organization** best practices
- **Interactive Web Applications** with Streamlit

Perfect for understanding modern AI application development patterns!

---

## Contributing

Feel free to:
- Add new email templates
- Improve RAG matching algorithms
- Enhance UI/UX design
- Add new features

---

## License

This project is for educational purposes. Make sure to comply with OpenAI's usage policies when using their API.