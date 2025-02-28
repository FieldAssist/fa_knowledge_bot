# API Reference

This document provides detailed information about the Azure OpenAI APIs used in the FA Knowledge Bot.

## Azure OpenAI Services

### Text Embeddings API

**Model**: text-embedding-ada-002
**Endpoint**: `{AZURE_OPENAI_ENDPOINT}/openai/deployments/{deployment-name}/embeddings`
**API Version**: 2024-02-15-preview

#### Configuration
```python
from langchain_openai import AzureOpenAIEmbeddings

embeddings = AzureOpenAIEmbeddings(
    azure_deployment="embedding",
    openai_api_version="2024-02-15-preview",
    openai_api_key="your-api-key",
    azure_endpoint="your-endpoint",
    chunk_size=1000
)
```

#### Parameters
- `chunk_size`: Number of tokens to process at once
- `max_retries`: Number of retries for failed requests
- `request_timeout`: Timeout for API requests

### Chat Completion API

**Model**: GPT-3.5 Turbo
**Endpoint**: `{AZURE_OPENAI_ENDPOINT}/openai/deployments/{deployment-name}/chat/completions`
**API Version**: 2024-02-15-preview

#### Configuration
```python
from langchain_openai import AzureChatOpenAI

llm = AzureChatOpenAI(
    azure_deployment="gpt35turbo",
    openai_api_version="2024-02-15-preview",
    openai_api_key="your-api-key",
    azure_endpoint="your-endpoint",
    temperature=0.3
)
```

#### Parameters
- `temperature`: Controls randomness (0.0 to 1.0)
- `max_tokens`: Maximum tokens in response
- `presence_penalty`: Penalty for new topics
- `frequency_penalty`: Penalty for repetition

## Environment Variables

Required environment variables for API configuration:

```env
AZURE_OPENAI_API_KEY=your-api-key
AZURE_OPENAI_ENDPOINT=your-endpoint
AZURE_OPENAI_API_VERSION=2024-02-15-preview
AZURE_OPENAI_CHAT_DEPLOYMENT=gpt35turbo
AZURE_OPENAI_EMBEDDING_DEPLOYMENT=embedding
```

## Rate Limits

Azure OpenAI services have rate limits that vary by tier:

- Embeddings API: Tokens per minute (TPM) limit
- Chat Completion API: Requests per minute (RPM) limit

Contact Azure support for specific limits based on your subscription.

## Error Handling

Common API errors and their handling:

```python
try:
    response = embeddings.embed_documents(texts)
except Exception as e:
    if "rate limit" in str(e).lower():
        # Handle rate limit
        time.sleep(60)
        response = embeddings.embed_documents(texts)
    elif "invalid api key" in str(e).lower():
        # Handle authentication error
        raise ValueError("Invalid API key")
    else:
        # Handle other errors
        raise e
```

## Best Practices

1. **Rate Limiting**
   - Implement exponential backoff
   - Cache frequent embeddings
   - Batch requests when possible

2. **Error Handling**
   - Implement proper retry logic
   - Log API errors for debugging
   - Handle rate limits gracefully

3. **Security**
   - Store API keys securely
   - Use environment variables
   - Implement request validation

4. **Performance**
   - Batch similar requests
   - Cache responses where appropriate
   - Monitor API usage

## Example Usage

### Embedding Documents
```python
# Create embeddings for a document
texts = text_splitter.split_text(document)
embeddings_list = embeddings.embed_documents(texts)

# Store in FAISS
vector_store = FAISS.from_texts(texts, embeddings)
```

### Chat Completion
```python
# Generate a response
response = llm.generate_response(
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_question}
    ]
)
```

## Monitoring and Logging

Important metrics to monitor:

1. **API Performance**
   - Response times
   - Success rates
   - Rate limit usage

2. **Usage Metrics**
   - Token consumption
   - Request volume
   - Error rates

3. **Cost Metrics**
   - API calls per endpoint
   - Token usage costs
   - Overall service costs

## Troubleshooting

Common issues and solutions:

1. **Rate Limits**
   - Implement retries with backoff
   - Monitor usage patterns
   - Consider upgrading tier

2. **Token Limits**
   - Split large documents
   - Monitor token usage
   - Implement chunking

3. **API Errors**
   - Check API key validity
   - Verify endpoint URLs
   - Monitor service status
