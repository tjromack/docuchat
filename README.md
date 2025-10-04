## Project Status

**Phase 1 Complete**: Document upload and management system
- ✅ File upload with validation
- ✅ Text extraction from PDF/DOCX/TXT
- ✅ Document metadata storage
- ✅ RESTful API endpoints
- ✅ Interactive API documentation

**Phase 2 Complete**: RAG Implementation Core
- ✅ Text chunking with overlap strategy
- ✅ Vector embeddings (sentence-transformers)
- ✅ ChromaDB vector database integration
- ✅ Semantic similarity search
- ✅ Chat endpoint for Q&A
- ✅ Complete RAG pipeline (retrieve → augment → generate)
- 📝 Using mock LLM responses for demo (can integrate OpenAI/Ollama)

<<<<<<< HEAD
**Phase 3 Planned**: Frontend Interface
- 🔄 React-based chat interface
- 🔄 Document upload UI
- 🔄 Conversation history
- 🔄 Source document highlighting
=======
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
   # Edit .env with your settings
   ```

4. **Run the application**
   ```bash
   python -m app.main
   ```

5. **Access the API**
   - API Documentation: http://localhost:8000/docs
   - Health Check: http://localhost:8000/health
   - Upload documents via the interactive docs interface

## API Endpoints

### Documents
- `POST /api/documents/upload` - Upload a document
- `GET /api/documents/` - List all documents
- `GET /api/documents/{id}` - Get specific document
- `DELETE /api/documents/{id}` - Delete a document

### Health
- `GET /health` - Health check endpoint

## Project Structure

```
docuchat/
├── backend/
│   ├── app/
│   │   ├── models/          # Database models
│   │   ├── routers/         # API endpoints
│   │   ├── services/        # Business logic
│   │   └── main.py          # FastAPI application
│   ├── requirements.txt     # Python dependencies
│   └── .env                 # Environment variables
├── data/
│   ├── uploads/             # Uploaded files
│   ├── vectordb/           # Vector database storage
│   └── processed/          # Processed documents
└── README.md
```

## Configuration

Environment variables in `.env`:

```env
OPENAI_API_KEY=your_openai_api_key_here
DATABASE_URL=sqlite:///./docuchat.db
UPLOAD_FOLDER=../data/uploads
VECTOR_DB_PATH=../data/vectordb
```

## Usage Examples

### Upload a Document

```bash
curl -X POST -F "file=@document.pdf" http://localhost:8000/api/documents/upload
```

### List Documents

```bash
curl http://localhost:8000/api/documents/
```

## Development Roadmap

### Phase 2: RAG Implementation (In Progress)
- [ ] Text chunking with configurable strategies
- [ ] Vector embeddings generation
- [ ] ChromaDB integration for vector storage
- [ ] Semantic similarity search
- [ ] Chat endpoint for Q&A
- [ ] Source attribution and citations

### Phase 3: Frontend Interface
- [ ] React-based chat interface
- [ ] Document upload UI
- [ ] Conversation history
- [ ] Source document highlighting

### Phase 4: Advanced Features
- [ ] Multi-user support
- [ ] Document collections/workspaces
- [ ] Advanced search filters
- [ ] Export functionality
- [ ] Authentication system

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

Trevor Romack - tjromack@gmail.com
Project Link: https://github.com/tjromack/docuchat
>>>>>>> 51a03dc54851788a03cf1fdc000cd4b4136f094d
