# TASK B: AGENTIC RECOMMENDATION ENGINE
# This page implements Task B, which focuses on generating agentic recommendations based on user personas and selected contexts. 
# It allows users to select a persona archetype and a recommendation context, and then generates a set of recommendations that align with the selected persona and context. 
# This demonstrates the system's ability to create personalized and context-aware recommendations, which is a crucial component of the overall agentic recommendation system.   
# Contextual, conversational, cross‑domain recommendations with Nigerian cultural awareness.

import sys
import os
import streamlit as st
import pandas as pd
import random
from datetime import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.recommender.agentic_orchestrator import run_agentic_recommendation_pipeline
from src.recommender.agentic_orchestrator import simulate_user_review
from src.recommender.conversational_agent import conversational_agent
from src.recommender.behavioral_retrieval import retrieve_behavioral_matches
from src.recommender.recommendation_generation import generate_conversational_recommendations


st.set_page_config(page_title="Task B - Conversational Recommender", layout="wide")
st.title("Task B — Agentic Recommendation Engine")

# ----------------------------------------------------------------------
# 1. LOAD DATA (cached)
# ----------------------------------------------------------------------
@st.cache_data
def load_data():
    persona_df = pd.read_csv(os.path.join(PROJECT_ROOT, "outputs", "persona_dataset_full.csv"))
    unified_df = pd.read_csv(os.path.join(PROJECT_ROOT, "outputs", "unified_behavior_with_archetype.csv"))
    lagos_df = pd.read_csv(os.path.join(PROJECT_ROOT, "data", "external", "lagos_restaurants_metadata.csv"))
    return persona_df, unified_df, lagos_df

persona_df, unified_behavior_df, lagos_df = load_data()

# ----------------------------------------------------------------------
# 2. INITIALISE SESSION STATE
# ----------------------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []          # list of {"role": "user/assistant", "content": ...}
if "last_recommendations" not in st.session_state:
    st.session_state.last_recommendations = []
if "constraints" not in st.session_state:
    st.session_state.constraints = {}        # budget, location, cuisine
if "domain_choice" not in st.session_state:
    st.session_state.domain_choice = "Lagos restaurants"

# ----------------------------------------------------------------------
# 3. SIDEBAR - Persona, context, cold‑start, domain
# ----------------------------------------------------------------------
with st.sidebar:
    st.header("⚙️ Configuration")
    selected_archetype = st.selectbox("Persona Archetype", persona_df["archetype"].unique())
    
    # Domain selector
    domain_options = {
        "Lagos restaurants": "lagos_restaurants",
        "Yelp restaurants": "yelp",
        "Books (cross‑domain)": "goodreads",
        "All domains": None
    }
    selected_domain_label = st.selectbox("Recommendation domain", list(domain_options.keys()))
    st.session_state.domain_choice = domain_options[selected_domain_label]
    
    cold_start = st.checkbox("I'm a new user (cold‑start mode)")
    
    # Additional constraints
    st.subheader("Preferences (optional)")
    budget = st.selectbox("Budget", ["Any", "Budget", "Moderate", "Premium"])
    location = st.selectbox("Location", ["Any", "Island", "Mainland"])
    cuisine = st.text_input("Cuisine preference (e.g., 'Nigerian', 'Italian')")
    
    # Contextual signals (auto‑detected)
    now = datetime.now()
    is_weekend = now.weekday() >= 5
    is_month_end = now.day >= 25
    hour = now.hour
    if hour < 12:
        time_of_day = "morning"
    elif hour < 18:
        time_of_day = "afternoon"
    else:
        time_of_day = "evening"
    
    st.info(f" Context: {time_of_day}, {'weekend' if is_weekend else 'weekday'}, {'month‑end (budget mode)' if is_month_end else 'regular spending'}")

# ----------------------------------------------------------------------
# 4. HELPER: Call orchestrator with current context & constraints
# ----------------------------------------------------------------------
def get_recommendations(user_message=None):
    # Build persona row
    persona_row = persona_df[persona_df["archetype"] == selected_archetype].sample(1).iloc[0].to_dict()
    
    # Build constraints dict
    constraints = {
        "budget": budget if budget != "Any" else None,
        "location": location if location != "Any" else None,
        "cuisine": cuisine if cuisine else None,
        "cold_start": cold_start,
        "time_of_day": time_of_day,
        "is_weekend": is_weekend,
        "is_month_end": is_month_end
    }
    
    domain_choice = st.session_state.domain_choice
    
    # If user_message not provided, set a default
    if not user_message:
        user_message = "Give me recommendations"
    else:
        # Append user message to conversation history
        st.session_state.messages.append({"role": "user", "content": user_message})
    
    # Call the conversational agent (this is the core LLM call)
    response = conversational_agent(
        user_message=user_message,
        user_id="streamlit_user",
        persona_row=persona_row,
        domain=domain_choice,
        constraints=constraints,
        conversation_history=st.session_state.messages
    )
    
    # Append assistant response to conversation history
    st.session_state.messages.append({"role": "assistant", "content": response})
    
    # For demonstration, we will just show the raw response from the agent. In a real implementation, you would parse this response and extract structured recommendation data to display nicely.
# ----------------------------------------------------------------------
# 5. DISPLAY CONVERSATION HISTORY
# ----------------------------------------------------------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"]) 

# ----------------------------------------------------------------------
# 6. CHAT INPUT (multiturn)
# ----------------------------------------------------------------------
if prompt := st.chat_input("Ask for recommendations or give feedback (e.g., 'more options', 'cheaper', 'different cuisine')..."):
    # Process user message: simple intent extraction
    if "more options" in prompt.lower():
        # Rerun with same constraints but increase top_k (handled inside orchestrator)
        get_recommendations(user_message=prompt)
    elif "cheaper" in prompt.lower() or "budget" in prompt.lower():
        st.session_state.constraints["budget"] = "Budget"
        get_recommendations(user_message=prompt)
    elif "different" in prompt.lower() or "not good" in prompt.lower():
        # force a new random sample
        get_recommendations(user_message=prompt)
    else:
        get_recommendations(user_message=prompt)
    
    st.rerun()

    response = conversational_agent(
        user_message=prompt,
        user_id="streamlit_user",
        persona_row=persona_row,
        domain=st.session_state.domain_choice,
        constraints={
            "budget": budget if budget != "Any" else None,
            "location": location if location != "Any" else None
        },
        conversation_history=st.session_state.messages
    )
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.rerun()

# ----------------------------------------------------------------------
# 7. BUTTON FOR INITIAL RECOMMENDATION (if no conversation yet)
# ----------------------------------------------------------------------
if len(st.session_state.messages) == 0:
    if st.button("Start Conversation & Get Recommendations"):
        get_recommendations()
        st.rerun()

# ----------------------------------------------------------------------
# 8. RESET BUTTON
# ----------------------------------------------------------------------
if st.sidebar.button("Reset Conversation"):
    st.session_state.messages = []
    st.session_state.last_recommendations = []
    st.session_state.constraints = {}
    st.rerun()