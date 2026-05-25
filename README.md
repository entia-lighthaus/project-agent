# Agentic Persona Intelligence System

An advanced behavioral AI system for agentic review generation and contextual conversational recommendations.

**Hackathon:** Bluechip Tech Challenge – Agentic User Modeling & Recommendation  
**Team:** GreenIQ 
**Live Demo:** [https://project-agent-7zpdykrqys3xnqmsdmpyme.streamlit.app/]
**GitHub:** [https://github.com/entia-lighthaus/project-agent.git]


# Summary
This project was built for a multi-task AI hackathon focused on:

Task A
User Modeling - Given a user’s past reviews and an unseen item, the agent generates a realistic star rating and a written review that mimics the user’s voice, tone, and cultural expression.

Task B
Recommendation Intelligence - An agentic recommender that retrieves, ranks, and explains recommendations while handling multi‑turn dialogue, cold‑start, cross‑domain transfer, and Nigerian context (Island vs Mainland, price sensitivity, social proof).

The project combines retrieval‑augmented few‑shot prompting, LLM reasoning (Groq Llama‑3.3‑70B), and behavioural clustering to achieve culturally aware, personalised outputs.

Key Innovations Include:

- Behavioral persona modeling
- Emotional simulation
- Multi-agent debate and reasoning
- Conversational retrieval
- Cross-domain recommendation intelligence
- Memory-aware interactions
- Contextual recommendation orchestration

---

# Overview

Traditional recommendation systems rely heavily on collaborative filtering and static embeddings. These approaches struggle with:

* cold-start users, 
* contextual reasoning, 
* conversational recommendations, 
* emotional adaptation, 
* cross-domain preference transfer, 
* explainability.

This project introduces a cognitively informed agentic architecture that reasons about:

* user archetypes, 
* emotional context, 
* conversational memory, 
* behavioral patterns, 
* contextual intent.

before generating:

* reviews,
* ratings,
* recommendations,
* conversational responses.

---

# Core Features

## Task A — Agentic User Modeling

### Behavioral Persona Discovery

* K-Means behavioral clustering
* Human-readable archetype assignment
* Sentiment-driven behavioral signals
* Emotional variability modeling

### Archetypes

The system identifies multiple behavioral personas such as:

* Warm Optimist
* Reactive Reviewer
* Harsh Critic
* Emotional Storyteller
* Deep Experience Analyst

### Cognitive Simulation

* Context-aware emotional reasoning
* Rating volatility simulation
* Emotional drift
* Context-sensitive review generation

### Multi-Agent Debate Engine

The system simulates multiple reasoning agents debating:

* emotional satisfaction
* analytical quality
* contextual alignment
* value consistency

before generating final outputs.

### Counterfactual Reasoning

The system evaluates hypothetical behavioral changes such as:

> “How would the rating change if service improved?”

This improves:

* interpretability
* behavioral realism
* cognitive transparency

### Memory-Aware Reasoning

The system maintains lightweight conversational memory across interactions.

---

# Task B — Agentic Recommendation Intelligence

## Contextual Conversational Retrieval

The recommendation engine supports:

* natural language recommendation requests
* clarification questions
* conversational memory
* contextual recommendation reasoning

Example:

User:

> “I want a chill rooftop in Lagos for date night.”

Agent:

> “Mainland or Island?”

---

## Cross-Domain Recommendation Intelligence

The system performs behavioral retrieval across:

* restaurants
* books
* grocery products
* home and lifestyle products

using:

* Yelp
* Lagos restaurant data
* Goodreads
* Amazon Grocery
* Amazon Home & Kitchen

---

## Conversational Recommendation Agent

The system includes a multiturn conversational agent capable of:

* slot filling
* clarification reasoning
* memory persistence
* contextual recommendations

The agent dynamically retrieves recommendations from real Lagos restaurant data.

---

# Architecture

## Layer 1 — Behavioral Modeling

Responsible for:

* feature engineering
* sentiment aggregation
* clustering
* archetype generation

## Layer 2 — Cognitive Simulation

Responsible for:

* emotional simulation
* contextual reasoning
* multi-agent debate
* counterfactual reasoning
* memory systems

## Layer 3 — Recommendation Intelligence

Responsible for:

* behavioral retrieval
* conversational recommendations
* cross-domain taste transfer
* contextual ranking
* recommendation explanations

---

# Datasets Used

## Yelp Academic Dataset

Used for:

* behavioral modeling
* review generation
* persona discovery

## Lagos Restaurant Dataset

Used for:

* Nigerian contextual adaptation
* conversational restaurant retrieval

## Goodreads Reviews

Used for:

* literary preference modeling
* cross-domain taste transfer

## Amazon Grocery Reviews

Used for:

* food preference behavior

## Amazon Home & Kitchen Reviews

Used for:

* lifestyle recommendation reasoning

---

# Evaluation Metrics

## Task A — User Modeling

### Rating Accuracy

* RMSE (Root Mean Squared Error)

### Review Quality

* ROUGE


### Behavioral Fidelity

Measured through:

* archetype consistency
* emotional alignment
* contextual realism

---

## Task B — Recommendation Intelligence

### Ranking Quality

* NDCG@10
* Hit Rate@10

### Recommendation Evaluation

* personalization quality
* conversational continuity
* contextual alignment
* cross-domain relevance

---

# Project Structure

```bash
project-agent/
│
├── app/
│   ├── streamlit_app.py
│   └── pages/
│
├── data/
│   ├── raw/
│   ├── curated/
│   └── external/
│
├── notebooks/
│
├── outputs/
│
├── src/
│   ├── personas/
│   ├── reasoning/
│   ├── memory/
│   └── recommender/
│
├── requirements.txt
├── Dockerfile
└── README.md
```

---

# Streamlit Application

The project includes a full Streamlit application with:

## Task A Page

* review generation
* behavioral reasoning
* multi-agent debate
* counterfactual reasoning

## Task B Page

* personalized recommendations
* cross-domain retrieval
* recommendation explanations

## Conversational Agent Page

* natural language interaction
* clarification questions
* conversational memory
* contextual retrieval

---

# Installation

## Clone Repository

```bash
git clone <your_repo_url>
cd project-agent
```

---

## Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Running the Application

## Launch Streamlit

```bash
cd app
streamlit run streamlit_app.py
```

---

# Docker Support

Build container:

```bash
docker build -t agentic-system .
```

Run container:

```bash
docker run -p 8501:8501 agentic-system
```

---

# Key Innovations

This project introduces several novel components:

* Agentic behavioral reasoning
* Multi-agent debate systems
* Conversational recommendation retrieval
* Counterfactual behavioral reasoning
* Cross-domain taste transfer
* Contextual conversational AI
* Memory-aware recommendation intelligence
* Nigerian contextual adaptation

---

# Future Improvements

Potential future work includes:

* reinforcement learning adaptation
* vector database memory systems
* graph neural networks for taste propagation
* multimodal recommendation systems
* real-time conversational agents
* persistent long-term memory
* voice interaction systems

---

# Author
Innocentia Duru

Built as part of an advanced AI behavioral intelligence and recommendation systems project.

---

