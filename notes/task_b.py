import sys
import os   
import streamlit as st
import pandas as pd
import sys


sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "../.."
        )
    )
)

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from src.recommender.agentic_orchestrator import (
    run_agentic_recommendation_pipeline
)


st.title(
    "Task B — Agentic Recommendation Engine"
)


# LOAD DATA
def load_data():
    persona_df = pd.read_csv(os.path.join(PROJECT_ROOT, "outputs", "persona_dataset_full.csv"))
    unified_df = pd.read_csv(os.path.join(PROJECT_ROOT, "outputs", "unified_behavior_with_archetype.csv"))
    lagos_df = pd.read_csv(os.path.join(PROJECT_ROOT, "data", "external", "lagos_restaurants_metadata.csv"))
    return persona_df, unified_df, lagos_df

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