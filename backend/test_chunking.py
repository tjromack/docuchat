from app.services.text_chunker import TextChunker

# Sample text
sample_text = """
This is a test document. It contains multiple sentences. 
We want to see how the chunking works. Each chunk should be 
around 500 characters. There should be some overlap between chunks 
for better context. This helps with retrieval quality.

Machine learning is fascinating. Natural language processing enables 
computers to understand text. RAG combines retrieval with generation. 
This creates more accurate AI responses.
"""

# Create chunker
chunker = TextChunker(chunk_size=200, chunk_overlap=50)

# Chunk the text
chunks = chunker.chunk_text(sample_text, metadata={"source": "test_doc.txt"})

# Display results
print(f"Created {len(chunks)} chunks:\n")
for i, chunk in enumerate(chunks):
    print(f"Chunk {i}:")
    print(f"  Text: {chunk['text'][:100]}...")
    print(f"  Words: {chunk['word_count']}")
    print(f"  Chars: {chunk['char_count']}\n")