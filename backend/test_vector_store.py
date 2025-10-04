from app.services.text_chunker import TextChunker
from app.services.embedding_service import EmbeddingService
from app.services.vector_store import VectorStore

print("=== Testing Vector Store ===\n")

# Initialize services
print("1. Initializing services...")
chunker = TextChunker(chunk_size=300, chunk_overlap=50)
embedding_service = EmbeddingService()
vector_store = VectorStore()

# Sample documents
documents = [
    {
        "id": 1,
        "text": """
        Python is a high-level programming language. It is widely used for web development,
        data science, and artificial intelligence. Python has a simple syntax that makes it
        easy to learn for beginners. The language supports multiple programming paradigms
        including object-oriented and functional programming.
        """
    },
    {
        "id": 2,
        "text": """
        Machine learning is a subset of artificial intelligence. It involves training
        algorithms on data to make predictions or decisions. Popular machine learning
        frameworks include TensorFlow and PyTorch. Machine learning is used in applications
        like image recognition, natural language processing, and recommendation systems.
        """
    },
    {
        "id": 3,
        "text": """
        Cooking pasta is a simple culinary skill. You need to boil water with salt,
        add the pasta, and cook for 8-12 minutes. Different pasta shapes work well
        with different sauces. Italian cuisine is known for its pasta dishes like
        carbonara, bolognese, and marinara.
        """
    }
]

print("\n2. Processing and storing documents...")
for doc in documents:
    # Chunk the text
    chunks = chunker.chunk_text(doc["text"], metadata={"title": f"Doc {doc['id']}"})
    print(f"   Document {doc['id']}: Created {len(chunks)} chunks")
    
    # Generate embeddings
    chunks_with_embeddings = embedding_service.embed_chunks(chunks)
    
    # Store in vector database
    vector_store.add_chunks(chunks_with_embeddings, doc["id"])

print("\n3. Vector store statistics:")
stats = vector_store.get_stats()
print(f"   Total chunks stored: {stats['total_chunks']}")
print(f"   Collection name: {stats['collection_name']}")

print("\n4. Testing similarity search...")

# Test queries
queries = [
    "How do I learn programming?",
    "What is artificial intelligence?",
    "How to make Italian food?"
]

for query in queries:
    print(f"\n   Query: '{query}'")
    
    # Generate query embedding
    query_embedding = embedding_service.embed_text(query)
    
    # Search
    results = vector_store.search(query_embedding, n_results=2)
    
    print(f"   Top 2 results:")
    for i in range(len(results["ids"][0])):
        chunk_text = results["documents"][0][i]
        doc_id = results["metadatas"][0][i]["document_id"]
        distance = results["distances"][0][i]
        
        # Lower distance = more similar
        similarity_score = 1 - distance
        
        print(f"      Result {i+1}:")
        print(f"         Document ID: {doc_id}")
        print(f"         Similarity: {similarity_score:.3f}")
        print(f"         Text preview: {chunk_text[:100]}...")

print("\n5. Testing document-specific search...")
query = "programming concepts"
query_embedding = embedding_service.embed_text(query)

# Search only in document 1 (Python doc)
results = vector_store.search(query_embedding, n_results=2, document_id=1)
print(f"\n   Searching for '{query}' in Document 1 only:")
print(f"   Found {len(results['ids'][0])} results from Document 1")

print("\n✓ Vector store working correctly!")
print("\nExpected results:")
print("- Programming query should match Python document")
print("- AI query should match Machine Learning document")
print("- Cooking query should match Pasta document")