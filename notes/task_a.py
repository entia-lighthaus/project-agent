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
import random

from src.recommender.agentic_orchestrator import (
    run_agentic_recommendation_pipeline
)


st.title(
    "Task A — Agentic Review Generation"
)


# LOAD PERSONAS

persona_df = pd.read_csv(
    "../outputs/persona_dataset.csv"
)


# LOAD LAGOS DATA

lagos_df = pd.read_csv(
    "../data/external/clean_lagos_restaurants.csv"
)


# LOAD UNIFIED DATA

unified_behavior_df = pd.read_csv(
    "../outputs/unified_behavior_dataset.csv"
)


# CONTEXT OPTIONS

contexts = [

    "celebration",

    "social_night_out",

    "weekday_quick_meal",

    "comfort_food_mood"
]


# PERSONA SELECTOR

selected_archetype = st.selectbox(

    "Select Persona Archetype",

    persona_df["archetype"].unique()
)


# CONTEXT SELECTOR

selected_context = st.selectbox(

    "Select Context",

    contexts
)


# GENERATE BUTTON

if st.button(
    "Generate Agentic Experience"
):

    # SAMPLE PERSONA

    sampled_persona = (

        persona_df[
            persona_df["archetype"]
            ==
            selected_archetype
        ]

        .sample(1)

        .iloc[0]
    )

    # SAMPLE BUSINESS

    sampled_business = (

        lagos_df
        .sample(1)
        .iloc[0]
    )

    # RUN PIPELINE

    output = (
        run_agentic_recommendation_pipeline(

            persona_row=sampled_persona,

            business_row=sampled_business,

            unified_behavior_df=unified_behavior_df,

            context_name=selected_context,

            user_id="streamlit_user"
        )
    )

    # DISPLAY RESULTS

    st.subheader(
        "Multi-Agent Debate"
    )

    st.json(
        output["debate_output"]
    )


    st.subheader(
        "Counterfactual Reasoning"
    )

    st.json(
        output["counterfactuals"]
    )


    st.subheader(
        "Recommendations"
    )

    for recommendation in output[
        "recommendations"
    ]:

        st.markdown("---")

        st.write(
            f"### Domain: {recommendation['domain']}"
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
        "Conversation Memory"
    )

    st.write(
        output["memory_context"]
    )

    st.success(
    "Agentic reasoning pipeline completed successfully."
    )


@st.cache_data
def load_data():
    persona_df = pd.read_csv("outputs/persona_dataset_full.csv")
    #persona_df = pd.read_csv("../outputs/persona_dataset_full.csv")
    unified_df = pd.read_csv("../outputs/unified_behavior_with_archetype.csv")
    restaurant_df = pd.read_csv("../data/external/lagos_restaurants_metadata.csv")
    return persona_df, unified_df, restaurant_df

# Then unpack:
persona_df, unified_behavior_df, lagos_df = load_data()


# task b load data
persona_df = pd.read_csv(
    # "../outputs/persona_dataset.csv"
    "outputs/persona_dataset_full.csv"
    
)

lagos_df = pd.read_csv(
    "../data/external/clean_lagos_restaurants.csv"
)

unified_behavior_df = pd.read_csv(
    "../outputs/unified_behavior_dataset.csv"
)

