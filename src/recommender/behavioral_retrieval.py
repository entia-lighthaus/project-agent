# BEHAVIORAL RETRIEVAL
# This is a key component of the recommendation pipeline, as it provides the agent with relevant behavioral 
# examples to reason from when generating recommendations.
# The retrieval is based on the unified behavior dataset, which contains all past reviews and interactions 
# with associated archetype labels. The retrieval can be domain‑specific (e.g., only Lagos restaurants) or 
# cross‑domain (e.g., also include Yelp, Goodreads) depending on the context and availability of data. 
# The retrieved examples are then used as input for the recommendation generation step, allowing the agent to
# make informed recommendations that align with the user's persona and preferences.

import pandas as pd
import numpy as np
from scipy.sparse import csr_matrix 
from sklearn.metrics.pairwise import cosine_similarity

# this function is useful for extensions where we want to compute similarity
def build_user_item_matrix(df):
    """
    Create a sparse user‑item matrix from a DataFrame with columns:
    user_id, item_id, rating.
    
    Returns:
        matrix (csr_matrix): shape (n_users, n_items)
        user_to_idx (dict): maps user_id -> row index
        item_to_idx (dict): maps item_id -> column index
    """
    # Get unique users and items
    users = df['user_id'].unique()
    items = df['item_id'].unique()
    
    # Create mapping dictionaries
    user_to_idx = {u: i for i, u in enumerate(users)}
    item_to_idx = {i: j for j, i in enumerate(items)}
    
    # Create arrays for sparse matrix construction
    row_indices = df['user_id'].map(user_to_idx).values
    col_indices = df['item_id'].map(item_to_idx).values
    values = df['rating'].values
    
    # Build sparse matrix
    matrix = csr_matrix((values, (row_indices, col_indices)),
                        shape=(len(users), len(items)))
    
    return matrix, user_to_idx, item_to_idx





def recommend_by_user_similarity(user_id, matrix, user_to_idx, item_to_idx, top_k=10):
    """
    Recommend items for a given user based on similar users.
    
    Returns: list of item IDs recommended.
    """
    # Get the user's row index
    if user_id not in user_to_idx:
        return []
    user_idx = user_to_idx[user_id]
    
    # Compute cosine similarity between all users (sparse)
    # This returns a dense matrix of shape (n_users, n_users)
    similarity_matrix = cosine_similarity(matrix)
    
    # Get similarity scores for the target user
    user_sim = similarity_matrix[user_idx]
    
    # Find indices of most similar users (excluding self)
    similar_users_idx = user_sim.argsort()[::-1][1:6]   # top 5 similar
    
    # Items already rated by target user
    rated_items = set(matrix[user_idx].indices)
    
    # Accumulate scores for candidate items
    candidate_scores = {}
    for sim_idx in similar_users_idx:
        sim_rated = matrix[sim_idx].indices       # items rated by similar user
        sim_ratings = matrix[sim_idx].data        # corresponding ratings
        for item_pos, rating in zip(sim_rated, sim_ratings):
            if item_pos not in rated_items and rating >= 4:   # threshold
                # Add the rating as a score (could also weight by similarity)
                candidate_scores[item_pos] = candidate_scores.get(item_pos, 0) + rating
    
    # Sort candidates by total score and pick top_k
    top_items = sorted(candidate_scores.items(), key=lambda x: x[1], reverse=True)[:top_k]
    
    # Convert back to original item IDs
    reverse_item_idx = {v: k for k, v in item_to_idx.items()}
    recommendations = [reverse_item_idx[pos] for pos, _ in top_items]
    return recommendations




def retrieve_behavioral_matches(persona_row, unified_df, top_k=10, domain='lagos_restaurants',
                                use_cosine=True):
    # 1. Filter by domain
    filtered = unified_df[unified_df['domain'] == domain].copy()
    if len(filtered) == 0:
        return pd.DataFrame()
    
    # 2. Try cosine similarity (if user_id is present)
    user_id = persona_row.get('user_id')
    if use_cosine and user_id:
        # Build matrix only once? For speed, we can build globally and cache.
        matrix, user_map, item_map = build_user_item_matrix(filtered)
        cos_rec_ids = recommend_by_user_similarity(user_id, matrix, user_map, item_map, top_k)
        if cos_rec_ids:
            # Get full rows for recommended items
            cos_recs = filtered[filtered['item_id'].isin(cos_rec_ids)]
            if len(cos_recs) >= top_k:
                return cos_recs.head(top_k)
    
    # 3. Fallback to archetype‑based retrieval (existing logic)
    archetype = persona_row.get('archetype', 'Balanced')
    same_archetype = filtered[filtered['archetype'] == archetype]
    if len(same_archetype) < top_k:
        # Add other archetypes to fill
        others = filtered[filtered['archetype'] != archetype].sample(min(top_k - len(same_archetype), 
                                                                        len(filtered[filtered['archetype'] != archetype])))
        candidates = pd.concat([same_archetype, others])
    else:
        candidates = same_archetype
    candidates = candidates.sort_values('rating', ascending=False).drop_duplicates('item_id').head(top_k)
    return candidates