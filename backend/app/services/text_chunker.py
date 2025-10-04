from typing import List, Dict
import re

class TextChunker:
    """Intelligent text chunking for RAG"""
    
    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 50):
        """
        Initialize chunker with size and overlap settings
        
        Args:
            chunk_size: Target size of each chunk in characters
            chunk_overlap: Number of characters to overlap between chunks
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
    
    def chunk_text(self, text: str, metadata: Dict = None) -> List[Dict]:
        """
        Split text into overlapping chunks
        
        Args:
            text: The text to chunk
            metadata: Optional metadata to attach to each chunk
            
        Returns:
            List of chunk dictionaries with text and metadata
        """
        if not text or not text.strip():
            return []
        
        # Clean the text
        text = self._clean_text(text)
        
        # Split into sentences first (better than arbitrary splits)
        sentences = self._split_into_sentences(text)
        
        chunks = []
        current_chunk = []
        current_length = 0
        
        for sentence in sentences:
            sentence_length = len(sentence)
            
            # If adding this sentence exceeds chunk_size, save current chunk
            if current_length + sentence_length > self.chunk_size and current_chunk:
                chunk_text = " ".join(current_chunk)
                chunks.append(self._create_chunk(chunk_text, len(chunks), metadata))
                
                # Start new chunk with overlap
                # Keep last few sentences for context
                overlap_text = " ".join(current_chunk[-2:]) if len(current_chunk) >= 2 else ""
                current_chunk = [overlap_text] if overlap_text else []
                current_length = len(overlap_text)
            
            current_chunk.append(sentence)
            current_length += sentence_length
        
        # Add the last chunk
        if current_chunk:
            chunk_text = " ".join(current_chunk)
            chunks.append(self._create_chunk(chunk_text, len(chunks), metadata))
        
        return chunks
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove page markers if present
        text = re.sub(r'--- Page \d+ ---', '', text)
        return text.strip()
    
    def _split_into_sentences(self, text: str) -> List[str]:
        """Split text into sentences"""
        # Simple sentence splitter (you could use spaCy for better results)
        sentences = re.split(r'(?<=[.!?])\s+', text)
        return [s.strip() for s in sentences if s.strip()]
    
    def _create_chunk(self, text: str, index: int, metadata: Dict = None) -> Dict:
        """Create a chunk dictionary"""
        chunk = {
            "text": text,
            "chunk_index": index,
            "char_count": len(text),
            "word_count": len(text.split())
        }
        
        if metadata:
            chunk["metadata"] = metadata
        
        return chunk
    
    def get_chunk_preview(self, chunk: Dict, max_length: int = 100) -> str:
        """Get a preview of a chunk"""
        text = chunk.get("text", "")
        if len(text) <= max_length:
            return text
        return text[:max_length] + "..."