__author__ = 'nirajkumar'

cfg = {
  # Retrieval Settings
  "retrieval": {
      "model": "gpt-4o",  # Pre-trained model for embeddings
      "embedding_dimension": 768,  # Embedding vector size
      "retrieval_method": "dense",  # Method: dense (using embeddings) or sparse (keyword-based)
      "index_type": "faiss",  # Type of index (e.g., FAISS for dense retrieval)
      "top_k": 5,  # Number of top documents to retrieve
      "database": {
          "type": "elasticsearch",  # Backend (could be Elasticsearch, Pinecone, etc.)
          "host": "localhost",
          "port": 9200,
          "index_name": "documents_index",  # Name of the document index
      }
  },
  
  # Generation Settings
  "generation": {
      "model": "gpt-4o",  # Pre-trained model for generation (can also be a smaller model like GPT-3)
      "max_length": 300,  # Maximum number of tokens to generate
      "temperature": 0.7,  # Controls randomness in the generation (higher = more random)
      "top_p": 0.9,  # Controls nucleus sampling (probability mass of tokens considered)
      "beam_search": False,  # Use beam search for more deterministic output
      "stop_sequences": ["\n\n"],  # Sequences to stop generation,
      "instructions": "Generate a summary of the text.",  # Instructions for the model
  },
  
  # Chunking and Preprocessing Settings
  "chunking": {
      "chunk_size": 512,  # Size of each text chunk in tokens
      "overlap_size": 50,  # Overlap between chunks to maintain context
  },
  
  # Embedding Generation (optional if embeddings need to be precomputed)
  "embedding_model": {
      "name": "text-embedding-ada-002",  # Pre-trained embedding model
      "batch_size": 32,  # Batch size for embedding generation
  },
  
  # Storage and Indexing Settings
  "storage": {
      "type": "local",  # Type of storage (could also be "cloud" or other types)
  }
}
