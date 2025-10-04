# DocuChat

A document chat assistant built with Retrieval Augmented Generation (RAG) that enables natural language queries over uploaded documents.

## Overview

DocuChat allows users to upload PDF, DOCX, and TXT files, then ask questions about the content in natural language. The system uses vector embeddings and semantic search to find relevant passages and generate answers with source citations.

**Live Demo:** Upload documents and ask questions at the web interface  
**API Documentation:** Available at `/docs` endpoint when running

## Features

- Document upload with drag-and-drop support
- Automatic text extraction and intelligent chunking
- Vector-based semantic search using ChromaDB
- Real-time chat interface with source citations
- RESTful API with interactive documentation
- Responsive web interface (no build tools required)

## Architecture

```
Document Upload → Text Extraction → Chunking → Embedding → Vector Storage
                                                              ↓
User Question → Embedding → Similarity Search → Context Retrieval → Answer Generation
```

**Key Components:**
- FastAPI backend with SQLAlchemy ORM
- ChromaDB for vector storage
- sentence-transformers for embeddings (384-dimensional)
- Vanilla HTML/CSS/JS frontend

## Quick Start

**Prerequisites:** Python 3.8+

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: .\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m app.main
```

Server runs at `http://localhost:8000`

### Frontend Setup

```bash
cd frontend
python -m http.server 8080
```

Interface available at `http://localhost:8080`

### Configuration

Create `backend/.env`:

```
DATABASE_URL=sqlite:///./docuchat.db
UPLOAD_FOLDER=../data/uploads
VECTOR_DB_PATH=../data/vectordb
OPENAI_API_KEY=optional_for_real_llm_responses
```

## API Endpoints

**Documents**
- `POST /api/documents/upload` - Upload and process document
- `GET /api/documents/` - List all documents
- `GET /api/documents/{id}` - Get document details
- `DELETE /api/documents/{id}` - Delete document

**Chat**
- `POST /api/chat/ask` - Ask question about documents
  ```json
  {
    "question": "What is the vacation policy?",
    "document_id": 1,  // optional
    "n_results": 5
  }
  ```

**System**
- `GET /health` - Health check

## Project Structure

```
docuchat/
├── backend/
│   ├── app/
│   │   ├── models/              # SQLAlchemy models
│   │   ├── routers/             # API route handlers
│   │   ├── services/            # Core business logic
│   │   │   ├── text_extractor.py
│   │   │   ├── text_chunker.py
│   │   │   ├── embedding_service.py
│   │   │   ├── vector_store.py
│   │   │   └── document_processor.py
│   │   └── main.py
│   └── requirements.txt
├── frontend/
│   ├── index.html
│   ├── css/style.css
│   └── js/app.js
└── data/
    ├── uploads/                 # Original documents
    └── vectordb/                # ChromaDB storage
```

## Technical Details

**Text Processing:**
- Chunk size: 500 characters
- Chunk overlap: 100 characters
- Embedding model: all-MiniLM-L6-v2 (384 dimensions)

**Storage:**
- SQLite for document metadata
- ChromaDB for vector embeddings
- Local filesystem for uploaded files

**Current Limitations:**
- Mock LLM responses (demonstrate RAG pipeline without API costs)
- Single-user mode
- 10MB file size limit

## Development Status

**Completed:**
- Phase 1: Document management system
- Phase 2: RAG pipeline implementation
- Phase 3: Web interface

**Planned:**
- Integration with OpenAI/Anthropic APIs
- Local LLM support (Ollama)
- User authentication
- Conversation history
- Document collections

## Testing

```bash
cd backend
python test_chunking.py
python test_embeddings.py
python test_vector_store.py
```

## Contributing

Pull requests welcome. For major changes, please open an issue first to discuss the proposed changes.

## License

MIT License - see LICENSE file for details

## Contact

GitHub: https://github.com/tjromack/docuchat
Email: tjromack@gmail.com