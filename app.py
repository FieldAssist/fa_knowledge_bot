import streamlit as st
import os
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import (
    PyPDFLoader,
    Docx2txtLoader,
    TextLoader,
    UnstructuredExcelLoader,
    UnstructuredImageLoader,
)
from langchain_openai import AzureOpenAIEmbeddings, AzureChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain_community.vectorstores import FAISS

# Load environment variables
load_dotenv()

# Azure OpenAI settings
OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
OPENAI_API_BASE = os.getenv("AZURE_OPENAI_ENDPOINT")
OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION")
OPENAI_MODEL = os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT")
OPENAI_EMBEDDING_MODEL = os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT")

# Print environment variables for debugging (excluding API key)
print("API Base:", OPENAI_API_BASE)
print("API Version:", OPENAI_API_VERSION)
print("Embedding Model:", OPENAI_EMBEDDING_MODEL)
print("Chat Model:", OPENAI_MODEL)

def process_file(file, file_type):
    # Create a temporary file to store the uploaded content
    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file_type}") as tmp_file:
        tmp_file.write(file.getvalue())
        file_path = tmp_file.name

    try:
        if file_type in ["pdf"]:
            loader = PyPDFLoader(file_path)
        elif file_type in ["docx", "doc"]:
            loader = Docx2txtLoader(file_path)
        elif file_type in ["txt"]:
            loader = TextLoader(file_path)
        elif file_type in ["xlsx", "xls"]:
            loader = UnstructuredExcelLoader(file_path)
        elif file_type in ["jpg", "jpeg", "png"]:
            loader = UnstructuredImageLoader(file_path)
        else:
            raise ValueError(f"Unsupported file type: {file_type}")
        
        return loader.load()
    finally:
        # Clean up the temporary file
        os.unlink(file_path)

def load_document(file_path):
    file_type = file_path.split(".")[-1].lower()
    if file_type in ["pdf"]:
        loader = PyPDFLoader(file_path)
    elif file_type in ["docx", "doc"]:
        loader = Docx2txtLoader(file_path)
    elif file_type in ["txt"]:
        loader = TextLoader(file_path)
    elif file_type in ["xlsx", "xls"]:
        loader = UnstructuredExcelLoader(file_path)
    elif file_type in ["jpg", "jpeg", "png"]:
        loader = UnstructuredImageLoader(file_path)
    else:
        raise ValueError(f"Unsupported file type: {file_type}")
    
    return loader.load()

def initialize_vector_store():
    # Create vector store directory if it doesn't exist
    if not os.path.exists("vector_store"):
        os.makedirs("vector_store")
    
    # Initialize embeddings
    embeddings = AzureOpenAIEmbeddings(
        azure_deployment=OPENAI_EMBEDDING_MODEL,
        openai_api_version=OPENAI_API_VERSION,
        openai_api_key=OPENAI_API_KEY,
        azure_endpoint=OPENAI_API_BASE,
        chunk_size=1000
    )
    
    # Load existing vector store if it exists
    if os.path.exists("vector_store/index.faiss"):
        vector_store = FAISS.load_local(
            "vector_store",
            embeddings,
            allow_dangerous_deserialization=True  # Safe since we created this file ourselves
        )
        print("Loaded existing vector store")
    else:
        vector_store = None
        print("No existing vector store found")
    
    return vector_store, embeddings

def add_documents_to_vectorstore(documents, vector_store=None, embeddings=None):
    # Split documents into chunks with more overlap for better context
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1500,
        chunk_overlap=300,
        length_function=len,
        separators=["\n\n", "\n", " ", ""]
    )
    splits = text_splitter.split_documents(documents)

    if vector_store is None:
        # Create new vector store
        vector_store = FAISS.from_documents(splits, embeddings)
    else:
        # Add to existing vector store
        vector_store.add_documents(splits)
    
    # Save vector store
    vector_store.save_local("vector_store")
    return vector_store

CHAT_TEMPLATE = """You are a helpful AI assistant. Use the following pieces of context to answer the question at the end.
If you don't know the answer, just say that you don't know. DO NOT try to make up an answer.

Context:
{context}

Question: {question}

Previous conversation:
{chat_history}

Instructions:
1. Carefully analyze the context and the question
2. Consider the previous conversation for context
3. If the answer is in the context, provide a detailed response
4. If you're unsure or the information isn't in the context, say so
5. Always cite specific parts of the context to support your answer

Answer:"""

def initialize_chat_chain(vector_store):
    retriever = vector_store.as_retriever(
        search_type="mmr",
        search_kwargs={
            "k": 5,
            "fetch_k": 8,
            "lambda_mult": 0.7
        }
    )
    
    llm = AzureChatOpenAI(
        azure_deployment=OPENAI_MODEL,
        openai_api_version=OPENAI_API_VERSION,
        openai_api_key=OPENAI_API_KEY,
        azure_endpoint=OPENAI_API_BASE,
        temperature=0.3
    )
    
    return ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        return_source_documents=True,
        combine_docs_chain_kwargs={"prompt": PromptTemplate(
            input_variables=["context", "question", "chat_history"],
            template=CHAT_TEMPLATE
        )}
    )

# Configure page
st.set_page_config(
    page_title="Knowledge Base Chatbot",
    page_icon="🤖",
    layout="wide"
)

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

if 'vector_store' not in st.session_state:
    st.session_state.vector_store, st.session_state.embeddings = initialize_vector_store()

if 'chat_chain' not in st.session_state and st.session_state.vector_store is not None:
    st.session_state.chat_chain = initialize_chat_chain(st.session_state.vector_store)

# Custom CSS
st.markdown("""
<style>
    .main {
        color: #000000;
    }
    .stTextArea textarea {
        color: #000000;
    }
    .stChatMessage {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 10px;
        margin: 5px 0;
    }
    .stChatMessage p {
        color: #000000 !important;
        margin: 0;
    }
    .user-message {
        background-color: #e3f2fd;
    }
    .assistant-message {
        background-color: #f5f5f5;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar for document upload
with st.sidebar:
    st.title("Document Upload")
    uploaded_files = st.file_uploader(
        "Upload documents",
        type=["pdf", "docx", "txt", "xlsx", "jpg", "jpeg", "png"],
        accept_multiple_files=True
    )
    
    if uploaded_files:
        with st.spinner("Processing documents..."):
            # Process uploaded documents
            documents = []
            for file in uploaded_files:
                # Save uploaded file temporarily
                file_path = os.path.join("temp", file.name)
                os.makedirs("temp", exist_ok=True)
                with open(file_path, "wb") as f:
                    f.write(file.getvalue())
                
                # Load document based on file type
                documents.extend(load_document(file_path))
                
                # Clean up
                os.unlink(file_path)
            
            if documents:
                # Add documents to vector store
                st.session_state.vector_store = add_documents_to_vectorstore(
                    documents,
                    st.session_state.vector_store,
                    st.session_state.embeddings
                )
                
                # Initialize chat chain if not already initialized
                if 'chat_chain' not in st.session_state:
                    st.session_state.chat_chain = initialize_chat_chain(st.session_state.vector_store)
                
                st.success("Documents processed successfully!")

# Main chat interface
st.title("Chat with your Documents")
st.markdown("---")

if st.session_state.vector_store is None:
    st.info("Please upload some documents in the sidebar to start chatting.")
else:
    # Chat container
    chat_container = st.container()
    
    # Display chat messages
    for message in st.session_state.chat_history:
        role_class = "user-message" if message["role"] == "user" else "assistant-message"
        with st.container():
            st.markdown(f"""
                <div class="stChatMessage {role_class}">
                    <p><strong>{'You' if message["role"] == "user" else 'Assistant'}:</strong> {message["content"]}</p>
                </div>
            """, unsafe_allow_html=True)
    
    # Chat input
    st.markdown("---")
    user_question = st.chat_input("Ask a question about your documents...")
    
    if user_question:
        with st.spinner("Thinking..."):
            result = st.session_state.chat_chain({
                "question": user_question,
                "chat_history": [(msg["role"], msg["content"]) 
                               for msg in st.session_state.chat_history]
            })
            
            # Format answer with source citations if available
            answer = result["answer"]
            source_docs = result.get("source_documents", [])
            if source_docs:
                answer += "\n\nSources:"
                seen_sources = set()
                for doc in source_docs:
                    if doc.metadata.get("source") not in seen_sources:
                        seen_sources.add(doc.metadata.get("source"))
                        answer += f"\n- {doc.metadata.get('source', 'Unknown source')}"
            
            # Add to chat history
            st.session_state.chat_history.append({"role": "user", "content": user_question})
            st.session_state.chat_history.append({"role": "assistant", "content": answer})
            
            # Force refresh
            st.rerun()

# Add clear chat button
if st.session_state.chat_history:
    if st.button("Clear Chat"):
        st.session_state.chat_history = []
        st.session_state.chat_chain = None
        st.rerun()
