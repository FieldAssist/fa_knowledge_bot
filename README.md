# FA Knowledge Bot

A powerful document-based chatbot built with Azure OpenAI and Streamlit. This bot uses Retrieval-Augmented Generation (RAG) to provide accurate answers based on your documents.

## Features

- Document upload support for multiple formats (PDF, DOCX, TXT, XLSX, Images)
- Persistent knowledge base using FAISS vector store
- Incremental document addition
- Intelligent context retrieval using Maximum Marginal Relevance
- Clean and modern chat interface
- Source citations for answers

## Setup

1. Clone the repository:
```bash
git clone https://github.com/FieldAssist/fa_knowledge_bot.git
cd fa_knowledge_bot
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
.\venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file with your Azure OpenAI credentials:
```env
AZURE_OPENAI_API_KEY=your_api_key
AZURE_OPENAI_ENDPOINT=your_endpoint
AZURE_OPENAI_API_VERSION=2024-02-15-preview
AZURE_OPENAI_CHAT_DEPLOYMENT=gpt35turbo
AZURE_OPENAI_EMBEDDING_DEPLOYMENT=embedding
```

5. Run the application:
```bash
streamlit run app.py
```

## Usage

1. Upload Documents:
   - Use the sidebar to upload your documents
   - Supported formats: PDF, DOCX, TXT, XLSX, JPG, JPEG, PNG
   - Documents are automatically processed and added to the knowledge base

2. Chat with Your Documents:
   - Ask questions about your documents
   - Get accurate answers with source citations
   - Add more documents at any time to expand the knowledge base

3. Persistent Knowledge:
   - Your knowledge base is saved between sessions
   - No need to re-upload documents every time
   - Incrementally add new documents as needed

## Technical Details

- Built with Python 3.11
- Uses Azure OpenAI for embeddings and chat
- FAISS vector store for efficient similarity search
- LangChain for document processing and chat chain
- Streamlit for the web interface

## Contributing

Feel free to open issues or submit pull requests for any improvements.
