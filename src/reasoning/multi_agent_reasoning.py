# This module implements a multi-agent reasoning system that simulates different aspects of human decision-making when evaluating a business. 
# Each agent represents a different perspective (emotional, value-based, analytical, social) and contributes to a final recommendation based on their individual assessments.
# Emotional Agent = reacts emotionally
# Analytical Agent = evaluates logically
# Value Agent	= checks value alignment
# Social Agent	= considers social/contextual fit


# EMOTIONAL AGENT

def emotional_agent(
    persona_row,
    business_row,
    context_name
):

    emotionality = persona_row.get(
        "emotionality_score",
        0
    )

    if emotionality > 0.7:

        return {
            "agent": "Emotional Agent",
            "decision": "positive",
            "reason":
                "Strong emotional engagement detected."
        }

    return {
        "agent": "Emotional Agent",
        "decision": "neutral",
        "reason":
            "Emotion was not a major factor."
    }


# VALUE AGENT

def value_agent(
    persona_row,
    business_row
):

    price_sensitivity = persona_row.get(
        "price_sensitivity",
        0
    )

    price_level = business_row.get(
        "price_level",
        2
    )

    if (
        price_sensitivity > 0.7
        and price_level >= 3
    ):

        return {
            "agent": "Value Agent",
            "decision": "negative",
            "reason":
                "Pricing conflicts with user values."
        }

    return {
        "agent": "Value Agent",
        "decision": "positive",
        "reason":
            "Pricing aligns with expectations."
    }


# ANALYTICAL AGENT

def analytical_agent(
    persona_row,
    business_row
):

    avg_rating = business_row.get(
        "stars",
        3
    )

    if avg_rating >= 4:

        return {
            "agent": "Analytical Agent",
            "decision": "positive",
            "reason":
                "Strong public reputation."
        }

    return {
        "agent": "Analytical Agent",
        "decision": "neutral",
        "reason":
            "Moderate reputation detected."
    }


# SOCIAL AGENT

def social_agent(
    context_name
):

    if context_name in [
        "celebration",
        "social_night_out"
    ]:

        return {
            "agent": "Social Agent",
            "decision": "positive",
            "reason":
                "Context supports social engagement."
        }

    return {
        "agent": "Social Agent",
        "decision": "neutral",
        "reason":
            "Social relevance limited."
    }


# FINAL DEBATE SYNTHESIS

def run_multi_agent_debate(
    persona_row,
    business_row,
    context_name
):

    agents = [

        emotional_agent(
            persona_row,
            business_row,
            context_name
        ),

        value_agent(
            persona_row,
            business_row
        ),

        analytical_agent(
            persona_row,
            business_row
        ),

        social_agent(
            context_name
        )
    ]

    positive_votes = sum(
        agent["decision"] == "positive"
        for agent in agents
    )

    negative_votes = sum(
        agent["decision"] == "negative"
        for agent in agents
    )

    if positive_votes > negative_votes:
        final_decision = "recommend"

    elif negative_votes > positive_votes:
        final_decision = "avoid"

    else:
        final_decision = "mixed"

    return {

        "final_decision":
            final_decision,

        "agent_discussions":
            agents
    }