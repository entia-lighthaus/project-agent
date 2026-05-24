# CONVERSATIONAL AGENT
# This module implements a conversational agent that interacts with users to extract preferences, 
# maintain memory, and generate personalized recommendations in a multi-turn dialogue format. It uses simple 
# rule-based extraction for demonstration but can be extended with more advanced NLP techniques for better 
# understanding and interaction. The agent maintains a memory of user interactions to provide a more personalized 
# and context-aware recommendation experience over time, demonstrating conversational continuity.

import re
import pandas as pd
import random
from groq import Groq
import os

from dotenv import load_dotenv

load_dotenv()

client = Groq(

    api_key=os.getenv(
        "GROQ_API_KEY"
    )
)



# MEMORY STORE

conversation_memory = {}

BASE_DIR = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "../.."
    )
)

lagos_path = os.path.join(
    BASE_DIR,
    "data",
    "external",
    "clean_lagos_restaurants.csv"
)

lagos_df = pd.read_csv(
    lagos_path
)



# EXTRACT USER PREFERENCES

def extract_preferences(
        
    user_message
    
):

    message = user_message.lower()

    preferences = {}


    # VIBE

    if "chill" in message:

        preferences["vibe"] = "chill"

    if "romantic" in message:

        preferences["vibe"] = "romantic"

    if "lively" in message:

        preferences["vibe"] = "lively"


    # LOCATION

    if "island" in message:

        preferences["area"] = "Island"

    if "mainland" in message:

        preferences["area"] = "Mainland"


    # OCCASION

    if "date" in message:

        preferences["occasion"] = "date night"

    if "birthday" in message:

        preferences["occasion"] = "celebration"


    # BUDGET

    if "cheap" in message:

        preferences["budget"] = "cheap"

    if "affordable" in message:

        preferences["budget"] = "affordable"

    if "premium" in message:

        preferences["budget"] = "premium"


    # VENUE TYPE

    if "rooftop" in message:

        preferences["venue_type"] = "rooftop"

    if "restaurant" in message:

        preferences["venue_type"] = "restaurant"


    return preferences



# UPDATE MEMORY

def update_memory(
    user_id,
    preferences
):

    if user_id not in conversation_memory:

        conversation_memory[user_id] = {}

    conversation_memory[user_id].update(
        preferences
    )



# GET MISSING SLOTS

def get_missing_slots(
    memory
):

    required_slots = [

        "venue_type",

        "occasion",

        "area"
    ]

    missing = []

    for slot in required_slots:

        if slot not in memory:

            missing.append(slot)

    return missing



# GENERATE FOLLOW-UP QUESTIONS

def generate_followup_question(
    missing_slot
):

    questions = {

        "area":
            "Mainland or Island?",

        "occasion":
            "What’s the occasion?",

        "venue_type":
            "Are you looking for a rooftop, restaurant, lounge, or café?"
    }

    return questions.get(
        missing_slot,
        "Can you tell me more?"
    )



# GENERATE RECOMMENDATIONS

def generate_conversational_recommendation(
    memory
):

    filtered_df = lagos_df.copy()


    # AREA FILTER

    area = memory.get(
        "area",
        ""
    )

    if area == "Island":

        island_keywords = [

            "VI",

            "Lekki",

            "Victoria Island",

            "Ikoyi"
        ]

        filtered_df = filtered_df[

            filtered_df[
                "restaurant_name"
            ]

            .astype(str)

            .str.contains(

                "|".join(
                    island_keywords
                ),

                case=False,

                na=False
            )
        ]


    # BUDGET FILTER

    budget = memory.get(
        "budget",
        ""
    )


    # VIBE FILTER

    vibe = memory.get(
        "vibe",
        ""
    )


    # LIGHT REVIEW FILTERING

    if vibe == "romantic":

        filtered_df = filtered_df[

            filtered_df[
                "review_text"
            ]

            .astype(str)

            .str.contains(

                "romantic|cozy|beautiful",

                case=False,

                na=False
            )
        ]


    if vibe == "chill":

        filtered_df = filtered_df[

            filtered_df[
                "review_text"
            ]

            .astype(str)

            .str.contains(

                "relax|calm|soft|cozy|nice",

                case=False,

                na=False
            )
        ]


    # FALLBACK

    if len(filtered_df) < 3:

        filtered_df = lagos_df.copy()


    # SAMPLE RECOMMENDATIONS

    sampled = filtered_df.sample(

        min(3, len(filtered_df)),

        random_state=random.randint(
            1,
            10000
        )
    )


    recommendations = []


    for _, row in sampled.iterrows():

        recommendations.append(

            {
                "name":
                    row["restaurant_name"],

                "description":
                    str(
                        row["review_text"]
                    )[:200]
            }
        )


    return recommendations


# GENERATE GEMINI RESPONSE
def generate_gemini_response(
    memory,
    recommendations
):

    recommendation_text = ""

    for rec in recommendations:

        recommendation_text += (

            f"- {rec['name']}: "

            f"{rec['description']}\n"
        )


    prompt = f"""

You are a conversational Lagos lifestyle recommendation assistant.

The user preferences are:

{memory}

The retrieved recommendations are:

{recommendation_text}

Generate a natural conversational recommendation response.

Requirements:
- Sound warm and intelligent
- Recommend the restaurants naturally
- Mention vibe and affordability where relevant
- Keep it concise
- Sound like a premium AI concierge
- Ask a follow-up question at the end
"""


    try:

        completion = client.chat.completions.create(

            model="llama3-70b-8192",

            messages=[

                {
                    "role": "system",

                    "content":
                        "You are a premium Lagos lifestyle recommendation concierge."
                },

                {
                    "role": "user",

                    "content": prompt
                }
            ],

            temperature=0.8,

            max_tokens=300
        )


        return (

            completion

            .choices[0]

            .message.content
        )


    except Exception:


        fallback_response = (

            f"I found a few places that match your "

            f"{memory.get('vibe', 'preferred')} vibe "

            f"for {memory.get('occasion', 'your outing')}.\n\n"
        )


        for rec in recommendations:

            fallback_response += (

                f"• {rec['name']} — "

                f"{rec['description'][:120]}...\n\n"
            )


        fallback_response += (

            "Would you like more affordable, premium, "

            "or hidden-gem recommendations?"
        )


        return fallback_response


# MAIN AGENT FUNCTION

def conversational_agent(
    user_message,
    user_id="default_user"
):

    if should_reset_conversation(
        user_message
    ):

        conversation_memory[user_id] = {}

    preferences = extract_preferences(
        user_message
    )

    update_memory(
        user_id,
        preferences
    )

    memory = conversation_memory[
        user_id
    ]


    missing_slots = get_missing_slots(
        memory
    )


    # ASK FOLLOW-UP QUESTION

    if len(missing_slots) > 0:

        question = generate_followup_question(

            missing_slots[0]
        )

        return {

            "type": "clarification",

            "response": question,

            "memory": memory
        }


    # GENERATE RECOMMENDATIONS

    recommendations = (

        generate_conversational_recommendation(
            memory
        )
    )

    natural_response = (

        generate_gemini_response(

            memory,

            recommendations
        )
    )


    return {

        "type": "recommendation",

        "response": natural_response,

        "recommendations": recommendations,

        "memory": memory
    }


# CONVERSATION RESET DETECTION
def should_reset_conversation(
    user_message
):

    reset_keywords = [

        "instead",

        "actually",

        "new",

        "another",

        "different",

        "forget",

        "change"
    ]

    message = user_message.lower()

    for word in reset_keywords:

        if word in message:

            return True

    return False