import streamlit as st
from rag.db import (
    add_to_collection,
    get_db_collection,
    query_collection,
    generate_context,
)
from rag.llm import llm_invoke
from rag.document_loader import generate_document_payload

# Page configuration
st.set_page_config(
    page_title="Nepal STI/STD Guidelines Assistant",
    page_icon="🏥",
    layout="wide",
)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

COLLECTION_NAME = "my_project"
collection = get_db_collection(COLLECTION_NAME)

# Sidebar with document loading status
with st.sidebar:
    st.title("🏥 Nepal STI/STD Guidelines")
    st.markdown("""
    This assistant provides information from Nepal's National Guidelines for STI/STD Management.
    
    **Note:** This is an informational tool. Always consult healthcare professionals for medical advice.
    """)
    debug_mode = st.checkbox("Debug Mode")
    if collection.count() > 0:
        st.success("Documents are loaded")
    else:
        with st.spinner("Loading documents..."):
            contents, ids, metadata = generate_document_payload(file_path="docs/project-report.pdf")
            add_to_collection(collection, contents, ids, metadata)
        st.success("Documents loaded successfully")

# Main chat interface
st.title("Nepal STI/STD Management Guidelines Assistant")
st.markdown("""
Welcome to the Nepal STI/STD Guidelines Assistant. Ask questions about:
- Diagnostic protocols
- Treatment guidelines
- Prevention strategies
- Healthcare facility procedures
- Public health measures
""")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar="🤖" if message["role"] == "assistant" else "👤"):
        st.write(message["content"])

# Chat input
if prompt := st.chat_input("Ask about the Medicine Vending Machine..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message immediately
    with st.chat_message("user", avatar="👤"):
        st.write(prompt)

    # Generate and display assistant response
    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("Thinking..."):
            try:
                query_result = query_collection(collection, prompt)
                if debug_mode:
                    st.write("Debug - Query Result:", query_result)
                
                context = generate_context(query_result)
                if debug_mode:
                    st.write("Debug - Context:", context[:200])
                
                response = llm_invoke(context, prompt)
                st.write(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                error_msg = f"An error occurred: {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})

# Clear chat button in sidebar
with st.sidebar:
    if st.button("Clear Chat History", type="primary"):
        st.session_state.messages = []
        st.rerun()
