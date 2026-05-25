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


st.title("Task B — Agentic Recommendation Engine")

# -------------------------------
# 1. LOAD DATA
# -------------------------------
@st.cache_data
def load_data():
    persona_df = pd.read_csv(os.path.join(PROJECT_ROOT, "outputs", "persona_dataset_full.csv"))
    unified_df = pd.read_csv(os.path.join(PROJECT_ROOT, "outputs", "unified_behavior_with_archetype.csv"))
    lagos_df = pd.read_csv(os.path.join(PROJECT_ROOT, "data", "external", "lagos_restaurants_metadata.csv"))
    return persona_df, unified_df, lagos_df

persona_df, unified_behavior_df, lagos_df = load_data()

# -------------------------------
# 2. CONTEXT OPTIONS (Nigerian‑flavoured)
# -------------------------------
contexts = {
    "celebration": "Excited, generous, willing to spend",
    "comfort_food_mood": "Warm, nostalgic, values portion size and taste",
    "social_night_out": "Energetic, prefers loud music and group seating",
    "weekday_quick_meal": "Practical, values speed and value for money",
    "sapa_budget": "Highly price‑sensitive, will compromise on ambience",
    "romantic_date": "Focuses on ambience, quietness, and presentation"
}

# -------------------------------
# 3. SESSION STATE FOR MULTI‑TURN CONVERSATION
# -------------------------------
if "conversation_memory" not in st.session_state:
    st.session_state.conversation_memory = []
if "last_recommendations" not in st.session_state:
    st.session_state.last_recommendations = []
if "user_feedback" not in st.session_state:
    st.session_state.user_feedback = None

# -------------------------------
# 4. COLD‑START HANDLER (new user with no history)
# -------------------------------
def cold_start_preferences():
    st.subheader("Tell us a bit about yourself (cold‑start)")
    fav_cuisine = st.selectbox("What type of food do you usually like?", 
                               ["Nigerian", "Fast Food", "Fine Dining", "Cafe", "Any"])
    budget = st.selectbox("What's your typical budget per person?", ["Budget (under ₦5k)", "Moderate (₦5k-₦15k)", "Premium (₦15k+)"])
    location = st.radio("Preferred location?", ["Island", "Mainland", "No preference"])
    return {"cuisine": fav_cuisine, "budget": budget, "location": location}

# -------------------------------
# 5. CONTEXTUAL FEATURES (time, day, month‑end)
# -------------------------------
def get_contextual_features():
    now = datetime.now()
    hour = now.hour
    day = now.weekday()  # Monday=0
    is_weekend = day >= 5
    is_month_end = now.day >= 25
    
    if hour < 11:
        time_context = "morning"
    elif hour < 16:
        time_context = "afternoon"
    else:
        time_context = "evening"
    
    return {
        "time_of_day": time_context,
        "is_weekend": is_weekend,
        "is_month_end": is_month_end,
        "suggestion": "budget" if is_month_end else "regular"
    }

# -------------------------------
# 6. USER INTERFACE
# -------------------------------
col1, col2 = st.columns(2)
with col1:
    selected_archetype = st.selectbox("Select Persona Archetype", persona_df["archetype"].unique())
with col2:
    selected_context = st.selectbox("Select Recommendation Context", list(contexts.keys()))

# Cold‑start toggle
cold_start = st.checkbox("I'm a new user (cold‑start mode)", value=False)
if cold_start:
    cold_start_prefs = cold_start_preferences()
else:
    cold_start_prefs = None

# Contextual features (automatically detected)
ctx = get_contextual_features()
st.info(f" Context: {ctx['time_of_day']}, {'weekend' if ctx['is_weekend'] else 'weekday'}, {'month‑end (budget mode)' if ctx['is_month_end'] else 'regular spending'}")

# Multi‑turn feedback (if user already saw recommendations)
if st.session_state.last_recommendations:
    user_feedback = st.selectbox("Did you like any of the previous recommendations?", ["", "Yes, show more like that", "No, try different ones", "Seen that before"])
    if user_feedback:
        st.session_state.user_feedback = user_feedback

# Generate button
if st.button("Generate Personalized Recommendations"):
    # Sample a persona row
    sampled_persona = persona_df[persona_df["archetype"] == selected_archetype].sample(1).iloc[0]
    
    # Sample a business (or cold‑start override)
    if cold_start and cold_start_prefs:
        # Filter by budget and location
        filtered = lagos_df.copy()
        if "Budget" in cold_start_prefs["budget"]:
            filtered = filtered[filtered["price_range"] == "Budget"]
        elif "Premium" in cold_start_prefs["budget"]:
            filtered = filtered[filtered["price_range"] == "Premium"]
        if cold_start_prefs["location"] != "No preference":
            filtered = filtered[filtered["location_type"] == cold_start_prefs["location"]]
        if len(filtered) > 0:
            sampled_business = filtered.sample(1).iloc[0]
        else:
            sampled_business = lagos_df.sample(1).iloc[0]
    else:
        sampled_business = lagos_df.sample(1).iloc[0]
    
    # Include contextual features in the call
    output = run_agentic_recommendation_pipeline(
        persona_row=sampled_persona,
        business_row=sampled_business,
        unified_behavior_df=unified_behavior_df,
        context_name=selected_context,
        user_id="streamlit_recommender_user",
        additional_context=ctx   # pass time, month‑end etc.
    )
    
    # Store recommendations in session state for multi‑turn
    st.session_state.last_recommendations = output["recommendations"]
    st.session_state.conversation_memory.append({"role": "user", "context": selected_context})
    st.session_state.conversation_memory.append({"role": "assistant", "recommendations": output["recommendations"][:3]})
    
    # Display recommendations
    st.subheader("Behavioral Recommendations")
    for rec in output["recommendations"]:
        st.markdown("---")
        st.write(f"### Domain: {rec['domain']}")
        st.write(f"⭐ Rating: {rec.get('rating', 'N/A')}")
        st.write(rec.get("recommendation_preview", "No preview"))
        st.info(f" {rec.get('explanation', 'No explanation')}")
    
    # Show reasoning trace if available
    if "reasoning" in output:
        with st.expander("See agentic reasoning trace"):
            st.write(output["reasoning"])
    
    st.subheader("Multiturn Memory")
    st.write(output.get("memory_context", "No memory context"))
    st.success("Recommendations generated with contextual awareness.")

# Add a reset button for conversation memory
if st.button("Reset Conversation"):
    st.session_state.conversation_memory = []
    st.session_state.last_recommendations = []
    st.session_state.user_feedback = None
    st.rerun()