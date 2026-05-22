# PRICE COUNTERFACTUAL
# This function analyzes how price sensitivity and business pricing may impact the predicted rating, and generates a counterfactual explanation if applicable.
# It checks if the persona is highly price-sensitive, if the business has a high price level, and if the predicted rating is low. If all conditions are met, 
# it suggests that making pricing more affordable could improve the rating, and provides an estimated improved rating based on the current prediction.
# This helps the system explain alternate behavioral outcomes.


def analyze_price_counterfactual(
    persona_row,
    business_row,
    predicted_rating
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
        and predicted_rating <= 3
    ):

        improved_rating = min(
            predicted_rating + 2,
            5
        )

        return {
            "factor": "pricing",
            "counterfactual":
                f"If pricing were more affordable, "
                f"the predicted rating could rise "
                f"to {improved_rating}."
        }

    return None


# SERVICE COUNTERFACTUAL

def analyze_service_counterfactual(
    predicted_rating
):

    if predicted_rating <= 3:

        improved_rating = min(
            predicted_rating + 1,
            5
        )

        return {
            "factor": "service",
            "counterfactual":
                f"If service quality improved, "
                f"the experience may increase "
                f"to {improved_rating} stars."
        }

    return None


# CONTEXT COUNTERFACTUAL

def analyze_context_counterfactual(
    context_name,
    predicted_rating
):

    if (
        context_name == "weekday_quick_meal"
        and predicted_rating <= 3
    ):

        return {
            "factor": "context",
            "counterfactual":
                "This venue may perform better "
                "during relaxed social occasions "
                "rather than rushed weekday visits."
        }

    return None


# FULL COUNTERFACTUAL ANALYSIS

def generate_counterfactuals(
    persona_row,
    business_row,
    context_name,
    predicted_rating
):

    analyses = [

        analyze_price_counterfactual(
            persona_row,
            business_row,
            predicted_rating
        ),

        analyze_service_counterfactual(
            predicted_rating
        ),

        analyze_context_counterfactual(
            context_name,
            predicted_rating
        )
    ]

    analyses = [
        analysis
        for analysis in analyses
        if analysis is not None
    ]

    return analyses