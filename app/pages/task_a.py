import os
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  
# TASK A: AGENTIC REVIEW GENERATION
# This page implements Task A, which focuses on generating agentic reviews based on user personas. 
# It allows users to select a persona archetype and a context, and then generates a review that reflects the selected persona's characteristics and the chosen context. 
# This demonstrates the system's ability to create personalized and context-aware content, which is a crucial component of the overall agentic recommendation system.

# TASK A: AGENTIC REVIEW GENERATION
# Simulates a user review (rating + text) for a given persona, context, and restaurant.

import sys



sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "../.."
        )
    )
)

import streamlit as st
import pandas as pd
import random
import requests
import json

# =========================
# 1. CONFIGURE PAGE
# =========================
st.set_page_config(page_title="Task A - Simulated Reviews", layout="wide")
st.title("Task A — Agentic Review Generation")

# =========================
# 2. LOAD DATA
# =========================
@st.cache_data
def load_data():
    persona_df = pd.read_csv("outputs/persona_dataset_full.csv")
    #persona_df = pd.read_csv("../outputs/persona_dataset_full.csv")
    unified_df = pd.read_csv("../outputs/unified_behavior_with_archetype.csv")
    restaurant_df = pd.read_csv("../data/external/lagos_restaurants_metadata.csv")
    return persona_df, unified_df, restaurant_df

# Then unpack:
persona_df, unified_behavior_df, lagos_df = load_data()


# =========================
# 3. CONTEXT OPTIONS (Nigerian‑flavoured)
# =========================
contexts = [
    "celebration",
    "social_night_out",
    "weekday_quick_meal",
    "comfort_food_mood",
    "date_night",
    "sapa_budget"
]

# =========================
# 4. HELPER: RETRIEVE FEW‑SHOT EXAMPLES
# =========================
def get_few_shot_examples(archetype, target_restaurant, unified_df, n=8):
    """
    Retrieve past reviews from the same archetype (random sample).
    target_restaurant is not used for filtering but kept for potential future use.
    """
    archetype_reviews = unified_df[unified_df["archetype"] == archetype]
    if len(archetype_reviews) == 0:
        archetype_reviews = unified_df.copy()  # fallback to all reviews
    

    # Try to match category if provided
    target_cat = target_restaurant.get("category", "").lower()
    if target_cat and len(archetype_reviews) > n:
        # filter reviews containing the category keyword (crude but works)
        matched = archetype_reviews[archetype_reviews["review_text"].str.lower().str.contains(target_cat, na=False)]
        if len(matched) >= n:
            archetype_reviews = matched
    # Try to match vibe keywords if category filtering is too strict 

    # Sample n reviews (or fewer if not enough)
    sample_size = min(n, len(archetype_reviews))
    sampled = archetype_reviews.sample(sample_size, random_state=42)
    
    examples = []
    for _, row in sampled.iterrows():
        examples.append({
            "rating": row["rating"],
            "review_text": row["review_text"][:200]  # truncate
        })
    return examples


# =========================
# 5. LLM CALL (GroqCloud API - Llama 3 70B)
# =========================
def call_llm(prompt, api_key):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.4,
        "max_tokens": 300
    }

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        st.error(f"LLM API error: {response.status_code} - {response.text}")
        return None


# =========================
# 6. PROMPT CONSTRUCTION
# =========================
def build_prompt(persona, target_business, context, few_shots):
    archetype = persona.get("archetype", "Balanced Reviewer")
    dominant_value = persona.get("dominant_value", "neutral")
    avg_rating = persona.get("avg_rating", 3.5)
    style = persona.get("style", "neutral_general")  # from earlier taxonomy

    # Context mapping to tone instructions
    context_tones = {
        "celebration": "Excited, generous, may overlook small flaws",
        "social_night_out": "Energetic, focuses on crowd and music",
        "weekday_quick_meal": "Practical, values speed and value",
        "comfort_food_mood": "Warm, nostalgic, values portion size",
        "date_night": "Romantic, attentive to ambience and service",
        "sapa_budget": "Price‑sensitive, critical of any waste"
    }

    tone = context_tones.get(context, "Balanced and honest")

    prompt = f"""You are simulating a real user on a Nigerian restaurant review platform.
    f"- User's historical average rating: {avg_rating:.1f} stars. Keep your predicted rating close to this value unless the restaurant is exceptionally good or bad.\n"

**User Persona:**
- Archetype: {archetype}
- Dominant value: {dominant_value}
- Typical rating: {avg_rating:.1f} stars
- Writing style: {style}
- Current mood/context: {context} → {tone}

**Examples of this user's past reviews (few‑shot):**
"""
    for i, ex in enumerate(few_shots, 1):
        prompt += f"{i}. Rating: {ex['rating']} stars\n   Review: {ex['review_text']}\n"

    prompt += f"""
**Now write a NEW review for this restaurant:**
Name: {target_business.get('name', 'Unknown')}
Category: {target_business.get('category', 'Nigerian')}
Price range: {target_business.get('price_range', 'moderate')}
Location: {target_business.get('location', 'Lagos')}
Description: {target_business.get('description', 'A local spot')}

**Output exactly in this format:**
Rating: (1-5 integer)
Review: (natural language review in the user's voice, 50-200 words. Write in **standard English** with occasional Nigerian Pidgin phrases (like "na wa", "abi", "sef", "jare") – not full Pidgin. Include at least one specific detail: dish name, price, wait time, or staff interaction. Avoid generic statements.)


Do NOT add any extra text or explanations.
"""
    return prompt


# =========================
# 7. PARSE LLM RESPONSE
# =========================
def parse_llm_response(response_text):
    """Extract rating and review from LLM output."""
    rating = None
    review = "Could not parse response."
    lines = response_text.strip().split("\n")
    for line in lines:
        if line.lower().startswith("rating:"):
            try:
                rating = int(line.split(":")[1].strip())
                rating = max(1, min(5, rating))
            except:
                rating = 3
        elif line.lower().startswith("review:"):
            review = line.split(":", 1)[1].strip()
    if rating is None:
        rating = 3  # fallback
    return rating, review


# =========================
# 8. MAIN UI
# =========================
# Persona selector
selected_archetype = st.selectbox("Select Persona Archetype", persona_df["archetype"].unique())
selected_context = st.selectbox("Select Context", contexts)

# Optionally select a specific restaurant (or random)
use_random = st.checkbox("Random restaurant each time", value=True)
if not use_random:
    restaurant_names = lagos_df["name"].tolist()
    selected_restaurant = st.selectbox("Or choose a restaurant", restaurant_names)
else:
    selected_restaurant = None

if st.button("Generate Simulated Review"):
    # 1. Get persona row
    sampled_persona = persona_df[persona_df["archetype"] == selected_archetype].sample(1).iloc[0]
    
    # 2. Get business row
    if selected_restaurant:
        target_business = lagos_df[lagos_df["name"] == selected_restaurant].iloc[0]
    else:
        target_business = lagos_df.sample(1).iloc[0]
    
    # 3. Retrieve few‑shot examples (same archetype)
    few_shots = get_few_shot_examples(selected_archetype, target_business, unified_behavior_df, n=3)
    
    # 4. Build prompt
    prompt = build_prompt(sampled_persona, target_business, selected_context, few_shots)
    
    # 5. Call LLM (requires Groq API key in secrets)
    
    import streamlit as st
    try:
        api_key = st.secrets["GROQ_API_KEY"]
    except KeyError:
        st.error("API Key not found. Please set GROQ_API_KEY in your Streamlit Cloud app secrets.")
        st.stop()

     
    # api_key = st.secrets.get("GROQ_API_KEY", None)

    if not api_key:
        st.error("Groq API key not found. Please set GROQ_API_KEY in Streamlit secrets.")
    else:
        with st.spinner("Simulating review..."):
            llm_output = call_llm(prompt, api_key)
            if llm_output:
                rating, review_text = parse_llm_response(llm_output)
                
                # Display result
                st.subheader(f" Simulated Review for: {target_business.get('name')}")
                # Show rating as stars
                star_display = "⭐" * rating + "☆" * (5 - rating)
                st.write(f"**Rating:** {star_display} ({rating}/5)")
                st.write(f"**Review:**\n{review_text}")
                
                # Optional: show the few‑shot examples used (for transparency)
                with st.expander("See few‑shot examples used"):
                    for i, ex in enumerate(few_shots, 1):
                        st.write(f"**Ex.{i}** – Rating: {ex['rating']} stars")
                        st.write(f"_{ex['review_text']}_")
                        st.write("---")
            else:
                st.error("Review generation failed. Check API key or network.")


# =========================
# 9. FOOTNOTE
# =========================
st.caption("Task A: Simulated reviews using LLM + few‑shot personas + Nigerian context.")