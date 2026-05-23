# STORE USER RECOMMENDATION HISTORY
# This module provides functions to store and retrieve user interactions with recommendations, 
# enabling a more personalized and context-aware recommendation experience over time.
# It maintains a memory of user interactions, allowing the system to build a multi-turn context for future recommendations.
# This is conversational continuity.

recommendation_memory = {}


def store_recommendation_interaction(

    user_id,

    recommendation
):

    if user_id not in recommendation_memory:

        recommendation_memory[user_id] = []

    recommendation_memory[user_id].append(
        recommendation
    )


def retrieve_recommendation_history(
    user_id
):

    return recommendation_memory.get(
        user_id,
        []
    )


def build_multiturn_context(
    user_id
):

    history = (
        retrieve_recommendation_history(
            user_id
        )
    )

    if len(history) == 0:

        return "No prior recommendation history."

    domains = [

        item["domain"]

        for item in history
    ]

    return f"""
    User previously interacted with:
    {domains}
    """