# This module contains functions for estimating the uncertainty of the reasoning process, 
# which can help the system identify when its conclusions may be less reliable and provide more cautious recommendations or explanations.
# The uncertainty estimation considers factors such as the amount of information available, the consistency of agent discussions, and the emotional variability of the persona.

# WHY THIS MATTERS
# Without uncertainty AI looks unrealistically confident.
# With uncertainty AI appears thoughtful and human. This is very important psychologically.


# UNCERTAINTY ESTIMATION
def estimate_decision_confidence(
    persona_row,
    memory,
    debate_result
):

    confidence = 1.0

    interaction_count = memory.get(
        "interaction_count",
        0
    )

    # LOW MEMORY

    if interaction_count < 3:
        confidence -= 0.3

    # CONFLICTING AGENTS

    decisions = [

        agent["decision"]

        for agent in debate_result[
            "agent_discussions"
        ]
    ]

    positive_votes = decisions.count(
        "positive"
    )

    negative_votes = decisions.count(
        "negative"
    )

    if (
        positive_votes > 0
        and negative_votes > 0
    ):

        confidence -= 0.2

    # HIGH EMOTIONAL VARIABILITY

    emotionality = persona_row.get(
        "emotionality_score",
        0
    )

    if emotionality > 0.8:
        confidence -= 0.1

    confidence = max(
        confidence,
        0
    )

    # LABEL

    if confidence >= 0.75:
        confidence_label = "high"

    elif confidence >= 0.45:
        confidence_label = "moderate"

    else:
        confidence_label = "low"

    return {

        "confidence_score":
            round(confidence, 2),

        "confidence_label":
            confidence_label
    }