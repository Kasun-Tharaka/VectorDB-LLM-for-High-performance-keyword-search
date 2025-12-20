import sys
from pathlib import Path
import numpy as np

# Add project root to python path
project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

from src.ingestion.reader import DatasetReader
from src.analysis.search_engine import SearchEngine
from src.core.config_loader import config
from src.utils.logger import setup_logger

logger = setup_logger(__name__)

def run_etl_pipeline(raw_file_path: str):
    logger.info("Starting ETL Pipeline...")
    
    # 1. Setup
    reader = DatasetReader(raw_file_path)
    search_engine = SearchEngine() # Creates new/empty DB
    
    # 2. Process in batches
    batch_count = 0
    total_entries = 0
    
    # Configuration
    batch_size = 100 # Small batch for demo, increase for prod
    
    for batch in reader.read_batch(batch_size=batch_size):
        urls = [entry.url for entry in batch if entry.url]
        if not urls:
            continue
            
        # 3. Embed and Index
        search_engine.index_data(urls)
        
        total_entries += len(urls)
        batch_count += 1
        logger.info(f"Processed batch {batch_count}. Total URLs: {total_entries}")

    # 4. Save Index
    index_dir = Path(config.get("paths.indexes", "data/indexes"))
    index_dir.mkdir(parents=True, exist_ok=True)
    save_path = index_dir / "main.index"
    
    search_engine.vector_db.save(save_path)
    logger.info(f"ETL Complete. Index saved to {save_path}")

if __name__ == "__main__":
    # For demo, we use the sample file created earlier
    sample_file = project_root / "data" / "raw" / "sample_test.txt"
    if sample_file.exists():
        run_etl_pipeline(str(sample_file))
    else:
        logger.error(f"Sample file not found at {sample_file}. Run verify_ingestion.py first.")
