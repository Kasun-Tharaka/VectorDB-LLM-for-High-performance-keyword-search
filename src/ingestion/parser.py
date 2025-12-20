from dataclasses import dataclass
from typing import Optional
from src.utils.logger import setup_logger

logger = setup_logger(__name__)

@dataclass
class LogEntry:
    raw: str
    url: Optional[str] = None
    email: Optional[str] = None
    metadata: Optional[str] = None
    is_valid: bool = False

class LogParser:
    """
    Parses lines in the format: url:email:metadata
    """
    def parse_line(self, line: str) -> LogEntry:
        line = line.strip()
        if not line:
            return LogEntry(raw=line, is_valid=False)

        parts = line.split(":", 2) # Split into max 3 parts
        
        if len(parts) < 2:
            # Minimal expectation: url:something
            # But specific requirement usually implies strict structure. 
            # Given samples: "url:email:metadata", we try to extract what we can.
            # If only 2 parts, could be url:email or url:metadata. 
            # We will be lenient but warn.
            logger.debug(f"Line has fewer than 3 parts: {line}")
            return LogEntry(raw=line, url=parts[0], is_valid=True) # Basic validity
            
        entry = LogEntry(
            raw=line,
            url=parts[0].strip(),
            email=parts[1].strip(),
            metadata=parts[2].strip() if len(parts) > 2 else "",
            is_valid=True
        )
        return entry
