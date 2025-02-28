# FA Knowledge Bot

A powerful document-based chatbot built with Azure OpenAI and Streamlit. This bot uses Retrieval-Augmented Generation (RAG) to provide accurate answers based on your documents.

## Features

- Document upload support for multiple formats (PDF, DOCX, TXT, XLSX, Images)
- Persistent knowledge base using FAISS vector store
- Incremental document addition
- Intelligent context retrieval using Maximum Marginal Relevance
- Clean and modern chat interface
- Source citations for answers

## Documentation

- [Technical Architecture](docs/technical_architecture.md) - Detailed explanation of how the system works
- [API Reference](docs/api_reference.md) - API documentation for the Azure OpenAI services used
- [Development Guide](docs/development_guide.md) - Guide for developers who want to contribute

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

## Technical Architecture

The system uses a sophisticated RAG (Retrieval-Augmented Generation) architecture:

1. Document Processing:
   - Text extraction from multiple formats
   - Chunk splitting with overlap for context
   - Azure OpenAI embeddings generation

2. Vector Store:
   - FAISS for efficient similarity search
   - Persistent storage between sessions
   - Incremental document addition

3. Query Processing:
   - Maximum Marginal Relevance search
   - Context-aware response generation
   - Source citation tracking

For more details, see the [Technical Architecture](docs/technical_architecture.md) document.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

Please read our [Development Guide](docs/development_guide.md) for detailed instructions.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Azure OpenAI for providing the language models
- LangChain for the document processing pipeline
- FAISS for vector similarity search
- Streamlit for the web interface
