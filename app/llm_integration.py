"""
LLM Integration Module for Marvel Knowledge Graph API

This module handles the integration with OpenAI API to generate natural language
responses based on knowledge graph facts.
"""

import openai
from typing import Dict, Any
from app.config import OPENAI_API_KEY, OPENAI_MODEL, SNIPPETS


def generate_llm_response(question: str, facts: Dict[str, Any], query_plan: Dict[str, Any]) -> str:
    """
    Generate a natural language response using OpenAI API based on knowledge graph facts.
    
    Args:
        question: The user's original question
        facts: Dictionary containing query results and metadata
        query_plan: The execution plan used for the query
        
    Returns:
        str: Natural language response based on the knowledge graph facts
    """
    
    # Build context from facts
    context_parts = []
    
    if query_plan.get("start_entity"):
        start_entity = query_plan['start_entity']
        context_parts.append(f"Entity: {start_entity} ({query_plan.get('start_type', 'Unknown')})")
        
        # Add character snippet if available
        if start_entity in SNIPPETS:
            context_parts.append(f"Character Background: {SNIPPETS[start_entity]}")
    
    if query_plan.get("relation_chain"):
        context_parts.append(f"Relationships: {' → '.join(query_plan['relation_chain'])}")
    
    if facts.get("results"):
        if isinstance(facts["results"], list):
            context_parts.append(f"Results: {', '.join(facts['results'])}")
            
            # Add snippets for result characters if they're characters
            character_results = []
            for result in facts["results"]:
                if result in SNIPPETS:
                    character_results.append(f"{result}: {SNIPPETS[result]}")
            
            if character_results:
                context_parts.append("Character Details:")
                context_parts.extend(character_results)
        else:
            context_parts.append(f"Results: {facts['results']}")
    
    context = "\n".join(context_parts)
    
    # Create the prompt
    system_prompt = """You are a Marvel Universe expert and S.H.I.E.L.D. analyst. 
Your task is to provide accurate, informative answers about Marvel characters, their powers, genes, and team affiliations.

Use ONLY the provided context and facts. Be factual and precise. If the context doesn't contain enough information, say so.
Always cite specific characters, powers, genes, or teams mentioned in the context.

When character backgrounds are provided, use them to add rich context and storytelling to your responses.
Incorporate the character's history, personality, and background into your explanations to make them more engaging and informative.

Format your response in a clear, informative way that directly answers the user's question."""

    user_prompt = f"""Question: {question}

Context from Knowledge Graph:
{context}

Please provide a comprehensive answer based on the above context."""

    try:
        client = openai.OpenAI(api_key=OPENAI_API_KEY)
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.3,
            max_tokens=500
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error generating response: {str(e)}"


def create_context_summary(facts: Dict[str, Any], query_plan: Dict[str, Any]) -> str:
    """
    Create a summary of the knowledge graph context for LLM consumption.
    
    Args:
        facts: Dictionary containing query results and metadata
        query_plan: The execution plan used for the query
        
    Returns:
        str: Formatted context summary
    """
    summary_parts = []
    
    # Add query type
    if facts.get("query_type"):
        summary_parts.append(f"Query Type: {facts['query_type']}")
    
    # Add start entity and type
    if query_plan.get("start_entity"):
        summary_parts.append(f"Start Entity: {query_plan['start_entity']} ({query_plan.get('start_type', 'Unknown')})")
    
    # Add relationship chain
    if query_plan.get("relation_chain"):
        summary_parts.append(f"Relationships: {' → '.join(query_plan['relation_chain'])}")
    
    # Add results
    if facts.get("results"):
        if isinstance(facts["results"], list):
            summary_parts.append(f"Found Results: {', '.join(facts['results'])}")
        else:
            summary_parts.append(f"Found Results: {facts['results']}")
    
    return "\n".join(summary_parts)


def validate_llm_config() -> bool:
    """
    Validate that the LLM configuration is properly set up.
    
    Returns:
        bool: True if configuration is valid, False otherwise
    """
    if not OPENAI_API_KEY:
        return False
    if not OPENAI_MODEL:
        return False
    return True 