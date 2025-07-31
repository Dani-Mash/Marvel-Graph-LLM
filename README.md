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
🎥 **UI Demo Video** - Streamlit Web Application

*Watch the full demonstration of the Marvel Graph LLM system in action, showcasing both API endpoints.*

**📁 Video File**: `assets/ui_demo_app.mp4` (30MB - available locally)

**📺 To View**: 
- **Local**: Run the application and view the video in the `assets/` folder
- **GitHub Releases**: Video will be uploaded to repository releases for easy access
- **External**: Video can be hosted on YouTube/Vimeo for web viewing

**🎯 Demo Features Shown**:
- Interactive question interface with natural language processing
- Real-time API calls to POST /question endpoint
- Character relationship visualization with GET /graph/{character} endpoint
- AI-powered responses grounded in knowledge graph data

### **What You'll See in the Demo:**
- **Interactive Question Interface**: Ask natural language questions about Marvel characters
- **AI-Powered Responses**: Get detailed, grounded answers about powers, teams, and relationships
- **Graph Visualization**: See character relationships and connections in real-time
- **API Integration**: Watch the seamless connection between the web interface and backend API

## 📚 Documentation

### **🧪 Sample Queries & Responses**
See [`docs/sample_queries.md`](docs/sample_queries.md) for detailed, grounded query/response examples and LLM grounding explanations.

### **🧠 Technical Architecture**
See [`docs/technical_architecture.md`](docs/technical_architecture.md) for a comprehensive explanation of how the knowledge graph data is combined with the LLM, including prompt engineering, query logic, entity extraction evolution, and technology choices.

## 📊 Jupyter Notebooks

### **1. Graph Visualization & Analysis** (`notebooks/exploratory_graph.ipynb`)
Comprehensive visualization and analysis of the Marvel Knowledge Graph with color-coded nodes, relationship schemas, and statistical analysis.

### **2. Knowledge Graph Query Engine Testing** (`notebooks/test_kg_query_engine.ipynb`)
Demonstrates the knowledge graph query engine with comprehensive testing of entity recognition, intent detection, and response generation.

## 📊 Data Generation

### **Knowledge Graph Data Creation** (`src/generate_data.py`)

Creates the complete Marvel Knowledge Graph dataset from a single source of truth.

**Generated Files:**
- **Entities**: `characters.csv`, `teams.csv`, `genes.csv`, `powers.csv`
- **Relationships**: `char_team.csv`, `char_gene.csv`, `gene_power.csv`, `char_power.csv`
- **Character Backgrounds**: `text_snippets.json`
- **Complete Graph**: `marvel_kg.graphml` (34 nodes, 48 edges)

**Usage:**
```bash
python src/generate_data.py
```

**Note**: This script is the foundation of the entire system, creating all data from a single source of truth.
