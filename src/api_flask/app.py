import os
import sys

# Ensure project root is in python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from flask import Flask, request, jsonify
from src.analysis.search_engine import SearchEngine
from src.analysis.llm_helper import LLMHelper
from src.core.config_loader import config

app = Flask(__name__)

# Global instances
search_engine = None
llm_helper = None

@app.before_request
def initialize():
    global search_engine, llm_helper
    if search_engine is None:
        # Initialize implementation
        # In production, we would load the existing index
        # Using a relative path that works when running from project root or inside docker
        index_path = config.get("paths.indexes") + "/main.index"
        search_engine = SearchEngine(vector_db_path=index_path)
        llm_helper = LLMHelper()

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})

@app.route("/search", methods=["POST"])
def search_url():
    global search_engine, llm_helper
    
    if not search_engine:
         return jsonify({"error": "Search engine not initialized"}), 500

    data = request.get_json()
    if not data or "url" not in data:
        return jsonify({"error": "Missing 'url' in request body"}), 400
    
    url = data["url"]
    top_k = data.get("top_k", 5)

    try:
        distances, indices = search_engine.search(url, k=top_k)
        
        matches = []
        for d, i in zip(distances, indices):
             matches.append({"index": int(i), "score": float(d), "url": f"Index_{i}"})

        summary = llm_helper.summarize_threat(url, matches)
        
        response = {
            "query": url,
            "summary": summary,
            "matches": matches
        }
        return jsonify(response)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
