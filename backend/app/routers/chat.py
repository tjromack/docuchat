from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
from ..models.database import get_db
from ..models.document import Document
from ..services.embedding_service import EmbeddingService
from ..services.vector_store import VectorStore
import os

router = APIRouter(prefix="/api/chat", tags=["chat"])

# Initialize services (singleton pattern)
embedding_service = EmbeddingService()
vector_store = VectorStore()

# Request/Response models
class ChatRequest(BaseModel):
    question: str
    document_id: Optional[int] = None

    n_results: int = 5

class SourceChunk(BaseModel):
    document_id: int
    text: str
    similarity: float

class ChatResponse(BaseModel):
    answer: str
    sources: List[SourceChunk]
    question: str

@router.post("/ask", response_model=ChatResponse)
async def ask_question(request: ChatRequest, db: Session = Depends(get_db)):
    """Ask a question about uploaded documents"""
    try:
        print(f"Received question: {request.question}")
        
        if not request.question or not request.question.strip():
            raise HTTPException(status_code=400, detail="Question cannot be empty")
        
        # Generate embedding for the question
        print("Generating question embedding...")
        question_embedding = embedding_service.embed_text(request.question)
        
        # Search for relevant chunks
        print(f"Searching for relevant chunks (top {request.n_results})...")
        search_results = vector_store.search(
            query_embedding=question_embedding,
            n_results=request.n_results,
            document_id=request.document_id
        )
        
        # Check if we found any results
        if not search_results["ids"][0]:
            raise HTTPException(
                status_code=404, 
                detail="No relevant documents found. Please upload documents first."
            )
        
        print(f"Found {len(search_results['ids'][0])} relevant chunks")
        
        # Prepare context from retrieved chunks
        context_chunks = []
        sources = []
        
        for i in range(len(search_results["ids"][0])):
            chunk_text = search_results["documents"][0][i]
            doc_id = search_results["metadatas"][0][i]["document_id"]
            distance = search_results["distances"][0][i]
            similarity = 1 - distance
            
            context_chunks.append(chunk_text)
            sources.append(SourceChunk(
                document_id=doc_id,
                text=chunk_text[:200] + "..." if len(chunk_text) > 200 else chunk_text,
                similarity=round(similarity, 3)
            ))
        
        # Build context for the LLM
        context = "\n\n".join([f"[Document {i+1}]\n{chunk}" for i, chunk in enumerate(context_chunks)])
        
        print("Generating answer with OpenAI...")
        
        # Generate answer using OpenAI
        answer = await generate_answer(request.question, context)
        
        print("Answer generated successfully")
        
        return ChatResponse(
            answer=answer,
            sources=sources,
            question=request.question
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in chat endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to process question: {str(e)}")

async def generate_answer(question: str, context: str) -> str:
    """
    Generate answer using context
    NOTE: Using mock response for demo purposes
    In production, this would call OpenAI API
    """
    
    # Extract key information from context for a relevant mock response
    context_preview = context[:500] + "..." if len(context) > 500 else context
    
    mock_response = f"""Based on the retrieved documents, here's the answer to your question:

{context_preview}

---
[DEMO MODE: This is a mock response showing retrieved context. In production, this would be an AI-generated answer using OpenAI GPT-3.5/4. The RAG retrieval pipeline is fully functional - only the LLM generation is mocked for demo purposes.]"""
    
    return mock_response

@router.get("/history")
async def get_chat_history():
    """Get chat history (to be implemented with conversation storage)"""
    return {"message": "Chat history feature coming soon"}