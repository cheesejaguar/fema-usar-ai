# For Developers

This document contains more advanced information for developers who want to contribute to the project or understand its architecture in more detail.

## API Endpoints

### Authentication
All endpoints require the `X-API-Key` header with your API key.

### Document Management

#### Upload Document
```bash
POST /api/documents/upload
Content-Type: multipart/form-data

curl -X POST \
  -H "X-API-Key: your-api-key" \
  -F "file=@document.pdf" \
  http://localhost:5000/api/documents/upload
```

#### List Documents
```bash
GET /api/documents
curl -H "X-API-Key: your-api-key" http://localhost:5000/api/documents
```

#### Delete Document
```bash
DELETE /api/documents/{document_id}
curl -X DELETE -H "X-API-Key: your-api-key" http://localhost:5000/api/documents/{id}
```

### Chat Interface

#### Chat with RAG
```bash
POST /api/chat
Content-Type: application/json

{
  "message": "What is the main topic of the uploaded documents?",
  "conversation_id": "optional-conversation-id",
  "use_rag": true,
  "stream": false
}
```

#### Streaming Chat
```bash
POST /api/chat
Content-Type: application/json

{
  "message": "Explain the key concepts",
  "stream": true
}
```

#### Generate ICS 205 Plan
```bash
POST /api/ics205
Content-Type: application/json

{
  "incident": "Fire at Main St"
}
```

### Health Check
```bash
GET /api/health
curl http://localhost:5000/api/health
```

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `NEMO_API_KEY` | NVIDIA NeMo API key | Required |
| `API_KEY` | Custom API key | Required |
| `DEFAULT_MODEL` | NeMo model | nemo-llama3-8b |
| `MAX_TOKENS` | Max response tokens | 1000 |
| `TEMPERATURE` | LLM temperature | 0.7 |
| `CHUNK_SIZE` | Document chunk size | 1000 |
| `CHUNK_OVERLAP` | Chunk overlap | 200 |

### File Upload Limits
- Maximum file size: 16MB
- Supported formats: PDF, DOCX, TXT

## Architecture

```
├── app.py                 # Application factory
├── config.py             # Configuration management
├── routes/               # API route blueprints
│   ├── documents.py      # Document management
│   ├── chat.py          # Chat endpoints
│   ├── ics205.py        # ICS 205 form generation
│   └── health.py        # Health checks
├── services/            # Business logic services
│   ├── vector_store.py  # Chroma vector database
│   ├── llm_service.py   # NeMo integration
│   └── document_processor.py # Document processing
└── utils/               # Utility functions
    ├── auth.py          # Authentication
    └── validation.py    # Request validation
```

## Development

### Running Tests
```bash
python -m pytest tests/
```

### Code Formatting
```bash
black .
flake8 .
```

### Adding New Document Types
1. Extend `DocumentProcessor` in `services/document_processor.py`
2. Add file extension to `ALLOWED_EXTENSIONS` in `utils/validation.py`
3. Update requirements if new libraries are needed

## Production Considerations

1. **Security**: Change default API keys and secret keys
2. **Scaling**: Use Redis for conversation storage in production
3. **Monitoring**: Add application monitoring and logging
4. **Database**: Consider PostgreSQL for metadata storage
5. **Load Balancing**: Use nginx or similar for load balancing

```