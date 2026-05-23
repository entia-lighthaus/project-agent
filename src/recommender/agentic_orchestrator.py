# AGENTIC ORCHESTRATOR
# This module orchestrates the entire agentic recommendation pipeline, integrating multi-agent reasoning, counterfactual generation, behavioral retrieval, and recommendation generation. 
# It also manages the recommendation memory to maintain conversational continuity across user interactions.

from src.reasoning.multi_agent_reasoning import (
    run_multi_agent_debate
)

from src.reasoning.counterfactuals import (
    generate_counterfactuals
)

from src.recommender.behavioral_retrieval import (
    retrieve_behavioral_matches
)

from src.recommender.recommendation_generation import (
    generate_conversational_recommendations
)

from src.recommender.recommendation_memory import (
    store_recommendation_interaction,
    build_multiturn_context
)


def run_agentic_recommendation_pipeline(

    persona_row,

    business_row,

    unified_behavior_df,

    context_name="social_night_out",

    user_id="user_001"
):

    # MULTITURN CONTEXT

    memory_context = (
        build_multiturn_context(
            user_id
        )
    )

    # MULTI-AGENT REASONING

    debate_output = (
        run_multi_agent_debate(

            persona_row,

            business_row,

            context_name
        )
    )

    # COUNTERFACTUAL REASONING

    counterfactuals = (
        generate_counterfactuals(

        persona_row=persona_row,

        business_row=business_row,

        context_name=context_name,

        predicted_rating=4 # TODO: replace with actual predicted rating from reasoning module. 
        # Later integrate: simulate_review() inside orchestration to produce generated review and predicted rating dynamically.
        )
    )

    # RETRIEVAL

    retrieval_results = (
        retrieve_behavioral_matches(

            persona_row,

            unified_behavior_df,

            top_k=10
        )
    )

    # GENERATE RECOMMENDATIONS

    recommendations = (
        generate_conversational_recommendations(

            persona_row,

            retrieval_results,

            top_k=5
        )
    )

    # STORE MEMORY

    for recommendation in recommendations:

        store_recommendation_interaction(

            user_id,

            recommendation
        )

    return {

        "memory_context":
            memory_context,

        "debate_output":
            debate_output,

        "counterfactuals":
            counterfactuals,

        "recommendations":
            recommendations
    }