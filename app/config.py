from pathlib import Path
from functools import lru_cache
import json, networkx as nx, os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the project root directory
project_root = Path(__file__).parent.parent
DATA = project_root / "data"
GRAPHML = DATA / "marvel_kg.graphml"

@lru_cache
def graph():
    return nx.read_graphml(GRAPHML)

with open(DATA / "text_snippets.json") as f:
    SNIPPETS = {row["character"]: row["snippet"] for row in json.load(f)}

# Cache + LLM keys
#REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL   = os.getenv("OPENAI_MODEL", "gpt-4o")
