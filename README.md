# 🦸‍♂️ Marvel Knowledge Graph API

A comprehensive knowledge graph system that combines Marvel Universe data with AI-powered natural language querying. This project demonstrates how to build a knowledge graph, integrate it with LLM responses, and provide a beautiful web interface for exploration.

## 🎯 Project Overview

This system allows users to ask natural language questions about Marvel characters, their powers, genes, and team affiliations, receiving AI-generated responses grounded in knowledge graph data.

### **Key Features:**
- **Knowledge Graph**: NetworkX-based graph with Marvel characters, powers, genes, and teams
- **Natural Language Processing**: spaCy and Sentence Transformers for entity recognition
- **LLM Integration**: OpenAI-powered responses with character context
- **Web Interface**: Beautiful Streamlit demo for interactive exploration
- **RESTful API**: FastAPI endpoints for programmatic access

## 📊 Graph Schema

### **Entities:**
- **Character**: Marvel superheroes and villains (e.g., Spider-Man, Wolverine)
- **Power**: Superhuman abilities (e.g., Enhanced Strength, Wall-Crawling)
- **Gene**: Genetic mutations that confer powers (e.g., Regenerative Mutation)
- **Team**: Superhero teams and organizations (e.g., X-Men, Avengers)

### **Relationships:**
- **POSSESSES_POWER**: Character → Power (e.g., Spider-Man → Wall-Crawling)
- **HAS_MUTATION**: Character → Gene (e.g., Wolverine → Regenerative Mutation)
- **CONFERS**: Gene → Power (e.g., Regenerative Mutation → Accelerated Healing)
- **MEMBER_OF**: Character → Team (e.g., Wolverine → X-Men)

### **Graph Structure:**
```
Character ──POSSESSES_POWER──→ Power
    │                              ↑
    │                              │
HAS_MUTATION                 CONFERS
    │                              │
    └──→ Gene ────────────────────┘
    │
MEMBER_OF
    │
    └──→ Team
```

## 🚀 Quick Start

### **Prerequisites:**
- Python 3.12
- OpenAI API key
- Virtual environment (recommended)

### **1. Clone and Setup:**
```bash
git clone <repository-url>
cd marvel-graph-llm
python -m venv venv
source venv/bin/activate  
pip install -r requirements.txt
```

### **2. Environment Configuration:**
Create a `.env` file in the root directory:
```bash
OPENAI_API_KEY=your-openai-api-key-here
OPENAI_MODEL=gpt-4o
```

### **3. Start the API:**
```bash
uvicorn app.enhanced_api:app --host 0.0.0.0 --port 8000
```

### **4. Run the Web Demo:**
```bash
streamlit run app/streamlit_demo.py
```

### **5. Access the Application:**
- **API Documentation**: http://localhost:8000/docs
- **Web Demo**: http://localhost:8501
- **Health Check**: http://localhost:8000/health

## 📚 API Endpoints

### **Core Endpoints:**
- `GET /health` - API health check
- `GET /graph/{character}` - Character's immediate neighbors
- `POST /question` - Natural language question answering

### **Example API Usage:**
```bash
# Ask a question
curl -X POST "http://localhost:8000/question" \
  -H "Content-Type: application/json" \
  -d '{"question": "What powers does Spider-Man have?"}'

# Get character graph
curl -X GET "http://localhost:8000/graph/Spider-Man"

# Check health
curl -X GET "http://localhost:8000/health"
```

## 🎥 UI Demo Video

Watch the Streamlit web application in action, demonstrating the two main API endpoints:

### **Demo Features:**
- **POST /question** - Natural language question answering with AI-powered responses
- **GET /graph/{character}** - Interactive character relationship visualization

### **Demo Video:**
🎥 **UI Demo Video** - *Coming Soon*

*The demo video will be available in the repository releases, showing the Streamlit web application in action with both API endpoints.*

**Note**: The demo video file is available locally in the `assets/` folder as `ui-demo.mov` and will be uploaded to GitHub Releases for easy access.

### **What You'll See in the Demo:**
- **Interactive Question Interface**: Ask natural language questions about Marvel characters
- **AI-Powered Responses**: Get detailed, grounded answers about powers, teams, and relationships
- **Graph Visualization**: See character relationships and connections in real-time
- **API Integration**: Watch the seamless connection between the web interface and backend API

## 🧪 Sample Queries & Responses

See [`docs/sample_queries.md`](docs/sample_queries.md) for detailed, grounded query/response examples and LLM grounding explanations.

## 🧠 Technical Architecture

See [`docs/technical_architecture.md`](docs/technical_architecture.md) for a comprehensive explanation of how the knowledge graph data is combined with the LLM, including prompt engineering, query logic, entity extraction evolution, and technology choices.

### **Example 1: Character Powers**
**Query:** "What powers does Spider-Man have?"

**Knowledge Graph Data:**
- Entity: Spider-Man (Character)
- Relationships: POSSESSES_POWER → Superhuman Agility, Enhanced Strength
- Character Background: Peter Parker, bitten by radioactive spider

**LLM Response:**
```
Spider-Man, whose real name is Peter Parker, possesses a range of powers that he gained after being bitten by a radioactive spider. These powers include:

1. **Wall-Crawling**: Spider-Man has the ability to adhere to walls and ceilings, allowing him to climb and move across surfaces with ease, much like a spider.

2. **Spider-Sense**: This is a heightened sense that alerts him to danger, providing him with a form of precognitive awareness that helps him avoid harm.

3. **Superhuman Agility**: Spider-Man exhibits agility far beyond that of a normal human, enabling him to perform acrobatic feats and maneuvers with incredible precision and speed.

4. **Enhanced Strength**: The bite also granted him superhuman strength, allowing him to lift heavy objects, overpower foes, and perform feats of strength beyond the capabilities of an ordinary person.

Guided by the mantra "With great power comes great responsibility," Spider-Man uses these abilities to protect New York City, combining his powers with his intelligence, wit, and scientific knowledge to combat crime and injustice.
```

### **Example 2: Team Membership**
**Query:** "What characters belong to X-Men?"

**Knowledge Graph Data:**
- Entity: X-Men (Team)
- Relationships: MEMBER_OF (reverse) → Wolverine, Cyclops, Jean Grey, Storm
- Character Backgrounds: Individual character snippets included

**LLM Response:**
```
The X-Men team includes several prominent mutant superheroes, each with unique abilities and backgrounds:

**Wolverine** (Logan): A fierce warrior with regenerative healing abilities, enhanced senses, and retractable adamantium claws. His healing factor allows him to recover from almost any injury, making him nearly immortal.

**Cyclops** (Scott Summers): The team's tactical leader who can project powerful optic blasts from his eyes. His ability to control these energy beams makes him one of the team's most powerful members.

**Jean Grey**: A powerful telepath and telekinetic who can read minds and move objects with her thoughts. Her psychic abilities make her one of the most versatile members of the team.

**Storm** (Ororo Munroe): A weather-controlling mutant who can manipulate atmospheric conditions. Her ability to control wind, rain, lightning, and other weather phenomena makes her incredibly powerful.

These mutants work together under Professor Xavier's guidance to protect both mutant and human kind, using their unique abilities to combat threats and promote peaceful coexistence between humans and mutants.
```

### **Example 3: Gene Analysis**
**Query:** "What powers does Regenerative Mutation confer?"

**Knowledge Graph Data:**
- Entity: Regenerative Mutation (Gene)
- Relationships: CONFERS → Accelerated Healing, Enhanced Senses
- Target Type: Power

**LLM Response:**
```
The Regenerative Mutation gene confers several powerful abilities that enhance the body's natural healing and sensory capabilities:

**Accelerated Healing**: This ability allows the body to repair damage at an incredibly rapid rate. Cuts, bruises, and even severe injuries can heal within minutes or hours rather than days or weeks. This makes the individual highly resistant to injury and able to recover from wounds that would be fatal to normal humans.

**Enhanced Senses**: The mutation also heightens all sensory perceptions, including sight, hearing, smell, taste, and touch. This provides superior awareness of the environment, allowing the individual to detect threats, track targets, and navigate complex situations with heightened precision.

These abilities are particularly valuable for individuals who engage in dangerous activities or combat situations, as they provide both protection and enhanced situational awareness. The combination of rapid healing and enhanced senses makes someone with this mutation incredibly resilient and perceptive.
```

## 🔧 Technical Architecture

### **Knowledge Graph Engine:**
- **NetworkX**: Graph data structure and traversal algorithms
- **Entity Recognition**: spaCy for advanced NLP and entity extraction
- **Intent Detection**: Sentence Transformers for semantic similarity
- **Query Planning**: Dynamic query interpretation based on entity types

### **LLM Integration:**
- **OpenAI API**: GPT-4o for natural language generation
- **Context Building**: Structured prompts with graph facts and character snippets
- **Response Grounding**: Facts from knowledge graph used to verify and enhance responses
- **Character Context**: Rich character backgrounds included in prompts (from data/text_snippets.json)

### **API Framework:**
- **FastAPI**: Modern, fast web framework for APIs
- **Pydantic**: Data validation and serialization
- **Uvicorn**: ASGI server for production deployment
- **Streamlit**: Interactive web interface for demos

## 🎯 Prompt Engineering

### **System Prompt:**
```
You are a Marvel Universe expert and S.H.I.E.L.D. analyst. 
Your task is to provide accurate, informative answers about Marvel characters, their powers, genes, and team affiliations.

Use ONLY the provided context and facts. Be factual and precise. If the context doesn't contain enough information, say so.
Always cite specific characters, powers, genes, or teams mentioned in the context.

When character backgrounds are provided, use them to add rich context and storytelling to your responses.
Incorporate the character's history, personality, and background into your explanations to make them more engaging and informative.

Format your response in a clear, informative way that directly answers the user's question.
```

### **Context Building:**
1. **Entity Information**: Start entity and type
2. **Character Snippets**: Rich background information
3. **Relationship Chain**: How the query was processed
4. **Graph Results**: Facts from knowledge graph traversal
5. **Result Context**: Additional character details for results

### **Query Logic:**
- **Entity Extraction**: Identify characters, powers, genes, or teams
- **Intent Detection**: Determine query type using semantic similarity
- **Graph Traversal**: Execute appropriate relationship chains
- **Response Generation**: Combine facts with LLM for grounded answers

## 📊 Jupyter Notebooks

### **1. Graph Visualization & Analysis** (`notebooks/exploratory_graph.ipynb`)

This notebook provides comprehensive visualization and analysis of the Marvel Knowledge Graph:

#### **Features:**
- **Graph Visualization**: Complete network diagram with color-coded nodes
  - 🔵 **Blue**: Characters (Spider-Man, Wolverine, etc.)
  - 🟢 **Green**: Teams (X-Men, Avengers, etc.)
  - 🟠 **Orange**: Genes (Regenerative Mutation, etc.)
  - 🟣 **Violet**: Powers (Enhanced Strength, Wall-Crawling, etc.)
- **Entity Definitions**: Clear explanation of what each entity type represents
- **Relationship Schema**: Visual representation of all relationship types
- **Graph Statistics**: Comprehensive analysis including:
  - Node distribution by type
  - Edge distribution by relationship
  - Network metrics (density, connectivity)
  - Top performers analysis

#### **What You'll See:**
- **Complete Graph Visualization**: All 34 nodes and 48 edges with proper layout
- **Entity Relationships**: Clear arrows showing POSSESSES_POWER, HAS_MUTATION, CONFERS, MEMBER_OF
- **Color-Coded Nodes**: Easy identification of entity types
- **Edge Labels**: Red text showing relationship types
- **Statistical Analysis**: Detailed breakdown of graph structure

### **2. Knowledge Graph Query Engine Testing** (`notebooks/test_kg_query_engine.ipynb`)

This notebook demonstrates the knowledge graph query engine with comprehensive testing:

#### **Features:**
- **Query Engine Testing**: Test the `kg_query_engin.py` with various query types
- **Entity Recognition**: Test how the system identifies different entity types
- **Intent Detection**: Verify query intent classification
- **Graph Traversal**: Test relationship chain execution
- **Response Generation**: Validate LLM integration with graph facts

#### **Test Examples:**
```python
# Character → Power queries
"What powers does Spider-Man have?"
# Character → Gene queries  
"Which mutation does Wolverine have?"
# Gene → Power queries
"What powers does Regenerative Mutation confer?"
# Team → Character queries
"Who belongs to X-Men?"
# Power → Character queries
"Which characters possess Wall-Crawling?"
```

## 📊 Data Generation

### **Knowledge Graph Data Creation** (`src/generate_data.py`)

Creates the complete Marvel Knowledge Graph dataset from a single source of truth.

#### **Generated Files:**
```
data/
├── characters.csv, teams.csv, genes.csv, powers.csv     # Entities
├── char_team.csv, char_gene.csv, gene_power.csv, char_power.csv  # Relationships
├── text_snippets.json                                   # Character backgrounds
└── marvel_kg.graphml                                    # Complete knowledge graph
```

#### **Main Output Files:**

**`data/text_snippets.json`** - Character background descriptions for LLM context:
```json
[
  {
    "character": "Wolverine",
    "snippet": "Born as James Howlett in 19th‑century Canada, Wolverine endured Weapon X experiments that bonded adamantium to his skeleton. His healing factor, heightened senses, and combat mastery make him the X‑Men's fiercest defender."
  },
  // ... 8 more characters
]
```

**`data/marvel_kg.graphml`** - Complete knowledge graph with 34 nodes and 48 edges:
- **10 Characters**: Wolverine, Cyclops, Storm, Jean Grey, Spider‑Man, Hulk, Captain America, Black Panther, Magneto, Scarlet Witch
- **4 Teams**: X‑Men, Avengers, Brotherhood of Mutants  
- **10 Genes**: Regenerative Mutation, Optic‑Blast, Weather Manipulation, Omega Level Telepathy, Radioactive Spider Mutation, Gamma Radiation Mutation, Super‑Soldier Serum, Heart‑Shaped Herb, Magnetokinesis, Chaos Magic
- **10 Powers**: Accelerated Healing, Enhanced Senses, Optic Blasts, Weather Control, Telepathy, Telekinesis, Superhuman Agility, Enhanced Strength, Superhuman Strength, Magnetism Control, Reality Manipulation
- **4 Relationship Types**: POSSESSES_POWER, HAS_MUTATION, CONFERS, MEMBER_OF

#### **Usage:**
```bash
python src/generate_data.py
```

**Note**: This script is the foundation of the entire system, creating all data from a single source of truth.
