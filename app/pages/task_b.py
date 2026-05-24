# TASK B: AGENTIC RECOMMENDATION ENGINE
# This page implements Task B, which focuses on generating agentic recommendations based on user personas and selected contexts. 
# It allows users to select a persona archetype and a recommendation context, and then generates a set of recommendations that align with the selected persona and context. 
# This demonstrates the system's ability to create personalized and context-aware recommendations, which is a crucial component of the overall agentic recommendation system.   

import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "../.."
        )
    )
)

import streamlit as st
import pandas as pd
import sys
import os


sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "../.."
        )
    )
)


from src.recommender.agentic_orchestrator import (
    run_agentic_recommendation_pipeline
)


st.title(
    "Task B — Agentic Recommendation Engine"
)


# LOAD DATA

persona_df = pd.read_csv(
    "../outputs/persona_dataset.csv"
)

lagos_df = pd.read_csv(
    "../data/external/clean_lagos_restaurants.csv"
)

unified_behavior_df = pd.read_csv(
    "../outputs/unified_behavior_dataset.csv"
)


# CONTEXTS

contexts = [

    "celebration",

    "comfort_food_mood",

    "social_night_out",

    "weekday_quick_meal"
]


# PERSONA SELECTOR

selected_archetype = st.selectbox(

    "Select Persona Archetype",

    persona_df["archetype"].unique()
)


# CONTEXT SELECTOR

selected_context = st.selectbox(

    "Select Recommendation Context",

    contexts
)


# BUTTON

if st.button(
    "Generate Personalized Recommendations"
):

    sampled_persona = (

        persona_df[
            persona_df["archetype"]
            ==
            selected_archetype
        ]

        .sample(1)

        .iloc[0]
    )

    sampled_business = (

        lagos_df
        .sample(1)
        .iloc[0]
    )


    output = (
        run_agentic_recommendation_pipeline(

            persona_row=sampled_persona,

            business_row=sampled_business,

            unified_behavior_df=unified_behavior_df,

            context_name=selected_context,

            user_id="streamlit_recommender_user"
        )
    )


    st.subheader(
        "Behavioral Recommendations"
    )

    for recommendation in output[
        "recommendations"
    ]:

        st.markdown("---")

        st.write(
            f"### Domain: {recommendation['domain']}"
        )

        st.write(
            f"Rating: {recommendation['rating']}"
        )

        st.write(
            recommendation[
                "recommendation_preview"
            ]
        )

        st.info(
            recommendation[
                "explanation"
            ]
        )


    st.subheader(
        "Multiturn Recommendation Memory"
    )

    st.write(
        output[
            "memory_context"
        ]
    )

    st.success(
    "Cross-domain recommendation generation completed."
    )