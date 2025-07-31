# Technical Architecture: Knowledge Graph + LLM Integration

## Overview

This document explains how I combined structured graph data with Large Language Models to create a system that can answer natural language questions about the Marvel Universe. The goal was to build something that could understand human questions and provide factual, engaging responses based on actual Marvel character data.

## How the System Works

The basic flow is simple: a user asks a question, the system figures out what they're asking about, looks up relevant information in my knowledge graph, and then uses an AI language model to generate a helpful response.

### The Core Process

1. **Understanding the Question**: The system uses natural language processing to identify Marvel characters, powers, genes, or teams mentioned in the question.

2. **Finding Relevant Information**: Once it knows what the user is asking about, it searches through our knowledge graph to find related facts and relationships.

3. **Building Context**: The system combines the factual information from the graph with character background stories to create rich context.

4. **Generating Response**: Finally, it uses OpenAI's language model to create a natural, informative answer based on the gathered information.

## Entity Recognition Evolution

### My Initial Approach

I started by trying to use a fuzzy matching library called RapidFuzz to identify Marvel entities in user questions. This approach had several problems:

- Fuzzy matching produced too many false positives, making it unreliable
- It couldn't understand the context or type of entities (character vs power vs team)
- It will be slow when dealing with large sets of entities

### My Current Approach

I switched to using spaCy, a more sophisticated natural language processing library, combined with sentence transformers. This approach is much better because:

- It can understand the type of entity being mentioned (character, power, gene, or team)
- It provides context-aware recognition
- It has robust fallback mechanisms for edge cases
- It's faster and more accurate

## Query Logic and Intent Detection

The system needs to understand not just what entity the user is asking about, but also what kind of information they want. For example, "What powers does Spider-Man have?" is different from "Which characters have Wall-Crawling?"

### Smart Entity Type Routing

The system uses different logic based on what type of entity is being asked about:

- **For Genes**: It looks for what powers that gene confers
- **For Powers**: It finds which characters possess that power (reverse lookup)
- **For Teams**: It finds which characters belong to that team (reverse lookup)
- **For Characters**: It uses more sophisticated intent detection to determine if the user wants powers, genes, or team information

### Graph Traversal Strategy

The knowledge graph is like a network of connections. The system can traverse these connections in two ways:

- **Forward Traversal**: Following connections from a character to their powers, genes, or teams
- **Reverse Traversal**: Finding which characters have a particular power or belong to a particular team

For complex graphs, Cypher would be much easier to use because it can automatically parse user queries and handle traversals without needing to manually create each query plan like I had to do in my implementation.

## LLM Integration and Prompt Engineering

### Context Building Strategy

When preparing information for the language model, I combine multiple sources:

- The original user question
- The identified entity and its type
- The relationship chain that was followed
- The factual results from the knowledge graph
- Character background stories for richer context

### System Prompt Design

I carefully designed the prompt that instructs the language model. The system tells the AI to:

- Act as a Marvel Universe expert and S.H.I.E.L.D. analyst
- Use only the provided context and facts
- Be factual and precise
- Cite specific characters, powers, genes, or teams mentioned
- Use character backgrounds to add rich storytelling
- Format responses clearly and informatively

### Character Context Enhancement

I include short background stories about characters to make responses more engaging. For example, instead of just listing Spider-Man's powers, the system can mention his origin story and the famous "with great power comes great responsibility" mantra.

## Neo4j vs NetworkX Comparison

### Why I Chose NetworkX

I considered using Neo4j, a dedicated graph database, but ultimately chose NetworkX, a Python library, for several reasons:

**Neo4j Advantages:**
- Has a powerful query language called Cypher that can parse natural language queries more elegantly
- Cypher automatically handles complex graph traversals without needing to manually write each query plan
- Better for very large graphs with millions of nodes
- Provides better data consistency guarantees
- Includes built-in graph algorithms
- Offers interactive graph visualization
- More declarative approach - you describe what you want, not how to get it

**Neo4j Disadvantages:**
- Requires database setup and management
- More complex deployment process
- Requires learning Cypher syntax
- Higher resource requirements
- More complex Python integration

**My NetworkX Choice:**
For my Marvel Knowledge Graph project, NetworkX was the better choice because:
- My dataset is small (only 34 nodes and 48 edges)
- It allows for rapid prototyping and iteration
- No database setup is required
- It's easier to understand and modify
- It integrates seamlessly with my existing Python code

## Key Technical Decisions

### Entity Recognition Strategy

I chose spaCy and Sentence Transformers over RapidFuzz because they provide better type awareness and context understanding. This resulted in more accurate entity extraction with fewer false positives.

### Graph Traversal Approach

I implemented custom traversal logic rather than using Cypher queries because it provides simpler deployment and easier debugging. This resulted in fast, reliable query execution with clear error handling. However, for more complex graphs, Cypher would be much easier to use since it can automatically parse user queries and handle traversals without needing to manually create each query plan like I had to do here.

### Context Building Strategy

I chose to combine structured context with character snippets because it balances factual accuracy with engaging storytelling. This results in responses that are both accurate and interesting to read.

### LLM Integration Pattern

I chose OpenAI's GPT-4o with carefully engineered prompts because it provides the best balance of capability and reliability. This results in high-quality responses that are grounded in my graph data.

### Scalability Considerations

The current system can handle 100+ concurrent queries. However, NetworkX performance would degrade with graphs containing 10,000+ nodes. For larger datasets in the future, we could migrate to Neo4j.
