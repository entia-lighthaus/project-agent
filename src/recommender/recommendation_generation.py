# RECOMMENDATION GENERATION MODULE
# This module generates personalized recommendations based on user personas and cross-domain retrieval results. 
# It constructs explanations for each recommendation to enhance user understanding and engagement.

import random


# DOMAIN INTERPRETATIONS

DOMAIN_LABELS = {

    "yelp":
        "restaurant experiences",

    "lagos_restaurants":
        "Nigerian dining experiences",

    "goodreads":
        "books and reading experiences",

    "amazon_grocery":
        "food and grocery products",

    "amazon_home":
        "home and lifestyle products"
}


# BUILD RECOMMENDATION EXPLANATION

def generate_recommendation_explanation(

    persona_row,

    recommendation_row
):

    archetype = persona_row.get(
    "archetype",
    "Warm Optimist"
)

    domain = recommendation_row.get(
        "domain",
        "unknown"
    )

    review_text = str(
        recommendation_row.get(
            "review_text",
            ""
        )
    )[:180]

    domain_label = DOMAIN_LABELS.get(
        domain,
        domain
    )

    explanation_templates = [

        f"As a {archetype}, you may appreciate these {domain_label} because they align with your behavioral preferences and emotional tendencies.",

        f"This recommendation was selected because users with the {archetype} profile often enjoy similar {domain_label}.",

        f"Your interaction style resembles users who positively engage with these {domain_label}.",

        f"This recommendation reflects your inferred emotional and behavioral preferences across domains."
    ]

    explanation = random.choice(
        explanation_templates
    )

    return {

        "domain":
            domain,

        "rating":
            recommendation_row.get(
                "rating",
                None
            ),

        "recommendation_preview":
            review_text,

        "explanation":
            explanation
    }


# GENERATE MULTIPLE RECOMMENDATIONS

def generate_conversational_recommendations(

    persona_row,

    retrieval_results,

    top_k=5
):

    recommendations = []

    sampled_results = retrieval_results.head(
        top_k
    )

    for _, row in sampled_results.iterrows():

        recommendation = (
            generate_recommendation_explanation(

                persona_row,

                row
            )
        )

        recommendations.append(
            recommendation
        )

    return recommendations