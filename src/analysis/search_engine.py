import numpy as np
import faiss
from src.embedding.embedder import EmbeddingModel
from src.storage.vector_db import VectorDB
from src.utils.logger import setup_logger

logger = setup_logger(__name__)

class SearchEngine:
    def __init__(self, vector_db_path: str = None):
        self.embedder = EmbeddingModel()
        self.vector_db = VectorDB(index_path=vector_db_path)

    def index_data(self, texts: list):
        """Convenience method to embed and index a list of texts."""
        if not texts:
            return
        embeddings = self.embedder.encode(texts)
        # Normalize for cosine similarity if using IP metric
        faiss.normalize_L2(embeddings) 
        self.vector_db.add(embeddings)

    def search(self, query: str, k: int = 5):
        """
        Embeds the query and searches the vector DB.
        """
        logger.info(f"Searching for: {query}")
        query_vec = self.embedder.encode([query])
        faiss.normalize_L2(query_vec)
        
        distances, indices = self.vector_db.search(query_vec, k)
        return distances[0], indices[0]
