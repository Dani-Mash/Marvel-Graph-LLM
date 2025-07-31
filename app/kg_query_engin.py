"""
Knowledge Graph Query Engine for Marvel Universe

This module provides a complete knowledge graph query system that:
1. Loads Marvel character/power/gene/team data from GraphML files
2. Recognizes entities in natural language queries using spaCy
3. Determines query intent using sentence transformers
4. Executes graph traversals to find relevant information
5. Returns structured results for LLM integration

Key Components:
- KnowledgeGraph: Wrapper around NetworkX graph with typed nodes
- QueryInterpreter: Converts natural language to structured queries
- GraphExecutor: Executes traversal plans on the knowledge graph
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

import networkx as nx
from sentence_transformers import SentenceTransformer, util

# spaCy import for advanced entity recognition
try:
    import spacy
    from spacy.pipeline import EntityRuler
except ImportError:  
    spacy = None  

# Import project config with GraphML path
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

try:
    from app import config  # GRAPHML = DATA / "marvel_kg.graphml"
    GRAPHML = config.DATA / "marvel_kg.graphml"
except ImportError as exc: 
    raise SystemExit("Cannot import config.py with GRAPHML path") from exc


# ---------------------------------------------------------------------------
# Knowledge Graph Wrapper
# ---------------------------------------------------------------------------

class KnowledgeGraph:
    """
    Wrapper around NetworkX MultiDiGraph with typed nodes and labeled edges.
    
    Provides a clean interface for loading GraphML files and accessing
    Marvel Universe knowledge graph data with proper entity typing.
    """

    def __init__(self) -> None:
        """Initialize an empty directed multigraph."""
        self.G = nx.MultiDiGraph()

    @classmethod
    def from_graphml(cls, path: str | Path) -> "KnowledgeGraph":
        """
        Load a GraphML file into the KnowledgeGraph structure.
        
        Args:
            path: Path to the GraphML file containing Marvel data
            
        Returns:
            KnowledgeGraph instance with loaded data
            
        Note:
            - Converts undirected graphs to directed for consistency
            - Preserves all node attributes (name, label, type, etc.)
            - Maps edge attributes to 'relation' field for traversal
        """
        kg = cls()
        raw = nx.read_graphml(Path(path))  

        # Ensure directed graph for consistent traversal
        if not raw.is_directed():
            raw = raw.to_directed()

        # Copy all nodes with their attributes (name, label, type, etc.)
        for node_id, attrs in raw.nodes(data=True):
            kg.G.add_node(node_id, **attrs)

        # Copy edges and standardize relation attribute
        for src, dst, attrs in raw.edges(data=True):
            # Try multiple possible relation attribute names
            relation = (
                attrs.get("relation")
                or attrs.get("label")
                or attrs.get("type")
                or attrs.get("name")
                or "RELATED_TO"  # fallback
            )
            kg.G.add_edge(src, dst, relation=relation)
        return kg

    # Convenience methods for building graphs (used in tests/extensions)
    def add_character(self, name: str) -> None:
        """Add a character node to the graph."""
        self.G.add_node(name, type="Character")

    def add_team(self, name: str) -> None:
        """Add a team node to the graph."""
        self.G.add_node(name, type="Team")

    def add_gene(self, name: str) -> None:
        """Add a gene node to the graph."""
        self.G.add_node(name, type="Gene")

    def add_power(self, name: str) -> None:
        """Add a power node to the graph."""
        self.G.add_node(name, type="Power")

    def add_relationship(self, src: str, dst: str, rel: str) -> None:
        """Add a relationship edge between two nodes."""
        self.G.add_edge(src, dst, relation=rel)

    def node_type(self, node: str) -> str:
        """
        Get the type/label of a node.
        
        Returns the 'label' attribute or 'Unknown' if not found.
        This determines if a node is Character, Power, Gene, or Team.
        """
        return self.G.nodes[node].get("label", "Unknown")


# ---------------------------------------------------------------------------
# Query Interpreter
# ---------------------------------------------------------------------------

class QueryInterpreter:
    """
    Converts natural language queries into structured graph traversal plans.
    
    Uses sentence transformers for intent detection and spaCy for entity
    recognition to understand what the user is asking about.
    """

    def __init__(self, kg: KnowledgeGraph):
        """
        Initialize the query interpreter with a knowledge graph.
        
        Args:
            kg: The knowledge graph to query against
        """
        self.kg = kg

        # Load sentence transformer model for semantic similarity
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

        # Define intent templates with descriptions and relation chains
        self.intent_templates: Dict[str, tuple[str, List[str]]] = {
            "direct_power": (
                "Retrieve powers a character directly possesses",
                ["POSSESSES_POWER"],
            ),
            "mutation_power": (
                "Retrieve powers a character has via mutations",
                ["HAS_MUTATION", "CONFERS"],
            ),
            "team": (
                "Retrieve teams a character belongs to",
                ["MEMBER_OF"],
            ),
            "gene_power": (
                "Retrieve powers a gene confers",
                ["CONFERS"],
            ),
            "character_gene": (
                "Retrieve genes a character has",
                ["HAS_MUTATION"],
            ),
        }
        
        # Pre-compute embeddings for intent templates
        self.template_embeddings = {
            key: self.model.encode(text)
            for key, (text, _) in self.intent_templates.items()
        }

        # Initialize spaCy entity ruler if available
        self._nlp: Optional[Any] = None
        if spacy is not None:
            self._build_spacy_ruler()

    def _build_spacy_ruler(self) -> None:
        """
        Build a spaCy entity ruler with all graph entities.
        
        Creates patterns for every node in the knowledge graph so spaCy
        can recognize Marvel characters, powers, genes, and teams.
        """
        nlp = spacy.blank("en")  # type: ignore[arg-type]
        ruler: EntityRuler = nlp.add_pipe("entity_ruler")  # type: ignore[var-annotated]
        
        # Create patterns for all graph entities
        patterns = [
            {"label": self.kg.node_type(node), "pattern": node}
            for node in self.kg.G.nodes
        ]
        ruler.add_patterns(patterns)
        self._nlp = nlp

    def interpret(self, query: str) -> Dict[str, Any]:
        """
        Convert a natural language query into a structured traversal plan.
        
        Args:
            query: Natural language question (e.g., "What powers does Spider-Man have?")
            
        Returns:
            Dictionary with start_entity, start_type, relation_chain, and target_type
            
        Raises:
            ValueError: If no known entity is found in the query
        """
        # Step 1: Extract the main entity from the query
        start_entity = self._extract_entity(query)
        if start_entity is None:
            raise ValueError("No known entity found in query. Please clarify.")

        # Step 2: Determine intent based on entity type and query content
        entity_type = self.kg.node_type(start_entity)
        
        # Handle different entity types with appropriate relation chains
        if entity_type == "Gene":
            # Genes confer powers directly
            relation_chain = ["CONFERS"]
            intent = "gene_power"
        elif entity_type == "Power":
            # Powers are possessed by characters (reverse lookup)
            relation_chain = ["POSSESSES_POWER"]
            intent = "power_character"
        elif entity_type == "Team":
            # Teams have members (reverse lookup)
            relation_chain = ["MEMBER_OF"]
            intent = "team_character"
        elif entity_type == "Character":
            # For characters, check if query is about genes/mutations
            q_low = query.lower()
            if any(word in q_low for word in ["gene", "mutation", "mutant"]):
                relation_chain = ["HAS_MUTATION"]
                intent = "character_gene"
            else:
                # Use embedding-based intent detection for other character queries
                q_emb = self.model.encode(query)
                intent = max(
                    self.intent_templates,
                    key=lambda k: util.cos_sim(q_emb, self.template_embeddings[k]).item(),
                )
                relation_chain = self.intent_templates[intent][1]
        else:
            # For other entities, use embedding-based intent detection
            q_emb = self.model.encode(query)
            intent = max(
                self.intent_templates,
                key=lambda k: util.cos_sim(q_emb, self.template_embeddings[k]).item(),
            )
            relation_chain = self.intent_templates[intent][1]

        # Determine target type based on intent
        target_type = "Power" if intent.endswith("power") else "Team" if intent == "team" else "Gene" if intent == "character_gene" else "Character" if intent in ["power_character", "team_character"] else "Unknown"

        plan = {
            "start_entity": start_entity,
            "start_type": entity_type,
            "relation_chain": relation_chain,
            "target_type": target_type,
        }
        return plan

    def _extract_entity(self, query: str) -> Optional[str]:
        """
        Extract the main entity from a natural language query.
        
        Args:
            query: Natural language query
            
        Returns:
            Entity name if found, None otherwise
            
        Note:
            Uses spaCy entity recognition if available, falls back to
            simple string matching with case and dash normalization.
        """
        # Try spaCy entity recognition first
        if self._nlp is not None:
            doc = self._nlp(query)
            for ent in doc.ents:
                # Check if recognized entity exists in our graph
                if ent.text in self.kg.G.nodes:
                    return ent.text
        
        # Fallback to simple string matching
        q_low = query.lower()
        for node_name in self.kg.G.nodes:
            # Handle different dash types and case sensitivity
            node_lower = node_name.lower()
            if (node_lower in q_low or 
                node_lower.replace('‑', '-') in q_low or  # en dash
                node_lower.replace('-', '‑') in q_low):   # hyphen
                return node_name
        return None


# ---------------------------------------------------------------------------
# Graph Executor
# ---------------------------------------------------------------------------

class GraphExecutor:
    """
    Executes structured traversal plans on the knowledge graph.
    
    Takes the plan from QueryInterpreter and traverses the graph
    following the specified relation chains to find results.
    """

    def __init__(self, kg: KnowledgeGraph):
        """
        Initialize executor with a knowledge graph.
        
        Args:
            kg: The knowledge graph to traverse
        """
        self.G = kg.G

    def execute(self, plan: Dict[str, Any]) -> List[str]:
        """
        Execute a traversal plan on the knowledge graph.
        
        Args:
            plan: Dictionary with start_entity, start_type, and relation_chain
            
        Returns:
            List of entity names that match the traversal
            
        Note:
            Handles both forward and reverse relationships based on entity type.
            For Power and Team entities, uses incoming edges (reverse lookup).
            For other entities, uses outgoing edges (normal traversal).
        """
        nodes = [plan["start_entity"]]
        entity_type = plan.get("start_type", "")
        
        # Follow each relation in the chain
        for rel in plan["relation_chain"]:
            nxt: list[str] = []
            for n in nodes:
                if entity_type in ["Power", "Team"]:
                    # For Power and Team entities, find incoming edges (reverse relationship)
                    # This finds "who has this power" or "who belongs to this team"
                    for src, tgt, data in self.G.in_edges(n, data=True):
                        if data.get("relation") == rel:
                            nxt.append(src)
                else:
                    # For other entities, use outgoing edges (normal relationship)
                    # This finds "what powers does this character have" etc.
                    for _, tgt, data in self.G.out_edges(n, data=True):
                        if data.get("relation") == rel:
                            nxt.append(tgt)
            nodes = nxt
        return nodes


# ---------------------------------------------------------------------------
# CLI Entry Point
# ---------------------------------------------------------------------------

def main():
    """
    Command-line interface for testing the knowledge graph query engine.
    
    Usage:
        python kg_query_engin.py "What powers does Spider-Man have?"
        python kg_query_engin.py  # Interactive mode
    """
    # Load the knowledge graph
    kg = KnowledgeGraph.from_graphml(config.GRAPHML)
    interpreter = QueryInterpreter(kg)
    executor = GraphExecutor(kg)

    # Get query from command line or interactive input
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
    else:
        query = input("Enter your Marvel KG question › ")

    try:
        # Interpret and execute the query
        plan = interpreter.interpret(query)
        result = executor.execute(plan)
    except ValueError as err:
        print("Error:", err)
        sys.exit(1)

    # Display results
    print("\nQuery:", query)
    print("Plan:", plan)
    print("Result:", result)


if __name__ == "__main__":
    main()
