from typing import Dict, List
from .text_extractor import TextExtractor
from .text_chunker import TextChunker
from .embedding_service import EmbeddingService
from .vector_store import VectorStore

class DocumentProcessor:
    """Orchestrates the document processing pipeline"""
    
    def __init__(self):
        self.text_extractor = TextExtractor()
        self.chunker = TextChunker(chunk_size=500, chunk_overlap=100)
        self.embedding_service = EmbeddingService()
        self.vector_store = VectorStore()
    
    def process_document(self, file_content: bytes, file_type: str, 
                        document_id: int, metadata: Dict = None) -> Dict:
        """
        Complete processing pipeline for a document
        
        Args:
            file_content: Raw file bytes
            file_type: File extension (.pdf, .docx, .txt)
            document_id: Database ID of the document
            metadata: Additional metadata to attach to chunks
            
        Returns:
            Dictionary with processing results
        """
        # Extract text
        extraction_result = self.text_extractor.extract_text(file_content, file_type)
        
        if not extraction_result["success"]:
            return {
                "success": False,
                "error": extraction_result["error"],
                "chunk_count": 0
            }
        
        extracted_text = extraction_result["text"]
        
        # Prepare metadata
        chunk_metadata = metadata or {}
        chunk_metadata.update(extraction_result.get("metadata", {}))
        
        # Chunk the text
        chunks = self.chunker.chunk_text(extracted_text, metadata=chunk_metadata)
        
        if not chunks:
            return {
                "success": False,
                "error": "No chunks generated from document",
                "chunk_count": 0
            }
        
        # Generate embeddings
        chunks_with_embeddings = self.embedding_service.embed_chunks(chunks)
        
        # Store in vector database
        self.vector_store.add_chunks(chunks_with_embeddings, document_id)
        
        return {
            "success": True,
            "chunk_count": len(chunks),
            "extraction_metadata": extraction_result.get("metadata", {})
        }
    
    def delete_document(self, document_id: int):
        """Delete all chunks for a document from vector store"""
        self.vector_store.delete_document_chunks(document_id)