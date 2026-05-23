import pandas as pd


# ARCHETYPE DOMAIN PREFERENCES

ARCHETYPE_DOMAIN_PREFERENCES = {

    "Warm Optimist": [
        "comfort",
        "family",
        "cozy",
        "uplifting",
        "wellness"
    ],

    "Reactive Reviewer": [
        "trendy",
        "viral",
        "social",
        "hype"
    ],

    "Harsh Critic": [
        "premium",
        "quality",
        "authentic",
        "luxury"
    ],

    "Emotional Storyteller": [
        "emotional",
        "nostalgic",
        "beautiful",
        "aesthetic"
    ],

    "Deep Experience Analyst": [
        "detailed",
        "analytical",
        "psychology",
        "educational"
    ]
}


# BUILD SEARCH TEXT

def build_search_text(
    row
):

    text_parts = [

        str(
            row.get(
                "review_text",
                ""
            )
        ),

        str(
            row.get(
                "domain",
                ""
            )
        )
    ]

    return " ".join(
        text_parts
    ).lower()


# RETRIEVE CROSS-DOMAIN MATCHES

def retrieve_behavioral_matches(

    persona_row,

    unified_behavior_df,

    top_k=10
):

    archetype = persona_row.get(
        "archetype",
        "Warm Optimist"
    )

    preference_terms = (
        ARCHETYPE_DOMAIN_PREFERENCES.get(
            archetype,
            []
        )
    )

    df = unified_behavior_df.copy()

    df["search_text"] = (
        df.apply(
            build_search_text,
            axis=1
        )
    )

    df["behavior_score"] = 0

    for term in preference_terms:

        df["behavior_score"] += (
            df["search_text"]
            .str.contains(
                term,
                case=False,
                na=False
            )
            .astype(int)
        )

    ranked_df = (
        df.sort_values(
            "behavior_score",
            ascending=False
        )
    )

    return ranked_df.head(top_k)