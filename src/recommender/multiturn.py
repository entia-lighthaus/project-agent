# MULTI-TURN RECOMMENDATION MODULE
# This module is responsible for handling the multi-turn recommendation process, 
# which involves updating the user's memory based on their interactions with the recommended businesses, 
# recomputing compatibility scores, and generating explanations for the recommendations. 

# The multi-turn process allows the system to adapt to the user's evolving preferences and context, 
# providing a more personalized and dynamic recommendation experience. 
# The pipeline will: Update memory with new interactions, Recompute compatibility scores, Generate explanations, 
# Provide updated recommendations, Enhance user engagement and satisfaction through personalized interactions.


from src.memory.user_memory import (
    update_user_memory,
    summarize_memory
)

from src.recommender.compatibility import (
    compute_total_compatibility
)

from src.recommender.explanations import (
    generate_recommendation_explanation
)


# MULTI-TURN RECOMMENDATION STEP

def run_multiturn_recommendation_step(

    persona_row,

    business_row,

    memory,

    context_name,

    predicted_rating
):

    # EMOTIONAL TONE

    if predicted_rating >= 4:
        emotional_tone = "positive"

    elif predicted_rating <= 2:
        emotional_tone = "frustrated"

    else:
        emotional_tone = "mixed"

    # UPDATE MEMORY

    memory = update_user_memory(

        memory,

        business_row,

        predicted_rating,

        context_name,

        emotional_tone
    )

    # RECOMPUTE COMPATIBILITY

    compatibility = (
        compute_total_compatibility(

            persona_row,

            business_row,

            memory,

            context_name
        )
    )

    # GENERATE EXPLANATION

    explanation = (
        generate_recommendation_explanation(

            persona_row,

            business_row,

            memory,

            context_name,

            compatibility
        )
    )

    # MEMORY SUMMARY

    memory_summary = summarize_memory(
        memory
    )

    return {

        "updated_memory":
            memory,

        "memory_summary":
            memory_summary,

        "compatibility":
            compatibility,

        "recommendation_explanation":
            explanation
    }

# Your system will now: remember previous interactions, 
# adapt future recommendations, evolve emotionally
# avoid repetitive suggestions and simulate changing human preferences.

# Now, every interaction changes memory,future recommendations, emotional state, and behavioral expectations.

