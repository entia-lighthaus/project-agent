# Conversational Recommendation Agent Page
# This page allows users to interact with a conversational recommendation agent. 
# Users can input their preferences in natural language, and the agent will respond with recommendations or ask for clarification if needed. 
# The conversation history is maintained in the session state, allowing for a seamless chat experience.

import os
import streamlit as st
import sys
import pandas as pd


sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "../.."
        )
    )
)

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# DATA LOADING FUNCTION
def load_data():
    persona_df = pd.read_csv(os.path.join(PROJECT_ROOT, "outputs", "persona_dataset_full.csv"))
    unified_df = pd.read_csv(os.path.join(PROJECT_ROOT, "outputs", "unified_behavior_with_archetype.csv"))
    lagos_df = pd.read_csv(os.path.join(PROJECT_ROOT, "data", "external", "lagos_restaurants_metadata.csv"))
    return persona_df, unified_df, lagos_df


from src.recommender.conversational_agent import (
    conversational_agent
)


st.title(
    "Conversational Recommendation Agent" 
)


st.markdown("""
Chat naturally with the recommendation agent.

Example:
- “I want a chill rooftop in Lagos for date night.”
- “Affordable brunch spot on the Island.”
- “I want a premium social experience.”
""")


# SESSION MEMORY

if "messages" not in st.session_state:

    st.session_state.messages = []


# DISPLAY HISTORY

for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )


# USER INPUT

prompt = st.chat_input(
    "Tell me what you're looking for..."
)


if prompt:

    # DISPLAY USER MESSAGE

    st.session_state.messages.append(

        {
            "role": "user",

            "content": prompt
        }
    )


    with st.chat_message(
        "user"
    ):

        st.markdown(prompt)


    # AGENT RESPONSE

    output = conversational_agent(

        prompt,

        user_id="streamlit_chat_user"
    )


    # BUILD RESPONSE

    if output["type"] == "clarification":

        assistant_response = (
            output["response"]
        )
        
    else:

        assistant_response = (
            output["response"]
        )


    # DISPLAY ASSISTANT RESPONSE

    with st.chat_message(
        "assistant"
    ):

        st.markdown(
            assistant_response
        )


    # SAVE RESPONSE

    st.session_state.messages.append(

        {
            "role": "assistant",

            "content": assistant_response
        }
    )