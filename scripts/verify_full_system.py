import sys
from pathlib import Path

# Add project root to python path
project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

from src.ingestion.reader import DatasetReader
from src.analysis.search_engine import SearchEngine
from src.analysis.llm_helper import LLMHelper
from src.utils.logger import setup_logger

logger = setup_logger(__name__)

def verify_system():
    logger.info("=== Starting Full System Verification ===")
    
    # 1. Setup Data
    sample_file = project_root / "data" / "raw" / "sample_test.txt"
    if not sample_file.exists():
        logger.error("Sample file missing. Run verify_ingestion.py first.")
        return

    # 2. Initialize Components
    try:
        search_engine = SearchEngine() # In-memory index init
        llm = LLMHelper()
    except Exception as e:
        logger.error(f"Failed to initialize components: {e}")
        logger.error("Ensure 'sentence-transformers' and 'faiss-cpu' are installed.")
        return

    # 3. ETL (Ingest & Index)
    logger.info("Step 3: ETL - Ingesting data...")
    reader = DatasetReader(sample_file)
    urls = []
    for batch in reader.read_batch(batch_size=10):
        batch_urls = [e.url for e in batch if e.url]
        urls.extend(batch_urls)
    
    if urls:
        search_engine.index_data(urls)
        logger.info(f"Indexed {len(urls)} URLs.")
    else:
        logger.warning("No URLs found to index.")

    # 4. Search & Analyze
    query = "www.amazon.co.jp/ap/signin" # A known URL from the sample
    logger.info(f"Step 4: Searching for '{query}'...")
    
    try:
        distances, indices = search_engine.search(query, k=3)
        
        matches = []
        # Reconstruct matches (In real app, we'd map index -> valid data, here we just show indices)
        # But wait, we didn't store the map in SearchEngine for this simple demo!
        # Ideally VectorDB or SearchEngine should store the mapping or ID.
        # For verification, we assume indices 0, 1, 2 map to urls[0], urls[1], urls[2] if added sequentially.
        
        for i, idx in enumerate(indices):
            # Check range
            if idx < len(urls) and idx >= 0:
                match_url = urls[idx]
                matches.append({"url": match_url, "score": float(distances[i])})
                logger.info(f" Match {i+1}: {match_url} (Score: {distances[i]:.4f})")
            else:
                 logger.info(f" Match {i+1}: Index {idx} (Score: {distances[i]:.4f})")

        # 5. LLM Summary
        summary = llm.summarize_threat(query, matches)
        logger.info(f"Analysis Summary: {summary}")
        logger.info("=== Verification Complete: SUCCESS ===")
        
    except Exception as e:
        logger.error(f"Search failed: {e}")

if __name__ == "__main__":
    verify_system()
