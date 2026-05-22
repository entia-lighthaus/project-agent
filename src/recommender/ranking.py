# RANKING MODULE
# This module is responsible for ranking the candidate businesses based on their compatibility scores with the user's persona and context. 
# It takes the scored candidates and sorts them to produce a ranked list of recommendations.
# The ranking is based on the total compatibility score, which is a combination of value compatibility, context compatibility, archetype compatibility, and memory compatibility.
# The pipeline will: Retrieve candidate businesses, Score each candidate psychologically, Rank them, Return top recommendations, Preserve explainability


import pandas as pd

from src.recommender.compatibility import (
    compute_total_compatibility
)


# RANK CANDIDATES

def rank_recommendations(
    persona_row,
    candidates_df,
    memory,
    context_name
):

    scored_results = []

    for _, business_row in (
        candidates_df.iterrows()
    ):

        compatibility = (
            compute_total_compatibility(

                persona_row,
                business_row,
                memory,
                context_name
            )
        )

        scored_results.append({

            "business_name":
                business_row.get(
                    "name",
                    "Unknown"
                ),

            "category":
                business_row.get(
                    "category_group",
                    "Unknown"
                ),

            "stars":
                business_row.get(
                    "stars",
                    0
                ),

            "review_count":
                business_row.get(
                    "review_count",
                    0
                ),

            "compatibility_score":
                compatibility[
                    "total_score"
                ],

            "component_scores":
                compatibility[
                    "component_scores"
                ]
        })

    ranked_df = pd.DataFrame(
        scored_results
    )

    ranked_df = ranked_df.sort_values(
        by="compatibility_score",
        ascending=False
    )

    return ranked_df