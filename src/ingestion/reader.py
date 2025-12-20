import os
from pathlib import Path
from typing import Generator, List
from src.utils.logger import setup_logger
from .parser import LogParser, LogEntry

logger = setup_logger(__name__)

class DatasetReader:
    """
    Reads large dataset files line by line to avoid memory issues.
    """
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        self.parser = LogParser()
        if not self.file_path.exists():
            raise FileNotFoundError(f"File not found: {self.file_path}")

    def stream_entries(self) -> Generator[LogEntry, None, None]:
        """Yields parsed LogEntry objects."""
        logger.info(f"Starting to read {self.file_path}")
        try:
            with open(self.file_path, 'r', encoding='utf-8', errors='replace') as f:
                for line in f:
                    entry = self.parser.parse_line(line)
                    if entry.is_valid:
                        yield entry
        except Exception as e:
            logger.error(f"Error reading file {self.file_path}: {e}")
            raise

    def read_batch(self, batch_size: int = 1000) -> Generator[List[LogEntry], None, None]:
        """Yields batches of LogEntries."""
        batch = []
        for entry in self.stream_entries():
            batch.append(entry)
            if len(batch) >= batch_size:
                yield batch
                batch = []
        if batch:
            yield batch
