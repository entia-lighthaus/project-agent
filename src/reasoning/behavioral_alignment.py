# This module will:
# evaluate generated reviews
# compare reviews to persona psychology
# score realism
# detect behavioral drift
# explain WHY the review fits the persona

import re


# REVIEW LENGTH SCORE

def evaluate_review_length(review_text):

    word_count = len(
        review_text.split()
    )

    if 60 <= word_count <= 250:
        return 1

    return 0


# EMOTIONAL LANGUAGE SCORE

def evaluate_emotional_alignment(
    persona_row,
    review_text
):

    emotional_words = [
        "love",
        "hate",
        "amazing",
        "terrible",
        "excited",
        "angry",
        "frustrated",
        "happy",
        "disappointed"
    ]

    emotionality = (
        persona_row.get(
            "emotionality_score",
            0
        )
    )

    review_lower = review_text.lower()

    emotional_hits = sum(
        word in review_lower
        for word in emotional_words
    )

    if emotionality > 0.6 and emotional_hits > 2:
        return 1

    if emotionality <= 0.6 and emotional_hits <= 2:
        return 1

    return 0


# VALUE ALIGNMENT SCORE

def evaluate_value_alignment(
    persona_row,
    review_text
):

    review_lower = review_text.lower()

    score = 0

    if (
        persona_row.get(
            "price_sensitivity",
            0
        ) > 0.7
    ):

        pricing_words = [
            "price",
            "expensive",
            "cheap",
            "budget",
            "cost"
        ]

        if any(
            word in review_lower
            for word in pricing_words
        ):
            score += 1

    return score


# ARCHETYPE ALIGNMENT

def evaluate_archetype_alignment(
    persona_row,
    review_text
):

    archetype = persona_row.get(
        "archetype",
        ""
    )

    review_lower = review_text.lower()

    if archetype == "Emotional Storyteller":

        storytelling_markers = [
            "we",
            "when",
            "experience",
            "felt"
        ]

        if any(
            word in review_lower
            for word in storytelling_markers
        ):
            return 1

    return 1


# FINAL BEHAVIORAL FIDELITY SCORE

def evaluate_behavioral_fidelity(
    persona_row,
    review_text
):

    scores = {

        "length_score":
            evaluate_review_length(
                review_text
            ),

        "emotion_score":
            evaluate_emotional_alignment(
                persona_row,
                review_text
            ),

        "value_score":
            evaluate_value_alignment(
                persona_row,
                review_text
            ),

        "archetype_score":
            evaluate_archetype_alignment(
                persona_row,
                review_text
            )
    }

    total_score = sum(
        scores.values()
    )

    scores["behavioral_fidelity"] = (
        total_score / len(scores)
    )

    return scores