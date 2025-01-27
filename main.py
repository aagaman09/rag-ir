import streamlit as st
from rag.db import (
    add_to_collection,
    get_db_collection,
    query_collection,
    generate_context,
    get_all_documents,
    delete_collection,
)
from rag.llm import convert_to_latex, format_notes_for_display, llm_invoke, prepare_chat_prompt, generate_notes
from rag.document_loader import generate_document_payload

st.title("Query, Notes; Made Fun")

# Initialize the collection
COLLECTION_NAME = "user_uploaded_docs"
collection = get_db_collection(COLLECTION_NAME)

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Upload Document", "Query Document", "Generate Notes", "Generate Quiz"])

if "uploaded_file" not in st.session_state:
    st.session_state.uploaded_file = None
if "generated_notes" not in st.session_state:
    st.session_state.generated_notes = None
if "latex_notes" not in st.session_state:
    st.session_state.latex_notes = None

# Page 1: Upload Document
if page == "Upload Document":
    st.header("Upload a PDF Document")

    uploaded_file = st.file_uploader("Upload a PDF", type="pdf")

    if uploaded_file:
        st.session_state.uploaded_file = uploaded_file
        st.session_state.generated_notes = None
        st.session_state.latex_notes = None

        with open("temp.pdf", "wb") as f:
            f.write(uploaded_file.getbuffer())

        st.write("Clearing existing documents...")
        delete_collection(COLLECTION_NAME)
        collection = get_db_collection(COLLECTION_NAME)

        st.write("Processing PDF...")
        contents, ids, metadata = generate_document_payload(file_path="temp.pdf")
        add_to_collection(collection, contents, ids, metadata)
        st.write("PDF processed and added to database!")

# Page 2: Query Document
elif page == "Query Document":
    st.header("Query the Document")

    if st.session_state.uploaded_file is None:
        st.warning("Please upload a document first from the 'Upload Document' page.")
    else:
        query_text = st.text_input(
            "Ask anything about the uploaded document:",
            placeholder="Type your question here...",
        )

        if query_text and query_text.strip() != "":
            with st.spinner("Searching for answers..."):
                query_result = query_collection(collection, query_text)

                if query_result and query_result["documents"]:
                    context = generate_context(query_result)
                    prompt = prepare_chat_prompt(context, query_text)
                    result = llm_invoke(prompt)

                    st.write("### Answer:")
                    st.write(result)
                else:
                    st.write("No relevant information found in the document.")

# Page 3: Generate Notes
elif page == "Generate Notes":
    st.header("Generate Notes from Document")

    if st.session_state.uploaded_file is None:
        st.warning("Please upload a document first from the 'Upload Document' page.")
    else:
        
        if 'show_latex' not in st.session_state:
            st.session_state.show_latex = False
        if 'notes_generated' not in st.session_state:
            st.session_state.notes_generated = False

        # Generate Notes button
        if st.button("Generate Notes") or st.session_state.notes_generated:
            if not st.session_state.notes_generated:  
                with st.spinner("Generating notes..."):
                    all_documents = get_all_documents(collection)

                    if all_documents:
                        readable_notes, markdown_notes = generate_notes(all_documents)
                        
                        if readable_notes and markdown_notes:
                            st.session_state.readable_notes = readable_notes
                            st.session_state.markdown_notes = markdown_notes
                            st.session_state.notes_generated = True
                    else:
                        st.error("No documents found in the database.")

        
            if hasattr(st.session_state, 'readable_notes'):
                st.write("### Generated Notes:")
                st.write(format_notes_for_display(st.session_state.readable_notes))
                
                # Create two columns for the buttons
                col1, col2 = st.columns([1, 4])
                
                with col1:
                    # Export to LaTeX button
                    if st.button("Export to LaTeX"):
                        st.session_state.show_latex = True
                
                # Show LaTeX content
                if st.session_state.show_latex:
                    latex_notes = convert_to_latex(st.session_state.markdown_notes)
                    st.session_state.latex_notes = latex_notes
                    
                    st.write("### LaTeX Preview:")
                    st.code(latex_notes, language="latex")
                    
                    st.download_button(
                        label="Download LaTeX File",
                        data=latex_notes,
                        file_name="notes.tex",
                        mime="text/plain",
                        key="download_latex"
                    )

        # clear button to reset everything
        if st.session_state.notes_generated:
            if st.button("Clear Notes"):
                st.session_state.notes_generated = False
                st.session_state.show_latex = False
                if 'readable_notes' in st.session_state:
                    del st.session_state.readable_notes
                if 'markdown_notes' in st.session_state:
                    del st.session_state.markdown_notes
                if 'latex_notes' in st.session_state:
                    del st.session_state.latex_notes
                st.experimental_rerun()
