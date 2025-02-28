# Development Guide

This guide provides instructions for developers who want to contribute to the FA Knowledge Bot project.

## Development Environment Setup

### Prerequisites

1. Python 3.11 or higher
2. Git
3. Azure OpenAI API access
4. Visual Studio Code (recommended)

### Local Development Setup

1. **Clone the Repository**
```bash
git clone https://github.com/FieldAssist/fa_knowledge_bot.git
cd fa_knowledge_bot
```

2. **Create Virtual Environment**
```bash
python -m venv venv
.\venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure Environment Variables**
```bash
cp .env.example .env
# Edit .env with your Azure OpenAI credentials
```

5. **Run Tests**
```bash
python -m pytest tests/
```

## Project Structure

```
fa_knowledge_bot/
├── docs/                    # Documentation
│   ├── technical_architecture.md
│   ├── api_reference.md
│   └── development_guide.md
├── tests/                   # Test files
│   ├── test_document_processor.py
│   ├── test_vector_store.py
│   └── test_chat.py
├── vector_store/           # Persistent vector store
├── temp/                   # Temporary file storage
├── .env                    # Environment variables
├── .env.example           # Example environment file
├── .gitignore            # Git ignore rules
├── README.md             # Project documentation
├── requirements.txt      # Python dependencies
└── app.py               # Main application file
```

## Code Style Guidelines

### Python Style Guide

1. **PEP 8 Compliance**
   - Use 4 spaces for indentation
   - Maximum line length of 88 characters (Black formatter)
   - Use meaningful variable names

2. **Type Hints**
```python
def process_document(file_path: str) -> List[Document]:
    """
    Process a document and return a list of Document objects.
    
    Args:
        file_path: Path to the document file
        
    Returns:
        List of processed Document objects
    """
    # Implementation
```

3. **Documentation**
   - Use docstrings for all functions and classes
   - Include type hints for parameters and return values
   - Document exceptions and edge cases

### Git Workflow

1. **Branch Naming**
```
feature/   # New features
bugfix/    # Bug fixes
hotfix/    # Urgent fixes
docs/      # Documentation updates
```

2. **Commit Messages**
```
feat: Add support for PDF processing
fix: Handle empty document uploads
docs: Update technical architecture
test: Add vector store tests
```

3. **Pull Request Process**
   - Create feature branch
   - Make changes and test
   - Submit PR with description
   - Address review comments

## Testing Guidelines

### Unit Tests

1. **Test Structure**
```python
def test_document_processing():
    # Arrange
    file_path = "test_data/sample.pdf"
    
    # Act
    result = process_document(file_path)
    
    # Assert
    assert len(result) > 0
    assert isinstance(result[0], Document)
```

2. **Test Coverage**
   - Aim for 80%+ coverage
   - Test edge cases
   - Test error conditions

### Integration Tests

1. **Vector Store Tests**
```python
def test_vector_store_persistence():
    # Test saving and loading
    documents = [Document("test")]
    store = create_vector_store(documents)
    store.save("test_store")
    
    loaded_store = load_vector_store("test_store")
    assert loaded_store.similarity_search("test")
```

2. **Chat Tests**
```python
def test_chat_response():
    # Test chat functionality
    question = "What is in the document?"
    response = get_chat_response(question)
    assert response
    assert len(response) > 0
```

## Performance Optimization

### Vector Store

1. **Batch Processing**
```python
def batch_process_documents(documents: List[str], batch_size: int = 1000):
    for i in range(0, len(documents), batch_size):
        batch = documents[i:i + batch_size]
        process_batch(batch)
```

2. **Caching**
```python
from functools import lru_cache

@lru_cache(maxsize=1000)
def get_document_embedding(text: str) -> List[float]:
    return embeddings.embed_query(text)
```

### Memory Management

1. **File Cleanup**
```python
def cleanup_temp_files():
    temp_dir = "temp"
    for file in os.listdir(temp_dir):
        os.remove(os.path.join(temp_dir, file))
```

2. **Resource Management**
```python
class DocumentProcessor:
    def __init__(self):
        self.temp_files = []
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cleanup()
```

## Deployment

### Local Development
```bash
streamlit run app.py
```

### Production Deployment

1. **Docker Setup**
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

CMD ["streamlit", "run", "app.py"]
```

2. **Environment Configuration**
```bash
docker build -t fa-knowledge-bot .
docker run -p 8501:8501 --env-file .env fa-knowledge-bot
```

## Monitoring and Logging

### Application Logging
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)
```

### Performance Monitoring
```python
from time import time

def measure_performance(func):
    def wrapper(*args, **kwargs):
        start = time()
        result = func(*args, **kwargs)
        end = time()
        logger.info(f"{func.__name__} took {end - start:.2f} seconds")
        return result
    return wrapper
```

## Contributing

1. Fork the repository
2. Create your feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

## Support

For questions or issues:
1. Check existing issues
2. Create a new issue
3. Join discussions
4. Contact maintainers

Remember to:
- Follow code style guidelines
- Write tests for new features
- Update documentation
- Be respectful and collaborative
