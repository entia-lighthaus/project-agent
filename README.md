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

## LLM‑Powered Conversational Agent & Contextual Conversational Retrieval

Our recommendation engine is not a static list – it’s a conversational, persona‑aware agent that understands natural language, adapts to user feedback, and reasons across domains (restaurants, books, groceries, lifestyle). It is built on:

Groq Llama 3.3 70B – fast inference with high reasoning capability.

Unified behavior dataset – enriched with archetype, dominant_value, item_name, and cultural tags (Island/Mainland, price range).

Persona memory – each user’s archetype (e.g., Harsh Critic, Emotional Storyteller) and dominant value (e.g., service quality, ambience) drive recommendation logic.

Contextual awareness – automatically detects time of day, weekend, month‑end (budget mode), and location preference.

Multi‑turn conversation – stores chat history in Streamlit session state; the agent remembers previous exchanges and can refine recommendations (e.g., “cheaper”, “more options”, “different cuisine”).



# Example:

User:  I want a romantic rooftop dinner in Lagos.  

Agent: Sure! Are you thinking Island or Mainland?  

User: Island.  

Agent: I’d recommend Àkéta Rooftop in VI – modern African, mains ~₦15k, great sunset views. Or RSVP Lagos for a livelier lounge vibe. Would you like something more budget‑friendly?  

User: Yes, cheaper.  

Agent: Got it. For a romantic but affordable rooftop, try Sky Lounge on the Mainland – mains ~₦8k. Also, would you consider a book recommendation with a romantic theme?  

User: That would be lovely.  

Agent: “The Wedding Date” by Jasmine Guillory – a fun, romantic read that Lagos readers with an Emotional Storyteller persona loved.  

# Key capabilities
Feature & 	Implementation
- Persona injection: Prompt includes user archetype, dominant value, average rating.
- Cross‑domain transfer:	Retrieves from unified_behavior_df – seamlessly switches from restaurants to books/groceries based on user request.
- Cold‑start handling:	When no interaction history exists, agent asks clarifying questions (budget, location, occasion).
- LLM reasoning:	The agent explains why an item is recommended (“Because you value service quality and it’s month‑end, I chose this budget restaurant with high staff ratings”).
- Nigerian cultural grounding	(Uses location types (Island/Mainland), Pidgin expressions (na wa, abi, jare), and “sapa” budget logic.)

# Code location
Main agent logic: src/recommender/conversational_agent.py

Streamlit integration: app/pages/task_b.py

To run the conversational agent locally, select Task B in the Streamlit sidebar and start chatting. The agent will adapt to your chosen persona and domain.

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

