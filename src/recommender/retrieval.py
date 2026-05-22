# This module contains functions for retrieving candidate businesses based on the user's persona and preferences, which can then be used for generating reviews and explanations.
# The retrieval process considers factors such as the user's preferred category, price sensitivity, and emotionality, as well as the business's category, price level, and popularity, 
# to generate a list of potential matches that align with the user's profile and context. This helps the system provide more personalized and relevant recommendations and explanations.

import pandas as pd


# CATEGORY MATCHING

def retrieve_candidates(
    persona_row,
    business_df,
    top_n=20
):

    favorite_category = None

    if "preferred_category" in persona_row:

        favorite_category = (
            persona_row[
                "preferred_category"
            ]
        )

    # CATEGORY FILTERING

    if (
        favorite_category is not None
        and "category_group" in business_df.columns
    ):

        filtered_df = business_df[
            business_df[
                "category_group"
            ] == favorite_category
        ]

    else:

        filtered_df = business_df.copy()

    # QUALITY FILTER

    if "stars" in filtered_df.columns:

        filtered_df = filtered_df[
            filtered_df["stars"] >= 3
        ]

    # SORT BY POPULARITY

    if "review_count" in filtered_df.columns:

        filtered_df = filtered_df.sort_values(
            by="review_count",
            ascending=False
        )

    return filtered_df.head(top_n)