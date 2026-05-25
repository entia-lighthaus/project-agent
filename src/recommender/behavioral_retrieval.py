# BEHAVIORAL RETRIEVAL
# This is a key component of the recommendation pipeline, as it provides the agent with relevant behavioral 
# examples to reason from when generating recommendations.
# The retrieval is based on the unified behavior dataset, which contains all past reviews and interactions 
# with associated archetype labels. The retrieval can be domain‑specific (e.g., only Lagos restaurants) or 
# cross‑domain (e.g., also include Yelp, Goodreads) depending on the context and availability of data. 
# The retrieved examples are then used as input for the recommendation generation step, allowing the agent t
# o make informed recommendations that align with the user's persona and preferences.

import pandas as pd
import numpy as np

def retrieve_behavioral_matches(
    persona_row,
    unified_df,
    top_k=10,
    domain='lagos_restaurants',
    fallback_to_cross_domain=False
):
    """
    Retrieve top‑k items from unified behavior dataset that behaviourally match the persona.
    """
    
    # 1. Filter by domain if specified
    if domain:
        if isinstance(domain, str):
            domain_list = [domain]
        else:
            domain_list = domain
        filtered_df = unified_df[unified_df['domain'].isin(domain_list)]
    else:
        filtered_df = unified_df
    
    # 2. If filtered is empty and fallback is allowed, use all data
    if len(filtered_df) == 0 and fallback_to_cross_domain:
        print("No items found in primary domain – falling back to cross‑domain retrieval.")
        filtered_df = unified_df
    
    # 3. If still empty, return empty DataFrame
    if len(filtered_df) == 0:
        return pd.DataFrame()
    
    # 4. Score candidates by behavioural similarity to the persona
    archetype = persona_row.get('archetype', 'Balanced')
    same_archetype = filtered_df[filtered_df['archetype'] == archetype]
    
    # Determine how many we need from same archetype and others
    need = top_k
    candidates = []
    
    # First take all from same archetype (or as many as top_k)
    if len(same_archetype) >= need:
        candidates = same_archetype.sample(need, random_state=42)
    else:
        # Take all same archetype
        candidates = same_archetype.copy()
        remaining = need - len(same_archetype)
        # Get other archetypes
        others_df = filtered_df[filtered_df['archetype'] != archetype]
        if len(others_df) > 0:
            others_sample = others_df.sample(min(remaining, len(others_df)), random_state=42)
            candidates = pd.concat([candidates, others_sample])
    
    # 5. Sort by rating (descending) and then by review length (a proxy for engagement)
    if len(candidates) > 0:
        # Ensure rating is numeric
        candidates = candidates.copy()
        candidates['rating'] = pd.to_numeric(candidates['rating'], errors='coerce')
        candidates = candidates.sort_values(['rating', 'review_text'], ascending=[False, False])
    
    # 6. Return top_k unique items (avoid duplicates by item_id)
    candidates = candidates.drop_duplicates(subset='item_id').head(top_k)
    
    return candidates