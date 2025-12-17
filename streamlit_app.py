import streamlit as st
from email_assistant import (
    retrieve_relevant_templates,
    build_prompt,
    generate_email
)

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
    "Generate professional emails using prompt engineering, few-shot learning, "
    "and template-based context (RAG-style)."
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
    "Recipient’s Name",
    placeholder="Enter the recipient's name here"
)

sender_name = st.text_input(
    "Sender’s Name",
    placeholder="Enter your name here"
)

# =========================
# Action button
# =========================
if st.button("Generate Email"):
    if not user_query.strip():
        st.warning("Please enter an email request.")
    else:
        with st.spinner("Generating email..."):
            retrieved_templates = retrieve_relevant_templates(user_query)

            enhanced_request = (
                f"{user_query}\n"
                f"Recipient Name: {recipient_name}\n"
                f"Sender Name: {sender_name}"
            )

            final_prompt = build_prompt(
                user_request=enhanced_request,
                tone=tone,
                retrieved_templates=retrieved_templates
            )

            generated_email = generate_email(final_prompt)

        # =========================
        # Output
        # =========================
        st.subheader("📄 Generated Email")
        st.write(generated_email)

        st.subheader("📌 Retrieved Template(s)")
        for score, name, _ in retrieved_templates:
            st.write(f"- **{name}** (relevance score: {score})")
