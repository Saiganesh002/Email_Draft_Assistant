import streamlit as st
from app.agent import get_email_agent
import os
from difflib import SequenceMatcher

# =========================
# Page configuration
# =========================
st.set_page_config(
    page_title="AI Email Draft Assistant",
    page_icon="📧",
    layout="centered"
)

st.title("📧 AI Email Draft Assistant")
st.write(
    "Generate professional emails using LangChain agents, tools, "
    "and a simple RAG-style approach."
)

# =========================
# User inputs
# =========================
user_query = st.text_area(
    "Enter your email request",
    placeholder="Follow up on project status / Request sick leave / Schedule a meeting"
)

tone = st.selectbox(
    "Select email tone",
    ["formal", "professional", "casual"]
)

recipient_name = st.text_input(
    "Enter recipient name",
    placeholder="Enter recipient's name here"
)

sender_name = st.text_input(
    "Enter sender name",
    placeholder="Enter sender's name here"
)

# =========================
# Helper function for template relevance
# =========================
def calculate_template_relevance(user_query):
    """Calculate relevance scores for all templates"""
    template_folder = "templates"
    templates = {}
    
    for file in os.listdir(template_folder):
        if file.endswith(".txt"):
            with open(os.path.join(template_folder, file), "r", encoding="utf-8") as f:
                templates[file] = f.read()
    
    query_lower = user_query.lower()
    relevance_scores = {}
    
    for name, content in templates.items():
        # Calculate similarity score
        similarity = SequenceMatcher(None, query_lower, content.lower()).ratio()
        
        # Keyword matching bonus
        keyword_bonus = 0
        if "follow up" in query_lower and "follow_up" in name:
            keyword_bonus = 0.5
        elif "meeting" in query_lower and "meeting" in name:
            keyword_bonus = 0.5
        elif "thank" in query_lower and "thank" in name:
            keyword_bonus = 0.5
        elif "apolog" in query_lower and "apology" in name:
            keyword_bonus = 0.5
            
        final_score = min(1.0, similarity + keyword_bonus)
        relevance_scores[name.replace('.txt', '')] = round(final_score * 100, 1)
    
    return relevance_scores

# =========================
# Action button
# =========================
if st.button("Generate Email"):
    if not user_query.strip():
        st.warning("Please enter an email request.")
    else:
        with st.spinner("Generating email..."):
            agent = get_email_agent()

            agent_prompt = f"""
Generate a complete professional email for: {user_query}

Recipient: {recipient_name}
Sender: {sender_name}
Tone: {tone}

Requirements:
- Use fetch_email_template tool as inspiration and expand moderately
- Write 2-3 concise paragraphs with 2-3 sentences each
- Keep it professional but brief - around 100-150 words
- Include subject line, greeting, body, and signature
- Start with "Dear {recipient_name},"
- End with "Best regards," then "{sender_name}" on next line
- Focus specifically on: {user_query}
- Be clear, direct, and professional

CRITICAL: Templates are just basic structures - CREATE MUCH MORE DETAILED CONTENT.
IMPORTANT: Return ONLY the final email text, no explanations or reasoning.
"""

            response = agent.run(agent_prompt)
            
            # Extract only the email content if agent shows reasoning
            if "Subject:" in response and ("I will" in response or "Action:" in response):
                # Find the actual email content after agent reasoning
                lines = response.split('\n')
                email_start = -1
                for i, line in enumerate(lines):
                    if line.strip().startswith('Subject:'):
                        email_start = i
                        break
                if email_start >= 0:
                    response = '\n'.join(lines[email_start:]).strip()

            # =========================
            # OUTPUT NORMALIZATION
            # =========================

            # Normalize greeting
            if recipient_name:
                response = response.replace(
                    f"Hello {recipient_name},",
                    f"Dear {recipient_name},"
                )

            # Normalize signature - ensure sender name is on new line
            if sender_name:
                import re
                # Handle various closing formats followed by sender name
                pattern = r'(Best regards|Sincerely|Thanks|Regards|Kind regards),\s*' + re.escape(sender_name)
                response = re.sub(pattern, r'\1,\n' + sender_name, response, flags=re.IGNORECASE)

            # Ensure minimum content and proper structure
            lines = [line for line in response.split("\n") if line.strip()]
            if len(lines) < 8:  # Reduced minimum requirement for shorter emails
                # Add more content if email is too short
                if "I hope this email finds you well." not in response:
                    response = response.replace(
                        f"Dear {recipient_name},",
                        f"Dear {recipient_name},\n\nI hope this email finds you well."
                    )

        # =========================
        # Output
        # =========================
        st.subheader("📄 Generated Email")
        st.write(response)
        
        # =========================
        # Template Relevance Scores
        # =========================
        st.subheader("📊 Template Relevance Scores")
        relevance_scores = calculate_template_relevance(user_query)
        
        col1, col2 = st.columns(2)
        with col1:
            for template, score in list(relevance_scores.items())[:2]:
                st.metric(f"{template.replace('_', ' ').title()}", f"{score}%")
        with col2:
            for template, score in list(relevance_scores.items())[2:]:
                st.metric(f"{template.replace('_', ' ').title()}", f"{score}%")
