from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.analysis.search_engine import SearchEngine
from src.analysis.llm_helper import LLMHelper
from src.core.config_loader import config

app = FastAPI(title=config.get("app.name"), version=config.get("app.version"))

# Global instances
search_engine = None
llm_helper = None

@app.on_event("startup")
def startup_event():
    global search_engine, llm_helper
    # Initialize implementation
    # In production, we would load the existing index
    index_path = config.get("paths.indexes") + "/main.index"
    search_engine = SearchEngine(vector_db_path=index_path)
    llm_helper = LLMHelper()

class SearchRequest(BaseModel):
    url: str
    top_k: int = 5

class SearchResponse(BaseModel):
    query: str
    summary: str
    matches: list

@app.post("/search", response_model=SearchResponse)
def search_url(request: SearchRequest):
    if not search_engine:
        raise HTTPException(status_code=500, detail="Search engine not initialized")
        
    try:
        distances, indices = search_engine.search(request.url, k=request.top_k)
        
        # In a real app, we would map indices back to the raw string within the SearchEngine/VectorDB
        # For now, we return indices and distances
        matches = []
        for d, i in zip(distances, indices):
             matches.append({"index": int(i), "score": float(d), "url": f"Index_{i}"}) # Placeholder for real URL lookup
        
        summary = llm_helper.summarize_threat(request.url, matches)
        
        return SearchResponse(
            query=request.url,
            summary=summary,
            matches=matches
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health():
    return {"status": "ok"}
