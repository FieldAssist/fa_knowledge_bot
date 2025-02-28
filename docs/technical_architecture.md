# Technical Architecture

This document outlines the technical architecture of the FA Knowledge Bot, explaining how different components work together to provide document-based question answering capabilities.

## System Architecture

```
┌─────────────────┐     ┌──────────────────┐     ┌───────────────────┐
│   Streamlit UI  │────▶│  Document Upload │────▶│ Document Processor │
└─────────────────┘     └──────────────────┘     └───────────────────┘
         │                                                   │
         │                                                   ▼
         │                                        ┌───────────────────┐
         │                                        │  Text Splitter    │
         │                                        └───────────────────┘
         │                                                   │
         │                                                   ▼
         │                                        ┌───────────────────┐
         │                                        │  Azure Embeddings │
         │                                        └───────────────────┘
         │                                                   │
         │                                                   ▼
         │                                        ┌───────────────────┐
         │                                        │   FAISS Index     │
         │                                        └───────────────────┘
         │                                                   ▲
         │                                                   │
         ▼                                                   │
┌─────────────────┐     ┌──────────────────┐     ┌───────────────────┐
│   Chat Input    │────▶│  Query Processor │────▶│  Context Retriever│
└─────────────────┘     └──────────────────┘     └───────────────────┘
         │                                                   │
         ▼                                                   ▼
┌─────────────────┐     ┌──────────────────┐     ┌───────────────────┐
│  Chat Response  │◀────│   Azure OpenAI   │◀────│   RAG Pipeline    │
└─────────────────┘     └──────────────────┘     └───────────────────┘
```

## Component Details

### 1. Document Processing Pipeline

#### Document Upload
- Supports multiple file formats (PDF, DOCX, TXT, XLSX, Images)
- Uses specialized loaders for each format:
  - `PyPDFLoader` for PDFs
  - `Docx2txtLoader` for Word documents
  - `TextLoader` for text files
  - `UnstructuredExcelLoader` for Excel files
  - `UnstructuredImageLoader` for images

#### Text Extraction & Chunking
- `RecursiveCharacterTextSplitter` splits documents into manageable chunks
- Configuration:
  ```python
  chunk_size=1500
  chunk_overlap=300
  separators=["\n\n", "\n", " ", ""]
  ```
- Overlap ensures context continuity between chunks

### 2. Vector Store Implementation

#### Azure OpenAI Embeddings
- Uses `text-embedding-ada-002` model
- Converts text chunks into high-dimensional vectors
- Configuration:
  ```python
  deployment_name="embedding"
  chunk_size=1000
  ```

#### FAISS Vector Store
- Facebook AI Similarity Search (FAISS) for efficient similarity search
- Features:
  - Fast nearest neighbor search
  - Efficient vector indexing
  - Persistent storage
- Index saved to disk for persistence between sessions

### 3. RAG Pipeline

#### Context Retrieval
- Uses Maximum Marginal Relevance (MMR) search
- Configuration:
  ```python
  search_type="mmr"
  k=5           # Number of documents to retrieve
  fetch_k=8     # Number of documents to fetch before reranking
  lambda_mult=0.7  # Diversity vs relevance trade-off
  ```

#### Query Processing
- Converts user questions into embeddings
- Retrieves relevant context using MMR
- Maintains conversation history for context

#### Response Generation
- Uses Azure OpenAI GPT-3.5 Turbo
- Configuration:
  ```python
  deployment_name="gpt35turbo"
  temperature=0.3  # Lower temperature for focused responses
  ```
- Custom prompt template for consistent responses

### 4. User Interface

#### Streamlit Components
- Document upload interface in sidebar
- Chat history display with custom CSS
- Real-time chat input
- Source citation display

#### Session Management
- Persistent vector store between sessions
- Conversation history tracking
- Incremental document addition

## Data Flow

1. **Document Processing**:
   ```
   Document → Text Extraction → Chunking → Embedding → Vector Store
   ```

2. **Query Processing**:
   ```
   Question → Embedding → Similarity Search → Context Retrieval → RAG → Response
   ```

3. **Knowledge Base Updates**:
   ```
   New Document → Processing Pipeline → Vector Store Update → Immediate Availability
   ```

## Performance Considerations

### Vector Store
- FAISS optimized for similarity search
- Efficient index structure for fast retrieval
- Persistent storage reduces reload time

### Context Retrieval
- MMR balances relevance and diversity
- Configurable parameters for fine-tuning
- Overlap in chunks maintains context

### Response Generation
- Low temperature for focused answers
- Source citations for transparency
- Conversation history for context

## Security Considerations

### API Keys
- Stored in `.env` file
- Not committed to version control
- Required for Azure OpenAI services

### Document Storage
- Temporary storage for processing
- Automatic cleanup
- Vector store persistence with safe deserialization

## Future Improvements

1. **Scalability**
   - Distributed vector store
   - Batch processing for large documents
   - Caching for frequent queries

2. **Features**
   - Multi-language support
   - Advanced document parsing
   - User authentication
   - Query logging and analytics

3. **Performance**
   - Optimized chunk size
   - Advanced embedding techniques
   - Response streaming

4. **Security**
   - Role-based access control
   - Document encryption
   - Audit logging
