
"""
Marvel Knowledge Graph API - Streamlit Demo

A beautiful web UI for testing the Marvel Knowledge Graph API endpoints
and exploring character relationships, powers, and team affiliations.
"""

import streamlit as st
import requests
import json
import time
from typing import Dict, Any, List
import os
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="Marvel Knowledge Graph API",
    page_icon="🦸‍♂️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for beautiful styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #1f77b4, #ff7f0e, #2ca02c, #d62728);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin: 0.5rem 0;
    }
    .response-box {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #007bff;
        margin: 1rem 0;
    }
    .error-box {
        background: #ffffff;
        padding: 1.5rem;
        border-radius: 10px;
        border: 2px solid #dc3545;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        color: #333333;
        font-size: 16px;
        line-height: 1.6;
    }
    .success-box {
        background: #ffffff;
        padding: 1.5rem;
        border-radius: 10px;
        border: 2px solid #28a745;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        color: #333333;
        font-size: 16px;
        line-height: 1.6;
    }
    .stButton > button {
        background: linear-gradient(90deg, #007bff, #0056b3);
        color: white;
        border: none;
        border-radius: 5px;
        padding: 0.5rem 1rem;
        font-weight: bold;
    }
    .stButton > button:hover {
        background: linear-gradient(90deg, #0056b3, #004085);
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# API Configuration
API_BASE_URL = "http://localhost:8000"

def check_api_health() -> bool:
    """Check if the API is running and healthy."""
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        return response.status_code == 200
    except:
        return False

def get_api_stats() -> Dict[str, Any]:
    """Get API statistics."""
    try:
        response = requests.get(f"{API_BASE_URL}/api/stats")
        return response.json() if response.status_code == 200 else {}
    except:
        return {}

def query_character_graph(character: str) -> Dict[str, Any]:
    """Query character's immediate neighbors in the graph."""
    try:
        response = requests.get(f"{API_BASE_URL}/graph/{character}")
        return response.json() if response.status_code == 200 else {"error": "Character not found"}
    except Exception as e:
        return {"error": f"API Error: {str(e)}"}

def ask_question(question: str) -> Dict[str, Any]:
    """Ask a question to the LLM-powered API."""
    try:
        response = requests.post(
            f"{API_BASE_URL}/question",
            json={"question": question},
            timeout=30
        )
        return response.json() if response.status_code == 200 else {"error": "Failed to get response"}
    except Exception as e:
        return {"error": f"API Error: {str(e)}"}

def main():
    """Main Streamlit application."""
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🦸‍♂️ Marvel Knowledge Graph API</h1>
        <p>Explore the Marvel Universe through AI-powered knowledge graph queries</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("🎯 Quick Actions")
        
        # API Status
        api_healthy = check_api_health()
        if api_healthy:
            st.success("✅ API Connected")
        else:
            st.error("❌ API Not Connected")
            st.info("Make sure the API is running on localhost:8000")
        
        # API Stats
        if api_healthy:
            stats = get_api_stats()
            if stats:
                st.subheader("📊 API Statistics")
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Nodes", stats.get("graph_nodes", 0))
                with col2:
                    st.metric("Edges", stats.get("graph_edges", 0))
        
        st.divider()
        
        # Quick Examples
        st.subheader("💡 Example Queries")
        example_queries = [
            "What powers does Spider-Man have?",
            "What characters belong to X-Men?",
            "What genes does Wolverine have?",
            "What powers does Regenerative Mutation confer?",
            "What characters have Enhanced Senses?",
            "What team does Captain America belong to?"
        ]
        
        for query in example_queries:
            if st.button(query, key=f"example_{query}"):
                st.session_state.question = query
                st.session_state.active_tab = "Question"
                st.rerun()
    
    # Main content
    tab1, tab2, tab3 = st.tabs(["🎯 Question Query", "🕸️ Character Graph", "📊 API Info"])
    
    with tab1:
        st.header("🎯 Ask Questions About Marvel Characters")
        st.markdown("Ask natural language questions about characters, powers, genes, and team affiliations.")
        
        # Question input
        question = st.text_area(
            "Enter your question:",
            value=st.session_state.get("question", ""),
            placeholder="e.g., What powers does Spider-Man have?",
            height=100
        )
        
        col1, col2 = st.columns([1, 4])
        with col1:
            ask_button = st.button("🚀 Ask Question", type="primary")
        
        with col2:
            if st.button("🔄 Clear"):
                st.session_state.question = ""
                st.rerun()
        
        if ask_button and question:
            with st.spinner("🤖 Processing your question..."):
                result = ask_question(question)
                
                if "error" in result:
                    st.markdown(f"""
                    <div class="error-box">
                        <h3 style="color: #dc3545; margin-bottom: 1rem; font-size: 20px;">❌ Error</h3>
                        <div style="background: #f8f9fa; padding: 1rem; border-radius: 8px; border-left: 4px solid #dc3545;">
                            {result['error']}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="success-box">
                        <h3 style="color: #28a745; margin-bottom: 1rem; font-size: 20px;">✅ AI Response</h3>
                        <div style="background: #f8f9fa; padding: 1rem; border-radius: 8px; border-left: 4px solid #007bff;">
                            {result.get('answer', 'No response received')}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Show additional info if available
                    if "query_plan" in result:
                        with st.expander("🔍 Query Plan"):
                            st.json(result["query_plan"])
                    
                    if "facts" in result:
                        with st.expander("📊 Query Facts"):
                            st.json(result["facts"])
    
    with tab2:
        st.header("🕸️ Explore Character Relationships")
        st.markdown("View a character's immediate connections in the knowledge graph.")
        
        # Character input
        col1, col2 = st.columns([2, 1])
        with col1:
            character = st.text_input(
                "Enter character name:",
                placeholder="e.g., Spider-Man, Wolverine, Captain America"
            )
        
        with col2:
            graph_button = st.button("🔍 View Graph", type="primary")
        
        if graph_button and character:
            with st.spinner("🕸️ Loading character graph..."):
                result = query_character_graph(character)
                
                if "error" in result:
                    st.markdown(f"""
                    <div class="error-box">
                        <h3 style="color: #dc3545; margin-bottom: 1rem; font-size: 20px;">❌ Error</h3>
                        <div style="background: #f8f9fa; padding: 1rem; border-radius: 8px; border-left: 4px solid #dc3545;">
                            {result['error']}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="success-box">
                        <h3 style="color: #28a745; margin-bottom: 1rem; font-size: 20px;">✅ Character Graph for {character}</h3>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Display graph data
                    if "connections" in result:
                        connections = result["connections"]
                        
                        # Teams
                        if "teams" in connections and connections["teams"]:
                            st.subheader("🏢 Teams")
                            for team in connections["teams"]:
                                st.markdown(f"• **{team}**")
                        
                        # Powers
                        if "powers" in connections and connections["powers"]:
                            st.subheader("⚡ Powers")
                            for power in connections["powers"]:
                                st.markdown(f"• **{power}**")
                        
                        # Genes
                        if "genes" in connections and connections["genes"]:
                            st.subheader("🧬 Genes")
                            for gene in connections["genes"]:
                                st.markdown(f"• **{gene}**")
                        
                        # Characters (for reverse queries)
                        if "characters" in connections and connections["characters"]:
                            st.subheader("👥 Characters")
                            for char in connections["characters"]:
                                st.markdown(f"• **{char}**")
                    
                    # Show raw data
                    with st.expander("📊 Raw Graph Data"):
                        st.json(result)
    
    with tab3:
        st.header("📊 API Information")
        st.markdown("Learn about the API endpoints and capabilities.")
        
        # API Status
        if api_healthy:
            st.success("✅ API is running and healthy")
            
            # Endpoints info
            st.subheader("🔗 Available Endpoints")
            
            endpoints = [
                {
                    "method": "GET",
                    "path": "/health",
                    "description": "Check API health status"
                },
                {
                    "method": "GET", 
                    "path": "/api/stats",
                    "description": "Get knowledge graph statistics"
                },
                {
                    "method": "GET",
                    "path": "/graph/{character}",
                    "description": "Get character's immediate neighbors"
                },
                {
                    "method": "POST",
                    "path": "/question",
                    "description": "Ask natural language questions"
                }
            ]
            
            for endpoint in endpoints:
                st.markdown(f"""
                **{endpoint['method']}** `{endpoint['path']}`  
                {endpoint['description']}
                """)
            
            # API Stats
            stats = get_api_stats()
            if stats:
                st.subheader("📈 Current Statistics")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Graph Nodes", stats.get("graph_nodes", 0))
                with col2:
                    st.metric("Graph Edges", stats.get("graph_edges", 0))
                with col3:
                    llm_status = "✅ Configured" if stats.get("llm_configured", False) else "❌ Not Configured"
                    st.metric("LLM Status", llm_status)
        else:
            st.error("❌ API is not accessible")
            st.info("""
            To start the API, run:
            ```bash
            uvicorn app.enhanced_api:app --host 0.0.0.0 --port 8000
            ```
            """)
        
        # Features
        st.subheader("🚀 Features")
        features = [
            "🔍 Natural language question answering",
            "🕸️ Knowledge graph exploration", 
            "🤖 LLM-powered responses with character context",
            "📊 Character relationships visualization",
            "🧬 Gene and power analysis",
            "🏢 Team affiliation tracking"
        ]
        
        for feature in features:
            st.markdown(f"• {feature}")
        
        # Setup instructions
        st.subheader("⚙️ Setup Instructions")
        st.markdown("""
        1. **Install dependencies**: `pip install -r requirements.txt`
        2. **Set environment variables**: Create `.env` file with `OPENAI_API_KEY`
        3. **Start the API**: `uvicorn app.enhanced_api:app --host 0.0.0.0 --port 8000`
        4. **Run this demo**: `streamlit run streamlit_demo.py`
        """)

if __name__ == "__main__":
    main() 