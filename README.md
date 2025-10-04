<<<<<<< HEAD
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
=======
```markdown
# DocuChat - Document Chat Assistant with RAG

A production-ready document chat assistant that allows users to upload documents and ask questions about their content using Retrieval Augmented Generation (RAG).

## Project Status

**Phase 1 Complete**: Document upload and management system ✅
- ✅ File upload with validation
- ✅ Text extraction from PDF/DOCX/TXT
- ✅ Document metadata storage
- ✅ RESTful API endpoints
- ✅ Interactive API documentation

**Phase 2 Complete**: RAG Implementation Core ✅
- ✅ Text chunking with configurable overlap strategy
- ✅ Vector embeddings (sentence-transformers)
- ✅ ChromaDB vector database integration
- ✅ Semantic similarity search
- ✅ Chat endpoint for Q&A
- ✅ Complete RAG pipeline (retrieve → augment → generate)
- ✅ Source attribution with similarity scores
- 📝 Mock LLM responses for demo (OpenAI integration ready)

**Phase 3 Complete**: Frontend Interface ✅
- ✅ Modern, responsive web interface
- ✅ Document upload with drag-and-drop
- ✅ Real-time chat with message history
- ✅ Source citation display
- ✅ Mobile-friendly design
- ✅ Loading states and notifications
- ✅ Production-ready UI/UX

## Features

- **Multi-format Document Support**: PDF, DOCX, and TXT files
- **Intelligent Text Processing**: Automatic chunking with semantic overlap
- **Vector Search**: Fast similarity search using ChromaDB
- **Source Citations**: Every answer includes source documents with similarity scores
- **Clean UI**: Modern, responsive interface built with vanilla HTML/CSS/JS
- **RESTful API**: FastAPI-based backend with automatic documentation
- **Demo Mode**: Fully functional RAG retrieval with mock LLM responses

## Tech Stack

**Backend:**
- Python 3.8+
- FastAPI - Modern web framework
- SQLAlchemy - Database ORM
- ChromaDB - Vector database
- sentence-transformers - Text embeddings
- PyPDF2, python-docx - Document processing

**Frontend:**
- HTML5/CSS3/JavaScript (Vanilla)
- No build tools required
- Responsive design
>>>>>>> f4fb9425701a8622540eb58b6cec7d1eb390392e

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

<<<<<<< HEAD
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
=======
3. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your settings (optional: add OpenAI API key for real LLM responses)
   ```

4. **Run the backend**
   ```bash
   python -m app.main
   ```
   Backend will be available at http://localhost:8000

5. **Run the frontend (new terminal)**
   ```bash
   cd frontend
   python -m http.server 8080
   ```
   Frontend will be available at http://localhost:8080

## Usage

1. **Upload Documents**: Click "+ Upload" or drag and drop PDF, DOCX, or TXT files
2. **Wait for Processing**: Documents are automatically chunked and vectorized
3. **Ask Questions**: Type questions in natural language about your documents
4. **View Sources**: See which document chunks were used to generate the answer

## API Endpoints

### Documents
- `POST /api/documents/upload` - Upload and process a document
- `GET /api/documents/` - List all documents
- `GET /api/documents/{id}` - Get specific document details
- `DELETE /api/documents/{id}` - Delete a document

### Chat
- `POST /api/chat/ask` - Ask a question about documents
  - Request body: `{"question": "string", "document_id": int (optional), "n_results": 5}`
  - Returns answer with source citations

### Health
- `GET /health` - Health check endpoint
>>>>>>> f4fb9425701a8622540eb58b6cec7d1eb390392e

## Project Structure

```
docuchat/
├── backend/
│   ├── app/
<<<<<<< HEAD
│   │   ├── models/              # SQLAlchemy models
│   │   ├── routers/             # API route handlers
│   │   ├── services/            # Core business logic
=======
│   │   ├── models/          # Database models
│   │   ├── routers/         # API endpoints
│   │   │   ├── documents.py
│   │   │   └── chat.py
│   │   ├── services/        # Business logic
>>>>>>> f4fb9425701a8622540eb58b6cec7d1eb390392e
│   │   │   ├── text_extractor.py
│   │   │   ├── text_chunker.py
│   │   │   ├── embedding_service.py
│   │   │   ├── vector_store.py
│   │   │   └── document_processor.py
<<<<<<< HEAD
│   │   └── main.py
│   └── requirements.txt
├── frontend/
│   ├── index.html
│   ├── css/style.css
│   └── js/app.js
└── data/
    ├── uploads/                 # Original documents
    └── vectordb/                # ChromaDB storage
=======
│   │   └── main.py          # FastAPI application
│   ├── requirements.txt
│   └── .env
├── frontend/
│   ├── index.html
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── app.js
├── data/
│   ├── uploads/             # Uploaded files
│   ├── vectordb/           # ChromaDB storage
│   └── processed/          # Processed documents
└── README.md
>>>>>>> f4fb9425701a8622540eb58b6cec7d1eb390392e
```

## Technical Details

**Text Processing:**
- Chunk size: 500 characters
- Chunk overlap: 100 characters
- Embedding model: all-MiniLM-L6-v2 (384 dimensions)

<<<<<<< HEAD
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
=======
```env
OPENAI_API_KEY=your_openai_api_key_here (optional - for real LLM responses)
DATABASE_URL=sqlite:///./docuchat.db
UPLOAD_FOLDER=../data/uploads
VECTOR_DB_PATH=../data/vectordb
```

**Note**: The application works without an OpenAI API key using mock responses that demonstrate the RAG retrieval pipeline. Add an API key to get AI-generated answers.

## Architecture
>>>>>>> f4fb9425701a8622540eb58b6cec7d1eb390392e

**RAG Pipeline Flow:**
1. **Document Upload** → Text extraction → Chunking (500 chars, 100 overlap)
2. **Embedding** → sentence-transformers generates 384-dim vectors
3. **Storage** → Chunks and embeddings stored in ChromaDB
4. **Query** → User question → Embedding → Similarity search
5. **Retrieval** → Top 5 relevant chunks retrieved
6. **Generation** → Context + Question → LLM → Answer with sources

## Development

### Run Tests
```bash
cd backend
python test_chunking.py
python test_embeddings.py
python test_vector_store.py
```

<<<<<<< HEAD
=======
### Access API Documentation
Visit http://localhost:8000/docs for interactive API documentation

## Future Enhancements

- Real OpenAI/Anthropic LLM integration (currently using mock responses)
- Local LLM support with Ollama
- Multi-user authentication
- Document collections/workspaces
- Conversation history persistence
- Advanced filtering and search
- Export conversation transcripts
- Support for more file formats (markdown, CSV, etc.)

>>>>>>> f4fb9425701a8622540eb58b6cec7d1eb390392e
## Contributing

Pull requests welcome. For major changes, please open an issue first to discuss the proposed changes.

## License

<<<<<<< HEAD
MIT License - see LICENSE file for details

## Contact

GitHub: https://github.com/tjromack/docuchat
Email: tjromack@gmail.com
=======
This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

Project Link: https://github.com/tjromack/docuchat

## Acknowledgments

Built as a learning project to demonstrate:
- Retrieval Augmented Generation (RAG) architecture
- Vector database integration
- Modern web development practices
- Clean API design
- Production-ready code structure
```
>>>>>>> f4fb9425701a8622540eb58b6cec7d1eb390392e
