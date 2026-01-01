from typing import List
import numpy as np
from sentence_transformers import SentenceTransformer
from src.core.config_loader import config
from src.utils.logger import setup_logger

logger = setup_logger(__name__)

class EmbeddingModel:
    def __init__(self):
        model_name = config.get("embedding.model_name", "sentence-transformers/all-MiniLM-L6-v2")
        device = config.get("embedding.device", "cpu")
        logger.info(f"Loading embedding model: {model_name} on {device}")
        
        try:
            # loading specific model from sentence-transformers
            self.model = SentenceTransformer(model_name, device=device)
        except Exception as e:
            logger.error(f"Failed to load model {model_name}: {e}")
            raise

    def encode(self, texts: List[str]) -> np.ndarray:
        """
        Encodes a list of texts into embeddings.
        Returns a numpy array of shape (len(texts), dimension).
        """
        if not texts:
            return np.array([])
            
        try:
            # batch_size is handled by sentence-transformers internally for large lists, 
            # or we can pass it explicitly. config has batch_size.
            batch_size = config.get("embedding.batch_size", 32)
            embeddings = self.model.encode(
                texts, 
                batch_size=batch_size, 
                show_progress_bar=False, 
                convert_to_numpy=True
            )
            return embeddings
        except Exception as e:
            logger.error(f"Error during encoding: {e}")
            raise
