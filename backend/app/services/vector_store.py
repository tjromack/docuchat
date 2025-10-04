import chromadb
from chromadb.config import Settings
from typing import List, Dict, Optional
import os
from pathlib import Path

class VectorStore:
    """ChromaDB vector store for document chunks"""
    
    def __init__(self, persist_directory: str = None):
        """
        Initialize ChromaDB client
        
        Args:
            persist_directory: Directory to persist the database
        """
        if persist_directory is None:
            persist_directory = os.getenv("VECTOR_DB_PATH", "../data/vectordb")
        
        # Create directory if it doesn't exist
        Path(persist_directory).mkdir(parents=True, exist_ok=True)
        
        print(f"Initializing ChromaDB at: {persist_directory}")
        
        # Initialize ChromaDB client with persistence
        self.client = chromadb.PersistentClient(
            path=persist_directory,
            settings=Settings(
                anonymized_telemetry=False,
                allow_reset=True
            )
        )
        
        # Create or get collection
        self.collection = self.client.get_or_create_collection(
            name="document_chunks",
            metadata={"description": "Document chunks for RAG"}
        )
        
        print(f"Collection initialized. Current count: {self.collection.count()}")
    
    def add_chunks(self, chunks: List[Dict], document_id: int):
        """
        Add document chunks to the vector store
        
        Args:
            chunks: List of chunk dictionaries with 'text' and 'embedding' fields
            document_id: ID of the source document
        """
        if not chunks:
            print("No chunks to add")
            return
        
        # Prepare data for ChromaDB
        ids = []
        embeddings = []
        documents = []
        metadatas = []
        
        for i, chunk in enumerate(chunks):
            # Create unique ID
            chunk_id = f"doc_{document_id}_chunk_{i}"
            ids.append(chunk_id)
            
            # Extract embedding
            embeddings.append(chunk["embedding"])
            
            # Store the text
            documents.append(chunk["text"])
            
            # Store metadata
            metadata = {
                "document_id": document_id,
                "chunk_index": i,
                "char_count": chunk.get("char_count", len(chunk["text"])),
                "word_count": chunk.get("word_count", len(chunk["text"].split()))
            }
            
            # Add any additional metadata from chunk
            if "metadata" in chunk:
                metadata.update(chunk["metadata"])
            
            metadatas.append(metadata)
        
        # Add to ChromaDB
        self.collection.add(
            ids=ids,
            embeddings=embeddings,
            documents=documents,
            metadatas=metadatas
        )
        
        print(f"Added {len(chunks)} chunks for document {document_id}")
        print(f"Total chunks in collection: {self.collection.count()}")
    
    def search(self, query_embedding: List[float], n_results: int = 5, 
               document_id: Optional[int] = None) -> Dict:
        """
        Search for similar chunks
        
        Args:
            query_embedding: Embedding vector of the query
            n_results: Number of results to return
            document_id: Optional - filter by specific document
            
        Returns:
            Dictionary with ids, documents, metadatas, and distances
        """
        where_filter = None
        if document_id is not None:
            where_filter = {"document_id": document_id}
        
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            where=where_filter
        )
        
        return results
    
    def delete_document_chunks(self, document_id: int):
        """
        Delete all chunks for a specific document
        
        Args:
            document_id: ID of the document to delete
        """
        # Get all chunk IDs for this document
        results = self.collection.get(
            where={"document_id": document_id}
        )
        
        if results["ids"]:
            self.collection.delete(ids=results["ids"])
            print(f"Deleted {len(results['ids'])} chunks for document {document_id}")
        else:
            print(f"No chunks found for document {document_id}")
    
    def get_stats(self) -> Dict:
        """Get statistics about the vector store"""
        count = self.collection.count()
        
        # Get sample to understand data
        if count > 0:
            sample = self.collection.get(limit=1)
            sample_metadata = sample["metadatas"][0] if sample["metadatas"] else {}
        else:
            sample_metadata = {}
        
        return {
            "total_chunks": count,
            "collection_name": self.collection.name,
            "sample_metadata_keys": list(sample_metadata.keys())
        }
    
    def reset(self):
        """Delete all data from the collection (use with caution!)"""
        print("Resetting vector store...")
        self.client.delete_collection("document_chunks")
        self.collection = self.client.get_or_create_collection(
            name="document_chunks",
            metadata={"description": "Document chunks for RAG"}
        )
        print("Vector store reset complete")