import streamlit as st
import os
import sys
import shutil

# Ensure proper path visibility
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from rag_core import RAGCore

st.set_page_config(page_title="Document QA System", page_icon="🤖")

@st.cache_resource
def get_rag_system():
    try:
        # Try getting key from secrets first, then environment
        api_key = None
        if "GEMINI_API_KEY" in st.secrets:
            api_key = st.secrets["GEMINI_API_KEY"]
            
        return RAGCore(api_key=api_key)
    except Exception as e:
        st.error(f"Failed to initialize RAG System: {e}")
        return None

def save_uploaded_file(uploaded_file):
    """Save uploaded file to disk and return the path."""
    try:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        file_dir = os.path.join(base_dir, "file")
        os.makedirs(file_dir, exist_ok=True)
        
        file_path = os.path.join(file_dir, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        return file_path
    except Exception as e:
        return None

def main():
    st.title("📄 Dynamic PDF Q&A")
    st.markdown("Upload any PDF to summarize it and ask questions.")

    rag = get_rag_system()
    if not rag:
        st.stop()
        
    # Sidebar
    st.sidebar.header("Upload Document")
    uploaded_file = st.sidebar.file_uploader("Choose a PDF", type=["pdf"])

    # Initialize session state for file tracking
    if "current_file" not in st.session_state:
        st.session_state.current_file = None
        
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Handle Upload Logic
    if uploaded_file:
        # If a new file is uploaded (different name than what we processed last)
        if st.session_state.current_file != uploaded_file.name:
            with st.spinner(f"Processing {uploaded_file.name}..."):
                # Save file
                saved_path = save_uploaded_file(uploaded_file)
                if saved_path:
                    try:
                        # Process file
                        if rag.process_document(saved_path):
                            st.session_state.current_file = uploaded_file.name
                            st.session_state.messages = [] # Clear chat on new file
                            st.success(f"✅ Processed {uploaded_file.name}")
                        else:
                            st.error("❌ Processing failed.")
                    except Exception as e:
                        st.error(f"Error during processing: {e}")
                else:
                    st.error("Error saving file.")
    
    # Just show current status if no file uploaded but one exists in system
    elif st.sidebar.button("Re-process Default File"):
         with st.spinner("Processing default document..."):
            rag.process_document()
            st.success("Default document processed.")

    # Chat Interface
    st.divider()

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask a question about the document..."):
        # Display user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate answer
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            message_placeholder.markdown("Thinking...")
            
            try:
                # Check if system is ready
                if not rag.index:
                    if not rag._load_resources():
                         st.error("Index not found. Please upload a document first.")
                         st.stop()

                full_response = rag.answer(prompt)
                message_placeholder.markdown(full_response)
                
                # Show sources expander
                try:
                    sources = rag.retrieve(prompt)
                    with st.expander("View Sources"):
                        for i, source in enumerate(sources):
                            st.markdown(f"**Source {i+1}:**\n{source}\n---")
                except:
                    pass

                st.session_state.messages.append({"role": "assistant", "content": full_response})
            except Exception as e:
                message_placeholder.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
