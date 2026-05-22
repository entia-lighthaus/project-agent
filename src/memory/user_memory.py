# User Memory Management
# This module manages the user memory, which includes:
# - Storing user interactions
# - Retrieving relevant past interactions for context
# - Updating memory with new interactions


from collections import defaultdict


# CREATE EMPTY MEMORY

def initialize_user_memory():

    memory = {

        "favorite_categories": defaultdict(int),

        "disliked_categories": defaultdict(int),

        "recent_ratings": [],

        "recent_emotions": [],

        "recent_contexts": [],

        "price_sentiment_history": [],

        "interaction_count": 0
    }

    return memory


# UPDATE MEMORY AFTER REVIEW

def update_user_memory(
    memory,
    business_row,
    predicted_rating,
    context_name,
    emotional_tone
):

    category = business_row.get(
        "category_group",
        "unknown"
    )

    memory["interaction_count"] += 1

    memory["recent_ratings"].append(
        predicted_rating
    )

    memory["recent_contexts"].append(
        context_name
    )

    memory["recent_emotions"].append(
        emotional_tone
    )

    # FAVORITES

    if predicted_rating >= 4:

        memory["favorite_categories"][
            category
        ] += 1

    # DISLIKES

    if predicted_rating <= 2:

        memory["disliked_categories"][
            category
        ] += 1

    # PRICE EXPERIENCE MEMORY

    if "price_level" in business_row:

        memory[
            "price_sentiment_history"
        ].append(

            (
                business_row["price_level"],
                predicted_rating
            )
        )

    return memory


# EMOTIONAL DRIFT

def infer_emotional_state(
    memory
):

    recent_ratings = (
        memory["recent_ratings"][-5:]
    )

    if len(recent_ratings) == 0:
        return "neutral"

    avg_recent_rating = (
        sum(recent_ratings)
        / len(recent_ratings)
    )

    if avg_recent_rating >= 4:
        return "positive"

    if avg_recent_rating <= 2.5:
        return "frustrated"

    return "mixed"


# MEMORY SUMMARY

def summarize_memory(memory):

    favorite_categories = sorted(

        memory[
            "favorite_categories"
        ].items(),

        key=lambda x: x[1],

        reverse=True
    )

    disliked_categories = sorted(

        memory[
            "disliked_categories"
        ].items(),

        key=lambda x: x[1],

        reverse=True
    )

    summary = {

        "top_favorites":
            favorite_categories[:3],

        "top_dislikes":
            disliked_categories[:3],

        "interaction_count":
            memory["interaction_count"],

        "current_emotional_state":
            infer_emotional_state(
                memory
            )
    }

    return summary