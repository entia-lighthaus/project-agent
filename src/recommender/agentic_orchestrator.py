# AGENTIC ORCHESTRATOR
# This module orchestrates the entire agentic recommendation pipeline, integrating multi-agent reasoning, counterfactual generation, behavioral retrieval, and recommendation generation. 
# It also manages the recommendation memory to maintain conversational continuity across user interactions.

# AGENTIC ORCHESTRATOR
# Unified pipeline for Task A (review simulation) and Task B (contextual, conversational recommendation).

import os
import pandas as pd
import numpy as np
from datetime import datetime

from src.reasoning.multi_agent_reasoning import run_multi_agent_debate
from src.reasoning.counterfactuals import generate_counterfactuals
from src.recommender.behavioral_retrieval import retrieve_behavioral_matches
from src.recommender.recommendation_generation import generate_conversational_recommendations
from src.recommender.recommendation_memory import store_recommendation_interaction, build_multiturn_context

# Optional cross‑domain similarity (if not available, fallback)
# Optional cross‑domain similarity (skip if not installed)
try:
    from sentence_transformers import SentenceTransformer
    from sklearn.metrics.pairwise import cosine_similarity
    EMBEDDING_MODEL = SentenceTransformer('all-MiniLM-L6-v2')
    SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:
    SentenceTransformer = None
    cosine_similarity = None
    EMBEDDING_MODEL = None
    SENTENCE_TRANSFORMERS_AVAILABLE = False
    print("Info: sentence_transformers not installed. Cross-domain features disabled.")


def simulate_user_review(persona_row, target_item, unified_behavior_df, context_name="general", llm_call_func=None, api_key=None):
    """
    Task A: Generate a simulated star rating and review text for a target item.
    This function centralises the logic that was previously in task_a.py.
    
    Args:
        persona_row (dict): User persona (archetype, dominant_value, avg_rating, etc.)
        target_item (dict): Metadata of the item to review (name, category, price_range, description)
        unified_behavior_df (pd.DataFrame): All past reviews with archetype labels.
        context_name (str): e.g., "celebration", "sapa_budget", "general"
        llm_call_func (callable): Function that takes (prompt, api_key) and returns LLM output.
        api_key (str): Groq API key.
    
    Returns:
        dict: {'rating': int, 'review_text': str}
    """
    if llm_call_func is None:
        raise ValueError("llm_call_func required for review simulation")
    
    # Retrieve few‑shot examples from same archetype (fallback to all if none)
    archetype = persona_row.get("archetype", "Balanced")
    archetype_reviews = unified_behavior_df[unified_behavior_df["archetype"] == archetype]
    if len(archetype_reviews) < 3:
        archetype_reviews = unified_behavior_df  # fallback
    
    # Sample 5 reviews (or fewer)
    n_samples = min(5, len(archetype_reviews))
    few_shots = archetype_reviews.sample(n_samples, random_state=42)
    examples = []
    for _, row in few_shots.iterrows():
        examples.append({
            "rating": row["rating"],
            "review_text": row["review_text"][:200]
        })
    
    # Build prompt (reusing logic from task_a.py but parameterised)
    avg_rating = persona_row.get("avg_rating", 3.5)
    dominant_value = persona_row.get("dominant_value", "neutral")
    context_tones = {
        "celebration": "Excited, generous",
        "sapa_budget": "Price‑sensitive, critical",
        "general": "Balanced and honest"
    }
    tone = context_tones.get(context_name, "Balanced and honest")
    
    prompt = f"""You are simulating a Nigerian user on a review platform.

**User Persona:**
- Archetype: {archetype}
- Dominant value: {dominant_value}
- User's historical average rating: {avg_rating:.1f} stars. Keep your rating close to this unless the item is exceptionally good or bad.
- Current context: {context_name} → {tone}

**Few-shot examples of this user's past reviews:**
"""
    for i, ex in enumerate(examples, 1):
        prompt += f"{i}. Rating: {ex['rating']} stars\n   Review: {ex['review_text']}\n"
    
    prompt += f"""
**Now write a NEW review for this item:**
Name: {target_item.get('name', 'Unknown')}
Category: {target_item.get('category', 'General')}
Price range: {target_item.get('price_range', 'moderate')}
Location: {target_item.get('location_type', 'Lagos')}
Description: {target_item.get('description', 'No description')}

**Output exactly in this format:**
Rating: (1-5 integer)
Review: (natural language review in the user's voice, 50-150 words. Write in a mix of standard English and occasional Nigerian Pidgin – code‑switching. Include at least one specific detail.)

Do not add any extra text.
"""
    output = llm_call_func(prompt, api_key)
    if not output:
        return {"rating": 3, "review_text": "Failed to generate review."}
    
    # Parse rating and review
    rating = 3
    review = "Could not parse."
    lines = output.strip().split("\n")
    for line in lines:
        if line.lower().startswith("rating:"):
            try:
                rating = int(line.split(":", 1)[1].strip())
                rating = max(1, min(5, rating))
            except:
                rating = 3
        elif line.lower().startswith("review:"):
            review = line.split(":", 1)[1].strip()
    return {"rating": rating, "review_text": review}


def run_agentic_recommendation_pipeline(
    persona_row,
    business_row,
    unified_behavior_df,
    context_name="social_night_out",
    user_id="user_001",
    additional_context=None   # new: dict with time_of_day, is_weekend, is_month_end, location_preference
):
    """
    Task B: Full agentic recommendation pipeline with contextual signals.
    
    Args:
        additional_context (dict): e.g., {"time_of_day": "evening", "is_month_end": True, "location_preference": "Island"}
    """
    if additional_context is None:
        additional_context = {}
    
    # 1. Multiturn memory
    memory_context = build_multiturn_context(user_id)
    
    # 2. Multi-agent reasoning (can be enhanced with context)
    debate_output = run_multi_agent_debate(persona_row, business_row, context_name)
    
    # 3. Counterfactual reasoning (use predicted rating from debate if available)
    pred_rating = debate_output.get("final_decision_rating", 4)  # fallback
    counterfactuals = generate_counterfactuals(
        persona_row=persona_row,
        business_row=business_row,
        context_name=context_name,
        predicted_rating=pred_rating
    )
    
    # 4. Behavioral retrieval with context filtering
    retrieval_results = retrieve_behavioral_matches(
        persona_row,
        unified_behavior_df,
        top_k=10
    )
    
    # Apply context filters to retrieval results (if available)
    if isinstance(retrieval_results, pd.DataFrame) and len(retrieval_results) > 0:
        # Filter by location preference
        loc_pref = additional_context.get("location_preference")
        if loc_pref and loc_pref != "No preference" and "location_type" in retrieval_results.columns:
            retrieval_results = retrieval_results[retrieval_results["location_type"] == loc_pref]
        
        # Filter by budget mode (month-end)
        if additional_context.get("is_month_end", False) and "price_range" in retrieval_results.columns:
            retrieval_results = retrieval_results[retrieval_results["price_range"] == "Budget"]
        
        # If empty after filtering, fallback to original
        if len(retrieval_results) == 0:
            retrieval_results = retrieve_behavioral_matches(persona_row, unified_behavior_df, top_k=10)
    
    # 5. Generate conversational recommendations (pass context for LLM ranking)
    recommendations = generate_conversational_recommendations(
        persona_row,
        retrieval_results,
        top_k=5,
        context_info=additional_context   # pass to recommendation generation
    )
    
    # 6. Store memory
    for rec in recommendations:
        store_recommendation_interaction(user_id, rec)
    
    # Return unified dictionary (compatible with both tasks)
    return {
        "memory_context": memory_context,
        "debate_output": debate_output,
        "counterfactuals": counterfactuals,
        "recommendations": recommendations,
        "additional_context": additional_context   # for transparency
    }