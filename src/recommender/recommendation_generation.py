# RECOMMENDATION GENERATION MODULE
# This module generates personalized recommendations based on user personas and cross-domain retrieval results. 
# It constructs explanations for each recommendation to enhance user understanding and engagement.

import random
import json
import pandas as pd
from src.recommender.conversational_agent import call_llm

# DOMAIN INTERPRETATIONS (cross‑domain labels)
DOMAIN_LABELS = {
    "yelp": "restaurant experiences",
    "lagos_restaurants": "Nigerian dining experiences",
    "goodreads": "books and reading experiences",
    "amazon_grocery": "food and grocery products",
    "amazon_home": "home and lifestyle products"
}


def generate_recommendation_explanation(persona_row, recommendation_row, context_info=None):
    """
    Generate a single recommendation with an explanation, optionally influenced by context.
    
    Args:
        persona_row (dict): User persona (archetype, dominant_value, etc.)
        recommendation_row (dict or Series): Item metadata (domain, rating, review_text, etc.)
        context_info (dict, optional): e.g., {"time_of_day": "evening", "is_weekend": True, "is_month_end": True}
    
    Returns:
        dict: Domain, rating, preview, explanation
    """
    archetype = persona_row.get("archetype", "Warm Optimist")
    domain = recommendation_row.get("domain", "unknown")
    item_name = recommendation_row.get("item_name", "Unknown item")   # NEW
    rating = recommendation_row.get("rating", None)
    review_text = str(recommendation_row.get("review_text", ""))[:180]

    domain_label = DOMAIN_LABELS.get(domain, domain)


    # Base explanation templates (Nigerian‑flavoured)
    templates = [
        f"As a {archetype}, you may appreciate these {domain_label} because they align with your behavioral preferences and emotional tendencies.",
        f"This recommendation was selected because users with the {archetype} profile often enjoy similar {domain_label}.",
        f"Your interaction style resembles users who positively engage with these {domain_label}.",
        f"This recommendation reflects your inferred emotional and behavioral preferences across domains."
    ]
    
    # Context‑aware enhancements
    if context_info:
        time = context_info.get("time_of_day", "")
        is_weekend = context_info.get("is_weekend", False)
        is_month_end = context_info.get("is_month_end", False)
        location = context_info.get("location_preference", "")
        
        if is_month_end:
            templates.append(f"Considering month‑end budgeting, this {domain_label} offers good value for money – perfect for managing your sapa.")
        if is_weekend:
            templates.append(f"It's the weekend – this {domain_label} is great for a social night out or relaxed brunch.")
        if time == "morning":
            templates.append(f"Good morning! This {domain_label} is ideal for starting your day with a positive experience.")
        elif time == "evening":
            templates.append(f"Evening vibe check: this {domain_label} has the right ambience for winding down.")
        if location == "Island":
            templates.append(f"Located on the Island, this {domain_label} matches your preference for premium experiences.")
        elif location == "Mainland":
            templates.append(f"Mainland spot – convenient and authentic, just as you like it.")
    
    explanation = random.choice(templates)
    
    return {
        "domain": domain,
        "item_name": item_name,          
        "rating": recommendation_row.get("rating", None),
        "recommendation_preview": review_text,
        "explanation": explanation
    }


def generate_conversational_recommendations(persona_row, retrieval_results, top_k=5, context_info=None):
    """
    Generate a list of recommendations, optionally filtered/re‑ranked by context.
    
    Args:
        persona_row (dict): User persona
        retrieval_results (pd.DataFrame): Candidate items with columns (domain, rating, review_text, price_range, location_type, etc.)
        top_k (int): Number of recommendations to return
        context_info (dict, optional): Contextual signals (time, month‑end, location preference)
    
    Returns:
        list[dict]: Top‑k recommendation objects
    """
    # If retrieval_results is empty, return empty list
    if retrieval_results is None or len(retrieval_results) == 0:
        return []
    
    # Make a copy to avoid modifying original
    candidates = retrieval_results.copy()
    
    # Apply context‑based filtering (if columns exist)
    if context_info:
        # Month‑end: prefer Budget items (if price_range column exists)
        if context_info.get("is_month_end", False) and "price_range" in candidates.columns:
            # Boost Budget items by moving them to top, but keep others as fallback
            budget = candidates[candidates["price_range"] == "Budget"]
            non_budget = candidates[candidates["price_range"] != "Budget"]
            candidates = pd.concat([budget, non_budget]).reset_index(drop=True)
        
        # Weekend: prefer social venues (e.g., "lounge", "bar", "club" – if category column exists)
        if context_info.get("is_weekend", False) and "category" in candidates.columns:
            social_keywords = ["lounge", "bar", "club", "pub", "rooftop"]
            social_mask = candidates["category"].str.lower().apply(lambda x: any(k in str(x) for k in social_keywords))
            social = candidates[social_mask]
            others = candidates[~social_mask]
            candidates = pd.concat([social, others]).reset_index(drop=True)
        
        # Morning: prefer cafes/breakfast spots
        if context_info.get("time_of_day") == "morning" and "category" in candidates.columns:
            morning_keywords = ["cafe", "breakfast", "coffee", "bakery"]
            morning_mask = candidates["category"].str.lower().apply(lambda x: any(k in str(x) for k in morning_keywords))
            morning_items = candidates[morning_mask]
            others = candidates[~morning_mask]
            candidates = pd.concat([morning_items, others]).reset_index(drop=True)
        
        # Location preference (Island/Mainland)
        if "location_type" in candidates.columns:
            loc = context_info.get("location_preference")
            if loc and loc != "No preference":
                preferred = candidates[candidates["location_type"] == loc]
                other = candidates[candidates["location_type"] != loc]
                candidates = pd.concat([preferred, other]).reset_index(drop=True)
    
    # Take top_k after reordering
    sampled = candidates.head(top_k)
    
    recommendations = []
    for _, row in sampled.iterrows():
        rec = generate_recommendation_explanation(persona_row, row.to_dict(), context_info)
        recommendations.append(rec)
    
    return recommendations