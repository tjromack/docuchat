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

## Quick Start

### Prerequisites

- Python 3.8+
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/tjromack/docuchat.git
   cd docuchat
   ```

2. **Set up the backend**
   ```bash
   cd backend
   python -m venv venv
   
   # Windows
   .\venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   
   pip install -r requirements.txt
   ```

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

## Project Structure

```
docuchat/
├── backend/
│   ├── app/
│   │   ├── models/          # Database models
│   │   ├── routers/         # API endpoints
│   │   │   ├── documents.py
│   │   │   └── chat.py
│   │   ├── services/        # Business logic
│   │   │   ├── text_extractor.py
│   │   │   ├── text_chunker.py
│   │   │   ├── embedding_service.py
│   │   │   ├── vector_store.py
│   │   │   └── document_processor.py
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
```

## Configuration

Environment variables in `.env`:

```env
OPENAI_API_KEY=your_openai_api_key_here (optional - for real LLM responses)
DATABASE_URL=sqlite:///./docuchat.db
UPLOAD_FOLDER=../data/uploads
VECTOR_DB_PATH=../data/vectordb
```

**Note**: The application works without an OpenAI API key using mock responses that demonstrate the RAG retrieval pipeline. Add an API key to get AI-generated answers.

## Architecture

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

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

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
