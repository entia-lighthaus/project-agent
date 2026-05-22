# VALUE COMPATIBILITY
# This function evaluates how well a business aligns with a persona's values and preferences, such as price sensitivity.
# For example, a user with high price sensitivity would find a business with a lower price level more compatible, while a user with low price sensitivity might not be as affected by the price level.


def compute_value_compatibility(
    persona_row,
    business_row
):

    score = 0

    price_sensitivity = persona_row.get(
        "price_sensitivity",
        0
    )

    price_level = business_row.get(
        "price_level",
        2
    )

    # AFFORDABILITY MATCH

    if (
        price_sensitivity > 0.7
        and price_level <= 2
    ):

        score += 2

    elif (
        price_sensitivity > 0.7
        and price_level >= 4
    ):

        score -= 2

    else:

        score += 1

    return score


# CONTEXT COMPATIBILITY
# This function evaluates how well a business fits the current context or occasion. 
# For example, a restaurant might be more compatible for a "celebration" context, while a coffee shop might be more compatible for a "work" context.

def compute_context_compatibility(
    context_name,
    business_row
):

    score = 0

    category = business_row.get(
        "category_group",
        ""
    )

    if (
        context_name == "celebration"
        and category == "Restaurants"
    ):

        score += 2

    if (
        context_name == "comfort_food_mood"
        and category == "Food"
    ):

        score += 2

    return score


# ARCHETYPE COMPATIBILITY
# This function evaluates how well a business aligns with a persona's archetype.
# For example, a "Warm Optimist" might prefer highly rated businesses, while a "Harsh Critic" might be more critical of lower-rated businesses. 
# A "Deep Experience Analyst" might appreciate highly rated businesses but also consider other factors.

def compute_archetype_compatibility(
    persona_row,
    business_row
):

    score = 0

    archetype = persona_row.get(
        "archetype",
        ""
    )

    stars = business_row.get(
        "stars",
        3
    )

    if (
        archetype == "Warm Optimist"
        and stars >= 4
    ):

        score += 2

    if (
        archetype == "Harsh Critic"
        and stars < 4
    ):

        score -= 2

    if (
        archetype == "Deep Experience Analyst"
        and stars >= 4
    ):

        score += 1

    return score


# MEMORY COMPATIBILITY
# This function evaluates how well a business aligns with the user's past preferences and dislikes stored in memory. 
# For example, if a user has a history of favoring certain categories, businesses in those categories would score higher, while businesses in categories they've disliked would score lower.

def compute_memory_compatibility(
    memory,
    business_row
):

    score = 0

    category = business_row.get(
        "category_group",
        ""
    )

    favorites = memory.get(
        "favorite_categories",
        {}
    )

    dislikes = memory.get(
        "disliked_categories",
        {}
    )

    if category in favorites:
        score += favorites[category]

    if category in dislikes:
        score -= dislikes[category]

    return score


# FINAL COMPATIBILITY SCORE

def compute_total_compatibility(
    persona_row,
    business_row,
    memory,
    context_name
):

    value_score = (
        compute_value_compatibility(
            persona_row,
            business_row
        )
    )

    context_score = (
        compute_context_compatibility(
            context_name,
            business_row
        )
    )

    archetype_score = (
        compute_archetype_compatibility(
            persona_row,
            business_row
        )
    )

    memory_score = (
        compute_memory_compatibility(
            memory,
            business_row
        )
    )

    total_score = (

        value_score
        + context_score
        + archetype_score
        + memory_score
    )

    return {

        "total_score":
            total_score,

        "component_scores": {

            "value_score":
                value_score,

            "context_score":
                context_score,

            "archetype_score":
                archetype_score,

            "memory_score":
                memory_score
        }
    }