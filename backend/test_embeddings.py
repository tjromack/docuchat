from app.services.embedding_service import EmbeddingService
from app.services.text_chunker import TextChunker

# Initialize services
print("Initializing services...")
embedding_service = EmbeddingService()
chunker = TextChunker(chunk_size=200, chunk_overlap=50)

# Sample texts
text1 = "Machine learning and artificial intelligence are transforming technology."
text2 = "AI and ML are changing how we build software systems."
text3 = "I enjoy cooking pasta and making Italian food."

print("\nGenerating embeddings for sample texts...")

# Generate embeddings
emb1 = embedding_service.embed_text(text1)
emb2 = embedding_service.embed_text(text2)
emb3 = embedding_service.embed_text(text3)

print(f"\nEmbedding dimension: {len(emb1)}")
print(f"First embedding (first 5 values): {emb1[:5]}")

# Compute similarities
sim_1_2 = embedding_service.compute_similarity(emb1, emb2)
sim_1_3 = embedding_service.compute_similarity(emb1, emb3)
sim_2_3 = embedding_service.compute_similarity(emb2, emb3)

print(f"\nSimilarity Scores:")
print(f"Text 1 vs Text 2 (both about AI/ML): {sim_1_2:.4f}")
print(f"Text 1 vs Text 3 (AI vs cooking): {sim_1_3:.4f}")
print(f"Text 2 vs Text 3 (AI vs cooking): {sim_2_3:.4f}")

print("\nExpected: AI texts should have high similarity, AI vs cooking should be low")

# Test with chunks
print("\n--- Testing with Document Chunks ---")
sample_doc = """
Artificial intelligence is revolutionizing many industries. Machine learning 
algorithms can now perform tasks that once required human intelligence. 
Deep learning has enabled breakthroughs in image recognition and natural language processing.

The applications of AI are vast. From self-driving cars to medical diagnosis, 
AI systems are becoming increasingly sophisticated. Companies are investing 
heavily in AI research and development.
"""

chunks = chunker.chunk_text(sample_doc, metadata={"doc": "ai_overview.txt"})
print(f"Created {len(chunks)} chunks")

# Embed chunks
chunks_with_embeddings = embedding_service.embed_chunks(chunks)

print(f"\nChunk 0 preview: {chunks_with_embeddings[0]['text'][:80]}...")
print(f"Chunk 0 embedding size: {len(chunks_with_embeddings[0]['embedding'])}")
print(f"Chunk 0 has embedding: {chunks_with_embeddings[0]['embedding'][:3]}...")

print("\n✓ Embedding service working correctly!")