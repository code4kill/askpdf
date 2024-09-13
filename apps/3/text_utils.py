import numpy as np
import faiss
from PyPDF2 import PdfReader
from nltk import sent_tokenize
from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity
import nltk

# Ensure required NLTK resources are downloaded
nltk.download('punkt')

def text_extractions(file):
    """
    Read the PDF file and extract text from each page.
    
    :param file: Path to the PDF file.
    :return: Dictionary containing text content, number of pages, and metadata.
    """
    try:
        docs_string = ""
        reader = PdfReader(file)
        metadata = reader.metadata
        pages_length = len(reader.pages)
        
        print(f"Metadata of PDF: {metadata}\n")
        print(f"Number of pages in PDF: {pages_length}")

        for page in reader.pages:
            text = page.extract_text()
            if text:
                docs_string += text + "\n\n"
            else:
                print(f"Warning: No text extracted from page {reader.pages.index(page)}")

        return {'text': docs_string, 'pages': pages_length, 'metadata': metadata}
    
    except FileNotFoundError:
        print("Error: The file was not found.")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

class QueryBuilder:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        """
        Initialize QueryBuilder with a pre-trained model.
        
        :param model_name: Name of the SentenceTransformer model to use.
        """
        self.model_name = model_name
        self.cluster_size = 10
        self.chunks_with_text = []
        self.chunk_embeddings = np.array([])
        self.model = SentenceTransformer(self.model_name)
        self.index = None
    
    def create_chunk(self, text, no_of_clusters):
        """
        Create thematic chunks from the provided text using KMeans clustering.
        
        :param text: Text to be chunked.
        :param no_of_clusters: Number of clusters for KMeans.
        """
        self.cluster_size = no_of_clusters
        sentences = sent_tokenize(text)
        if not sentences:
            print("No sentences found in the provided text.")
            return
        
        try:
            sentence_embeddings = self.model.encode(sentences)
            kmeans = KMeans(n_clusters=self.cluster_size, random_state=0).fit(sentence_embeddings)
            clustered_sentences = {i: [] for i in range(self.cluster_size)}

            for i, label in enumerate(kmeans.labels_):
                clustered_sentences[label].append(sentences[i])

            thematic_chunks = [' '.join(clustered_sentences[i]) for i in range(self.cluster_size)]
            self.chunks_with_text = [{'chunk': chunk, 'text': ' '.join([s for s in sentences if s in chunk])} for chunk in thematic_chunks]
            self.chunk_embeddings = self.model.encode([chunk['chunk'] for chunk in self.chunks_with_text])

            # Initialize FAISS index
            dimension = self.chunk_embeddings.shape[1]
            self.index = faiss.IndexFlatL2(dimension)
            self.index.add(self.chunk_embeddings)
        
        except Exception as e:
            print(f"An error occurred during chunking: {e}")
    
    def get_answer(self, question):
        """
        Retrieve the most relevant chunk for the given question.
        
        :param question: User's question or query.
        :return: Most relevant chunk and its associated text.
        """
        _query = sent_tokenize(question)
        if not _query:
            print("No valid query found.")
            return None

        try:
            query_embedding = self.model.encode(_query)
            # Perform search using FAISS
            distances, indices = self.index.search(query_embedding, k=1)  # Find the top 1 result
            most_similar_idx = indices[0][0]  # Index of the most similar chunk

            if distances[0][0] == float('inf'):  # Check if similarity is infinite (meaning no results found)
                print("No similarity found.")
                return None
            
            most_relevant_chunk = self.chunks_with_text[most_similar_idx]
            return most_relevant_chunk
        
        except Exception as e:
            print(f"An error occurred during query processing: {e}")
            return None
