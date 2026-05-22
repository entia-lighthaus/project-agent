# COGNITIVE TRADEOFF SIMULATION
# This module contains functions for simulating cognitive tradeoffs that the user might experience when making decisions about their dining experience.
# The simulation considers factors such as price sensitivity, emotionality, social context, and user archetype to generate insights about how the user 
# might balance different considerations and how this could impact their review and overall experience. 
# This helps the system provide more nuanced and human-like explanations and recommendations.


def simulate_cognitive_tradeoffs(
    persona_row,
    business_row,
    context_name
):

    tradeoffs = []

    # PRICE VS EXPERIENCE

    price_sensitivity = persona_row.get(
        "price_sensitivity",
        0
    )

    emotionality = persona_row.get(
        "emotionality_score",
        0
    )

    price_level = business_row.get(
        "price_level",
        2
    )

    if (
        price_sensitivity > 0.7
        and emotionality > 0.7
        and price_level >= 3
    ):

        tradeoffs.append(

            "The user normally dislikes "
            "high pricing, but emotional "
            "excitement may override "
            "budget concerns."
        )


    # SOCIAL CONTEXT

    if context_name == "celebration":

        tradeoffs.append(

            "Celebration contexts increase "
            "tolerance for premium experiences."
        )


    # ANALYTICAL VS EMOTIONAL

    archetype = persona_row.get(
        "archetype",
        ""
    )

    if archetype == "Deep Experience Analyst":

        tradeoffs.append(

            "The user is balancing "
            "emotional enjoyment with "
            "careful evaluation."
        )

    return tradeoffs

#=====================================
# OTHER TRADEOFFS TO SIMULATE
# - Convenience vs Quality
# - Novelty vs Familiarity
# - Social Approval vs Personal Preference

# TODO: Expand function to simulate more complex and varied cognitive tradeoffs 
# based on additional persona and context factors, and to generate more detailed insights 
# about how these tradeoffs might influence the user's review and experience.

#"social_night_out"
# "weekday_quick_meal"
# "comfort_food_mood"
# "solo_reflection"
# "stress_eating"
# "date_night"
# "family_outing"


# 1. FULL ARCHETYPE MODALITIES

# Currently: "Deep Experience Analyst"

# Eventually we add:

# Warm Optimist
# Harsh Critic
# Reactive Reviewer
# Emotional Storyteller

# Each should reason differently.

# 2. MEMORY-CONDITIONED REASONING

# Later: if user previously disliked expensive venues → lower tolerance threshold.
# This becomes adaptive cognition.

