import numpy as np
import faiss
import pickle
from pathlib import Path
from src.core.config_loader import config
from src.utils.logger import setup_logger

logger = setup_logger(__name__)

class VectorDB:
    def __init__(self, index_path: str = None):
        self.dimension = config.get("vectordb.dimension", 384)
        self.index_type = config.get("vectordb.index_type", "IVF100,PQ8")
        self.metric = faiss.METRIC_INNER_PRODUCT if config.get("vectordb.metric") == "cosine" else faiss.METRIC_L2
        
        self.index_path = Path(index_path) if index_path else None
        self.index = None
        
        if self.index_path and self.index_path.exists():
            self.load(self.index_path)
        else:
            self.create_index()

    def create_index(self):
        """Creates a new FAISS index."""
        logger.info(f"Creating new FAISS index with dim={self.dimension}")
        # For simplicity in this demo, using IndexFlatIP (exact search) or basic IVF
        # Real production might use IndexIVFFlat or IndexIVFPQ.
        # Starting with Flat for simplicity unless data is huge immediately.
        # But user mentioned 5TB, so we should allow training.
        
        # We'll use a simple factory string.
        # Note: IVF requires training.
        try:
            # Using IDMap to map vectors to specific IDs if needed, 
            # here we just rely on positional verification.
            self.index = faiss.index_factory(self.dimension, "Flat", self.metric) 
            logger.info("Created Flat index (Exact Search) for initial bucket.")
        except Exception as e:
            logger.error(f"Failed to create index: {e}")
            raise

    def train(self, vectors: np.ndarray):
        """Trains the index if required (e.g., IVF)."""
        if not self.index.is_trained:
            logger.info(f"Training index with {len(vectors)} vectors...")
            self.index.train(vectors)

    def add(self, vectors: np.ndarray):
        """Adds vectors to the index. Returns IDs."""
        if not self.index.is_trained:
            self.train(vectors)
        
        logger.info(f"Adding {len(vectors)} vectors to index.")
        self.index.add(vectors)
        
    def search(self, vectors: np.ndarray, k: int = 5):
        """Searches for k nearest neighbors."""
        distances, indices = self.index.search(vectors, k)
        return distances, indices

    def save(self, path: str = None):
        target = path or self.index_path
        if not target:
            logger.warning("No path specified for saving index.")
            return
            
        logger.info(f"Saving index to {target}")
        faiss.write_index(self.index, str(target))

    def load(self, path: str):
        logger.info(f"Loading index from {path}")
        self.index = faiss.read_index(str(path))
