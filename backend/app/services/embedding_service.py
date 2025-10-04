from sentence_transformers import SentenceTransformer
from typing import List, Dict
import numpy as np

class EmbeddingService:
    """Service for generating text embeddings"""
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Initialize embedding model
        
        Args:
            model_name: HuggingFace model name for embeddings
                       'all-MiniLM-L6-v2' is fast and good quality (384 dimensions)
        """
        print(f"Loading embedding model: {model_name}")
        self.model = SentenceTransformer(model_name)
        self.embedding_dimension = self.model.get_sentence_embedding_dimension()
        print(f"Model loaded. Embedding dimension: {self.embedding_dimension}")
    
    def embed_text(self, text: str) -> List[float]:
        """
        Generate embedding for a single text
        
        Args:
            text: Text to embed
            
        Returns:
            List of floats representing the embedding vector
        """
        if not text or not text.strip():
            # Return zero vector for empty text
            return [0.0] * self.embedding_dimension
        
        embedding = self.model.encode(text, convert_to_tensor=False)
        return embedding.tolist()
    
    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for multiple texts (more efficient)
        
        Args:
            texts: List of texts to embed
            
        Returns:
            List of embedding vectors
        """
        if not texts:
            return []
        
        # Filter out empty texts but keep track of indices
        non_empty_texts = []
        non_empty_indices = []
        
        for i, text in enumerate(texts):
            if text and text.strip():
                non_empty_texts.append(text)
                non_empty_indices.append(i)
        
        if not non_empty_texts:
            # All texts were empty, return zero vectors
            return [[0.0] * self.embedding_dimension] * len(texts)
        
        # Generate embeddings for non-empty texts
        embeddings = self.model.encode(non_empty_texts, 
                                      convert_to_tensor=False,
                                      show_progress_bar=True)
        
        # Create result list with zero vectors for empty texts
        result = []
        non_empty_idx = 0
        
        for i in range(len(texts)):
            if i in non_empty_indices:
                result.append(embeddings[non_empty_idx].tolist())
                non_empty_idx += 1
            else:
                result.append([0.0] * self.embedding_dimension)
        
        return result
    
    def embed_chunks(self, chunks: List[Dict]) -> List[Dict]:
        """
        Generate embeddings for chunks and add them to chunk dictionaries
        
        Args:
            chunks: List of chunk dictionaries with 'text' field
            
        Returns:
            List of chunks with 'embedding' field added
        """
        texts = [chunk.get("text", "") for chunk in chunks]
        embeddings = self.embed_batch(texts)
        
        # Add embeddings to chunks
        for chunk, embedding in zip(chunks, embeddings):
            chunk["embedding"] = embedding
        
        return chunks
    
    def compute_similarity(self, embedding1: List[float], embedding2: List[float]) -> float:
        """
        Compute cosine similarity between two embeddings
        
        Args:
            embedding1: First embedding vector
            embedding2: Second embedding vector
            
        Returns:
            Similarity score between -1 and 1 (higher is more similar)
        """
        vec1 = np.array(embedding1)
        vec2 = np.array(embedding2)
        
        # Cosine similarity
        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        similarity = dot_product / (norm1 * norm2)
        return float(similarity)