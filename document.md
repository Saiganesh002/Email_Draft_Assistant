# AI Email Draft Assistant – Documentation

## Introduction

The goal of this project was to build a Proof of Concept (POC) to apply the concepts learned during the GenAI sessions. Instead of focusing on complex features, the idea was to create something practical and demonstrate modern AI application development patterns.

I chose to build an Email Draft Assistant because writing emails is a common task in daily work, and it clearly shows how LangChain agents, tool calling, and RAG implementation work in a real use case.

## Why This Use Case

Email drafting is a good example because:
- It is simple to understand
- Everyone writes emails at work
- The output quality can clearly show the effect of LangChain agent reasoning
- This project helps convert a short, informal user request into a complete, professional email with the right tone

## Overall Flow of the Application

At a high level, the application works in the following steps:

1. The user enters a short email request (for example, "Follow up on project status")
2. Selects the tone of the email (formal, professional, casual)
3. Enters the recipient's name and sender name
4. **LangChain agent** analyzes the request and decides to use tools
5. **Agent calls the custom tool** `fetch_email_template` to retrieve relevant templates
6. **RAG system** searches local templates and returns the most relevant one
7. **Agent generates email** using LLM with template context
8. The generated email is displayed in the UI along with template relevance scores

## LangChain Agent Architecture

The application uses a **Zero-shot ReAct agent** that:
- Receives user prompts and analyzes them
- Decides when to use the `fetch_email_template` tool
- Reasons about the best approach to generate emails
- Combines tool outputs with LLM capabilities

### Agent Configuration
```python
agent = initialize_agent(
    tools=[fetch_email_template],
    llm=ChatOpenAI(model="gpt-3.5-turbo"),
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION
)
```

## Custom Tool Implementation

The project implements a custom LangChain tool for template retrieval:

```python
@tool
def fetch_email_template(query: str) -> str:
    """
    Fetch a relevant email template based on the user's email request.
    Use this tool when drafting an email that may benefit from a predefined template.
    """
    return get_rag_context(query)
```

This tool:
- Is automatically discovered by the LangChain agent
- Gets called when the agent determines it needs template context
- Integrates seamlessly with the RAG system

## RAG Implementation

Instead of using a vector database, a simple but effective RAG approach is implemented:

### Retrieval Process
1. **Template Storage**: Email templates stored as local `.txt` files
2. **Query Analysis**: User request is analyzed for keywords and intent
3. **Template Matching**: Priority matching for specific phrases:
   - "follow up" → `follow_up.txt`
   - "meeting" → `meeting_request.txt`
   - "thank" → `thank_you.txt`
   - "apolog" → `apology.txt`
4. **Fallback Matching**: Keyword-based matching for edge cases

### Augmentation Process
- Retrieved templates provide structural context to the LLM
- Templates guide email format and professional language
- Agent uses templates as inspiration, not direct copying

### Generation Process
- LLM generates emails using template context
- Agent ensures proper personalization with names
- Output formatting is handled automatically

## Email Templates

The templates represent common email types:
- **Follow-up emails** - Project status updates, meeting follow-ups
- **Meeting requests** - Scheduling and coordination
- **Thank-you emails** - Appreciation and acknowledgment
- **Apology emails** - Professional apologies and explanations

These templates are not returned directly to the user. Instead, they guide the LLM when generating the final email through the RAG process.

## LLM Integration

The project uses **OpenAI GPT-3.5-turbo** through LangChain:

### Centralized Configuration
```python
# app/llm.py
def get_llm():
    return ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0.5,
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )
```

### Agent Integration
- LLM is configured once and used by the agent
- Temperature set to 0.5 for balanced creativity and consistency
- Handles both reasoning and email generation tasks

## Modular Architecture

The project follows clean separation of concerns:

### File Structure and Responsibilities
- **`streamlit_app.py`** - UI layer and user interaction
- **`app/agent.py`** - LangChain agent orchestration
- **`app/llm.py`** - Centralized LLM configuration
- **`app/tools.py`** - Custom LangChain tool wrapper
- **`app/rag.py`** - Core RAG retrieval logic
- **`templates/`** - Local knowledge base

### Data Flow
```
User Input → Agent → Tool → RAG → Templates → LLM → Generated Email
```

## Template Relevance Scoring

The application provides transparency by showing template relevance scores:
- **Similarity matching** using sequence comparison
- **Keyword bonuses** for exact phrase matches
- **Percentage scores** showing how well each template matched the query

This helps users understand which template influenced the email generation.

## Handling Names and Formatting

The application ensures professional formatting:

### Name Personalization
- User provides recipient and sender names
- Names are integrated into the agent prompt
- LLM personalizes emails automatically

### Post-Processing
- Signature formatting is normalized (ensures sender name on new line)
- Greeting standardization ("Hello" → "Dear")
- Minimum content validation

## API Key Handling

The OpenAI API key is stored securely:
- Stored in `.env` file
- Loaded using environment variables
- Never hardcoded in source files

## Technical Concepts Demonstrated

This project demonstrates all required GenAI concepts:

### LLM Interaction
- Direct integration with OpenAI GPT-3.5-turbo
- Proper prompt engineering and response handling

### LangChain Usage
- Agent framework implementation
- Tool integration and management
- Prompt template handling

### Agent Implementation
- Zero-shot ReAct agent pattern
- Autonomous tool selection and usage
- Reasoning and decision-making capabilities

### Tool Calling
- Custom tool development with `@tool` decorator
- Seamless integration with agent workflow
- Proper tool description and parameter handling

### RAG Implementation
- Local knowledge base retrieval
- Context augmentation for LLM
- Template-based knowledge enhancement

## Future Enhancements

Potential improvements for the system:
- **Vector embeddings** for more sophisticated template matching
- **Additional email scenarios** by expanding the template set
- **Multi-language support** for international use cases
- **Email history tracking** for context-aware suggestions

## Conclusion

This project successfully demonstrates:
- How LangChain agents can orchestrate complex workflows
- How custom tools integrate with agent reasoning
- How RAG systems enhance LLM capabilities with local knowledge
- How modular architecture supports maintainable AI applications

The project serves as a practical introduction to building production-ready GenAI applications using modern frameworks and best practices.