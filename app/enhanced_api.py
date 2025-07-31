from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from pathlib import Path
import sys

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app.kg_query_engin import KnowledgeGraph, QueryInterpreter, GraphExecutor
from app.config import DATA
from app.llm_integration import generate_llm_response, validate_llm_config

# Initialize FastAPI app
app = FastAPI(
    title="Marvel Knowledge Graph API",
    description="API for querying Marvel character relationships and generating natural language responses",
    version="1.0.0"
)

# Initialize knowledge graph components
kg = KnowledgeGraph.from_graphml(DATA / "marvel_kg.graphml")
interpreter = QueryInterpreter(kg)
executor = GraphExecutor(kg)

# Pydantic models
class QuestionRequest(BaseModel):
    question: str

class QuestionResponse(BaseModel):
    answer: str
    facts: Dict[str, Any]
    query_plan: Dict[str, Any]
    cached: bool = False

class GraphNodeResponse(BaseModel):
    node_id: str
    node_type: str
    node_name: str
    relation: str

class CharacterGraphResponse(BaseModel):
    character: str
    neighbors: List[GraphNodeResponse]


def query_knowledge_graph(question: str) -> Dict[str, Any]:
    """
    Query the knowledge graph and return facts and plan.
    """
    try:
        # Interpret the query
        plan = interpreter.interpret(question)
        
        # Execute the query
        results = executor.execute(plan)
        
        return {
            "success": True,
            "plan": plan,
            "results": results,
            "query_type": f"{plan.get('start_type', 'Unknown')} → {plan.get('target_type', 'Unknown')}"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "plan": {},
            "results": [],
            "query_type": "Unknown"
        }

@app.post("/question", response_model=QuestionResponse)
async def question_endpoint(request: QuestionRequest):
    """
    Accept a user's question, query the knowledge graph for relevant facts,
    and generate a natural language response using LLM.
    """
    
    # Query the knowledge graph
    facts = query_knowledge_graph(request.question)
    
    if not facts["success"]:
        raise HTTPException(status_code=400, detail=f"Query failed: {facts['error']}")
    
    # Generate LLM response
    answer = generate_llm_response(
        question=request.question,
        facts=facts,
        query_plan=facts["plan"]
    )
    
    return QuestionResponse(
        answer=answer,
        facts=facts,
        query_plan=facts["plan"],
        cached=False
    )

@app.get("/api/stats")
async def graph_stats():
    """Get knowledge graph statistics."""
    
    # Count nodes by type
    node_types = {}
    for node, attrs in kg.G.nodes(data=True):
        node_type = attrs.get('label', 'Unknown')
        node_types[node_type] = node_types.get(node_type, 0) + 1
    
    # Count edges by relation type
    edge_types = {}
    for _, _, attrs in kg.G.edges(data=True):
        edge_type = attrs.get('relation', 'Unknown')
        edge_types[edge_type] = edge_types.get(edge_type, 0) + 1
    
    return {
        "total_nodes": len(kg.G.nodes),
        "total_edges": len(kg.G.edges),
        "node_types": node_types,
        "edge_types": edge_types
    }

@app.get("/graph/{character}", response_model=CharacterGraphResponse)
async def character_graph(character: str):
    """
    Get a character's immediate neighbors in the graph.
    Returns all powers, genes, team affiliations, etc.
    """
    
    # Find the character node (case-insensitive and handle different dashes)
    character_node = None
    character_lower = character.lower()
    
    for node, attrs in kg.G.nodes(data=True):
        if attrs.get('label') == 'Character':
            node_name = attrs.get('name', '')
            # Handle different dash types and case
            if (node_name.lower() == character_lower or 
                node_name.lower().replace('‑', '-') == character_lower or
                node_name.lower().replace('-', '‑') == character_lower):
                character_node = node
                break
    
    if not character_node:
        raise HTTPException(status_code=404, detail=f"Character '{character}' not found")
    
    # Get all neighbors (outgoing edges)
    neighbors = []
    for _, target, data in kg.G.out_edges(character_node, data=True):
        target_attrs = kg.G.nodes[target]
        neighbors.append(GraphNodeResponse(
            node_id=target,
            node_type=target_attrs.get('label', 'Unknown'),
            node_name=target_attrs.get('name', target),
            relation=data.get('relation', 'Unknown')
        ))
    
    # Get incoming edges (for reverse relationships)
    for source, _, data in kg.G.in_edges(character_node, data=True):
        source_attrs = kg.G.nodes[source]
        neighbors.append(GraphNodeResponse(
            node_id=source,
            node_type=source_attrs.get('label', 'Unknown'),
            node_name=source_attrs.get('name', source),
            relation=f"has {data.get('relation', 'Unknown')}"
        ))
    
    return CharacterGraphResponse(
        character=character,
        neighbors=neighbors
    )

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "graph_nodes": len(kg.G.nodes),
        "graph_edges": len(kg.G.edges),
        "api_version": "1.0.0",
        "llm_configured": validate_llm_config()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 