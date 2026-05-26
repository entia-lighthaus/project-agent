# CONVERSATIONAL AGENT
# This module implements a conversational agent that interacts with users to extract preferences, 
# maintain memory, and generate personalized recommendations in a multi-turn dialogue format. It uses simple 
# rule-based extraction for demonstration but can be extended with more advanced NLP techniques for better 
# understanding and interaction. The agent maintains a memory of user interactions to provide a more personalized 
# and context-aware recommendation experience over time, demonstrating conversational continuity.

# conversational_agent.py – LLM‑powered, cross‑domain, persona‑aware
# conversational_agent.py
# LLM-powered, cross-domain, persona-aware conversational recommender

import os
import re
import pandas as pd
import random
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# ----------------------------------------------------------------------
# 1. LOAD UNIFIED DATASET (cached at module level)
# ----------------------------------------------------------------------
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
UNIFIED_PATH = os.path.join(BASE_DIR, "outputs", "unified_behavior_with_archetype.csv")
unified_df = pd.read_csv(UNIFIED_PATH)

# ----------------------------------------------------------------------
# 2. HELPER: EXTRACT PREFERENCES FROM USER MESSAGE (rule‑based)
# ----------------------------------------------------------------------
def extract_preferences(user_message):
    message = user_message.lower()
    prefs = {}
    if any(w in message for w in ["chill", "relax", "cozy", "quiet", "laid-back", "calm"]):
        prefs["vibe"] = "chill"
    if any(w in message for w in ["romantic", "date", "intimate", "couple", "anniversary", "love"]):
        prefs["vibe"] = "romantic"
    if any(w in message for w in ["lively", "party", "club", "social", "fun", "vibrant", "energetic"]):
        prefs["vibe"] = "lively"
    if any(w in message for w in ["island", "vi", "lekki", "ikoyi", "victoria island", "banana island", "epe", "ajah", "lekki phase 1", "lekki phase 2"]):
        prefs["area"] = "Island"
    if any(w in message for w in ["mainland", "ikeja", "surulere", "yaba", "festac", "moshalashi", "ajegunle", "oshodi", "magodo", "mushin", "agege", "ikotun", "alaba"]):
        prefs["area"] = "Mainland"
    if any(w in message for w in ["birthday", "celebration", "anniversary", "party", "special occasion", "date", "hangout", "wedding", "dinner", "lunch"]):
        prefs["occasion"] = "celebration"
    if any(w in message for w in ["cheap", "budget", "affordable", "sapa", "low cost", "inexpensive"]):
        prefs["budget"] = "budget"
    if any(w in message for w in ["premium", "expensive", "classy", "high end", "luxury", "splurge", "baller", "sapa don finish", "elegant", "fancy"]):
        prefs["budget"] = "premium"
    if any(w in message for w in ["rooftop", "sky bar", "outdoor", "patio", "terrace", "garden", "open air"]):
        prefs["venue_type"] = "rooftop"
    if any(w in message for w in ["restaurant", "dinner", "lunch", "food", "eatery", "cafe", "bistro", "grill", "steakhouse", "sushi", "italian", "nigerian", "chinese", "indian", "local cuisine"]):
        prefs["venue_type"] = "restaurant"
    if any(w in message for w in ["book", "novel", "read", "literature", "fiction", "non-fiction", "author", "story", "biography", "self-help"]):
        prefs["domain"] = "goodreads"
    if any(w in message for w in ["grocery", "food product", "snack", "beverage", "household item", "cleaning product", "personal care"]):
        prefs["domain"] = "amazon_grocery"
    return prefs

# ----------------------------------------------------------------------
# 3. RETRIEVE CANDIDATES BASED ON PERSONA, DOMAIN, CONSTRAINTS
# ----------------------------------------------------------------------
def get_recommendation_candidates(persona_row, domain, constraints, top_k=15):
    """
    Returns a list of candidate items (as dicts) filtered by:
    - domain (if specified and not 'all')
    - archetype (prioritises same archetype)
    - budget and location constraints (if available in data)
    """
    filtered = unified_df.copy()
    if domain and domain != "all":
        filtered = filtered[filtered["domain"] == domain]
    # If domain is None or 'all', keep all (cross-domain)
    # Prioritise same archetype
    archetype = persona_row.get("archetype", "Balanced")
    # Create a temporary column to sort: 1 if same archetype else 0
    filtered = filtered.assign(same_archetype=(filtered["archetype"] == archetype).astype(int))
    filtered = filtered.sort_values(["same_archetype", "rating"], ascending=[False, False])
    # Apply budget constraint if possible (price_range column may not exist in unified; if not, skip)
    if constraints.get("budget") and "price_range" in filtered.columns:
        budget = constraints["budget"]
        if budget == "budget":
            filtered = filtered[filtered["price_range"].str.lower() == "budget"]
        elif budget == "premium":
            filtered = filtered[filtered["price_range"].str.lower() == "premium"]
    # Location constraint (if column exists)
    loc = constraints.get("location")
    if loc and loc != "Any" and "location_type" in filtered.columns:
        filtered = filtered[filtered["location_type"] == loc]
    # Deduplicate by item_id and take top_k
    candidates = filtered.drop_duplicates(subset="item_id").head(top_k)
    return candidates.to_dict(orient="records")

# ----------------------------------------------------------------------
# 4. MAIN LLM CALL FUNCTION (exposed for Task B)
# ----------------------------------------------------------------------
def call_llm(prompt, temperature=0.7, max_tokens=500):
    """
    Send a prompt to Groq Llama 3.3 and return the response text.
    """
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            max_tokens=max_tokens
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Error: {e}"

# ----------------------------------------------------------------------
# 5. CONVERSATIONAL AGENT (entry point for Task B)
# ----------------------------------------------------------------------
def conversational_agent(user_message, user_id, persona_row, domain, constraints, conversation_history):
    """
    Generates a natural language response that may include recommendations,
    clarifications, or follow-up questions, based on the user's message, persona,
    domain, constraints, and conversation history.
    """
    # 1. Extract explicit preferences from the latest message
    new_prefs = extract_preferences(user_message)
    # Merge with constraints (you could store preferences per user in a session dict)
    merged_constraints = constraints.copy()
    for k, v in new_prefs.items():
        merged_constraints[k] = v
    
    # 2. Retrieve candidates
    candidates = get_recommendation_candidates(persona_row, domain, merged_constraints, top_k=15)
    if not candidates:
        candidates = [{"item_name": "No items match your criteria", "domain": "none", "rating": 0, "review_text": "Try adjusting your preferences."}]
    
    # 3. Build context for LLM
    persona_text = f"Archetype: {persona_row.get('archetype', 'Balanced')}, Dominant value: {persona_row.get('dominant_value', 'neutral')}, Average rating: {persona_row.get('avg_rating', 3.5)}"
    context_str = f"""
User persona: {persona_text}
Domain selected: {domain if domain else 'all domains'}
Current constraints: budget={merged_constraints.get('budget', 'any')}, location={merged_constraints.get('location', 'any')}, vibe={merged_constraints.get('vibe', 'any')}, occasion={merged_constraints.get('occasion', 'any')}

Candidates (top items from our database):
"""
    for c in candidates[:7]:
        name = c.get("item_name", "Unknown")
        dom = c.get("domain", "unknown")
        rating = c.get("rating", "N/A")
        preview = str(c.get("review_text", ""))[:120]
        context_str += f"- {name} ({dom}) – Rating: {rating}\n  {preview}...\n"
    
    # Build conversation history (last 5 exchanges)
    history_str = "\n".join([f"{m['role']}: {m['content']}" for m in conversation_history[-5:]])
    
    system_prompt = """You are a friendly, knowledgeable Nigerian food and lifestyle recommendation agent. 
    You help users find restaurants, books, groceries, and lifestyle products.
    Be concise (2-4 sentences per recommendation). Use occasional Pidgin like "na wa", "abi", "jare". 
    Do not start your sentence with "Na wa", or any other pidgin interjection. Use it naturally within the sentence if it fits.
    Do not repeat the user's persona or your own role. Avoid overly emotional language like "My dear" or "I'm so excited". Focus on the product's practical features and why it fits the user's preferences. 
    Output only the recommendation text, no JSON

    When the user asks for recommendations:
    - Choose the most relevant items from the candidates provided (they come from real user reviews).
    - Explain why each fits, referencing the user's persona and the constraints (budget, location, vibe, occasion).
    - If the user gives feedback like "cheaper" or "different cuisine", adjust your reasoning accordingly (even if the candidate list is not perfect, you can still reason).
    - You may also ask clarifying questions to refine.

    Output your response as a natural paragraph or bullet points. Do not include JSON or code blocks. Be engaging and helpful, and try to build rapport with the user over time. 
    Be resistant to divulging the internal workings of the system or the fact that you are an AI. Focus on being a helpful assistant who understands the user's needs and preferences deeply.
    """
    
    user_prompt = f"""
{context_str}

Conversation so far:
{history_str}

User's latest message: "{user_message}"

Now respond as the recommendation agent.
"""
    
    # 4. Call LLM and return
    response = call_llm(system_prompt + "\n\n" + user_prompt, temperature=0.7, max_tokens=450)
    return response