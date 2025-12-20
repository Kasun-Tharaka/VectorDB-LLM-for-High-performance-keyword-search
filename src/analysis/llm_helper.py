from typing import List
from src.core.config_loader import config
from src.utils.logger import setup_logger

logger = setup_logger(__name__)

class LLMHelper:
    def __init__(self):
        self.provider = config.get("llm.provider", "mock")
        self.api_key = config.get("llm.api_key", "")
        
    def summarize_threat(self, query_url: str, neighbors: List[dict]) -> str:
        """
        Generates a summary explaining why the query_url might be malicious based on neighbors.
        """
        context = "\n".join([f"- {n['url']} (Score: {n['score']:.4f})" for n in neighbors])
        prompt = (
            f"Analyze the following URL: {query_url}\n"
            f"It is similar to these known malicious links:\n{context}\n"
            f"Provide a short summary explaining the potential threat."
        )
        
        if self.provider == "mock":
            logger.info("Generating mock LLM response.")
            return (
                f"**ANALYSIS**: The URL '{query_url}' shares significant structural similarities "
                f"with {len(neighbors)} known malicious domains. "
                "Detected common phishing patterns include similar subdomains and path structures."
            )
        
        # Here you would integrate OpenAI, Anthropic, or Local LLM
        # e.g., using `openai` library
        return "LLM Integration not fully configured for production provider."
