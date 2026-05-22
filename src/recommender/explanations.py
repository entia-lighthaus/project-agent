# EXPLANATION MODULE
# This module is responsible for generating conversational explanations for the recommendations provided to the user.
# The explanations are designed to be engaging and informative, providing insights into why a particular business was recommended based on the user's persona, preferences, and current context. 
# The explanations will highlight key compatibility factors such as value alignment, context fit, and emotional state, making the recommendations more transparent and personalized for the user. 
# This helps to enhance the user's trust and satisfaction with the recommendation system by providing clear and relatable reasons for the suggestions made.


# DYNAMIC CONVERSATIONAL EXPLANATIONS

def generate_recommendation_explanation(

    persona_row,

    business_row,

    memory,

    context_name,

    compatibility_result,

    debate_result=None,

    confidence_result=None
):

    archetype = persona_row.get(
        "archetype",
        "User"
    )

    business_name = business_row.get(
        "name",
        "this place"
    )

    category = business_row.get(
        "category_group",
        "experience"
    )

    price_level = business_row.get(
        "price_level",
        2
    )

    score = compatibility_result.get(
        "total_score",
        0
    )

    # MEMORY SIGNALS

    favorites = memory.get(
        "favorite_categories",
        {}
    )

    dislikes = memory.get(
        "disliked_categories",
        {}
    )

    favorite_text = ""

    if category in favorites:

        favorite_text = (
            f"You've consistently responded "
            f"positively to {category.lower()} "
            f"experiences recently. "
        )

    dislike_text = ""

    if category in dislikes:

        dislike_text = (
            f"However, you've also shown "
            f"some mixed reactions toward "
            f"similar experiences recently. "
        )

    # PRICE REASONING

    price_text = ""

    price_sensitivity = persona_row.get(
        "price_sensitivity",
        0
    )

    if (
        price_sensitivity > 0.7
        and price_level >= 4
    ):

        price_text = (
            "The pricing may feel somewhat "
            "expensive based on your "
            "usual preferences. "
        )

    elif (
        price_sensitivity > 0.7
        and price_level <= 2
    ):

        price_text = (
            "This option aligns well with "
            "your preference for affordability. "
        )

    # CONTEXT REASONING

    context_text = ""

    if context_name == "celebration":

        context_text = (
            "Celebration contexts typically "
            "increase your tolerance for "
            "premium experiences. "
        )

    elif context_name == "comfort_food_mood":

        context_text = (
            "Your current mood suggests a "
            "preference for emotionally "
            "comforting experiences. "
        )

    elif context_name == "weekday_quick_meal":

        context_text = (
            "You currently appear to value "
            "convenience and efficiency. "
        )

    # ARCHETYPE REASONING

    archetype_text = ""

    if archetype == "Deep Experience Analyst":

        archetype_text = (
            "You tend to carefully balance "
            "emotional enjoyment with "
            "detailed evaluation. "
        )

    elif archetype == "Warm Optimist":

        archetype_text = (
            "You generally respond positively "
            "to emotionally uplifting experiences. "
        )

    elif archetype == "Harsh Critic":

        archetype_text = (
            "You typically maintain high "
            "standards when evaluating experiences. "
        )

    elif archetype == "Emotional Storyteller":

        archetype_text = (
            "You tend to value memorable "
            "and emotionally resonant experiences. "
        )

    # AGENT DEBATE SIGNALS

    debate_text = ""

    if debate_result is not None:

        decisions = [

            agent["reason"]

            for agent in debate_result[
                "agent_discussions"
            ]
        ]

        if len(decisions) > 0:

            debate_text = (
                "Internal reasoning signals suggest: "
                + " ".join(decisions)
            )

    # CONFIDENCE SIGNALS

    confidence_text = ""

    if confidence_result is not None:

        label = confidence_result.get(
            "confidence_label",
            "moderate"
        )

        confidence_text = (
            f"Recommendation confidence "
            f"is currently {label}. "
        )

    # FINAL RESPONSE

    explanation = f"""

Based on your {archetype} behavioral profile,
{business_name} appears to be a meaningful fit
for your current situation.

{favorite_text}

{dislike_text}

{price_text}

{context_text}

{archetype_text}

{debate_text}

This recommendation achieved a compatibility
score of {score}.

{confidence_text}
"""

    return explanation.strip()