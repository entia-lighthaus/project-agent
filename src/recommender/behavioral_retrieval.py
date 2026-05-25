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
    domain='lagos_restaurants',      # NEW: restrict to a specific domain
    fallback_to_cross_domain=False   # NEW: if no matches, use other domains
):
    """
    Retrieve top‑k items from unified behavior dataset that behaviourally match the persona.
    
    Args:
        persona_row (dict): Contains 'archetype', 'dominant_value', etc.
        unified_df (pd.DataFrame): Must have columns: 'user_id', 'item_id', 'rating', 'review_text', 'domain', 'archetype', ...
        top_k (int): Number of items to return.
        domain (str or list): Restrict to one or more domains (e.g., 'lagos_restaurants', 'yelp', 'goodreads').
        fallback_to_cross_domain (bool): If True and no items found in primary domain, retrieve from all domains.
    
    Returns:
        pd.DataFrame: Top‑k matched items (with all columns).
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
    #    Here we use a simple heuristic: boost items that were rated highly by users of the same archetype.
    #    More advanced: collaborative filtering scores.
    archetype = persona_row.get('archetype', 'Balanced')
    same_archetype = filtered_df[filtered_df['archetype'] == archetype]
    
    if len(same_archetype) >= top_k:
        candidates = same_archetype
    else:
        # Combine same archetype + others (but give weight to same archetype)
        others = filtered_df[filtered_df['archetype'] != archetype].sample(min(top_k - len(same_archetype), len(others)))
        candidates = pd.concat([same_archetype, others])
    
    # 5. Sort by rating (descending) and then by review length (a proxy for engagement)
    candidates = candidates.sort_values(['rating', 'review_text'], ascending=[False, False])
    
    # 6. Return top_k unique items (avoid duplicates by item_id)
    candidates = candidates.drop_duplicates(subset='item_id').head(top_k)
    
    return candidates