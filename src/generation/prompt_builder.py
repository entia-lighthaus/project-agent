# This module contains the function to build the review generation prompt based on the persona, business, context, predicted rating, and review blueprint.

def build_review_prompt(
    persona_row,
    business_row,
    context_name,
    predicted_rating,
    review_blueprint
):

    prompt = f"""

You are simulating a realistic human Yelp reviewer.

USER PROFILE:
- Archetype: {persona_row['archetype']}
- Dominant Value: {persona_row['dominant_value']}
- Nigerian Identity: {persona_row['nigerian_identity']}
- Nigerian Communication Style: {persona_row['nigerian_style']}

CURRENT CONTEXT:
- Situation: {context_name}

RESTAURANT:
- Name: {business_row['name']}
- Categories: {business_row['categories']}
- Average Yelp Rating: {business_row['stars']}

PREDICTED USER EXPERIENCE:
- Expected Rating: {predicted_rating} stars

REVIEW STYLE PLAN:
- Tone: {review_blueprint['review_plan']['tone']}
- Emotional Intensity:
  {review_blueprint['review_plan']['emotional_intensity']}
- Verbosity:
  {review_blueprint['review_plan']['verbosity']}
- Criticism Style:
  {review_blueprint['review_plan']['criticism_style']}
- Nigerian Flavor:
  {review_blueprint['review_plan']['nigerian_flavor']}

FOCUS AREAS:
{', '.join(review_blueprint['focus_areas'])}

INSTRUCTIONS:
- Write EXACTLY like a real human reviewer.
- Avoid sounding like AI.
- Be conversational and emotionally natural.
- Use realistic restaurant details.
- Match the user's personality strongly.
- Match the predicted emotional tone.
- Use subtle Nigerian conversational style where appropriate.
- Sound culturally Nigerian where appropriate.
- Do NOT explain yourself.
- Do NOT summarize.
- Do NOT use bullet points.
- Do NOT overuse slang.
- Write ONLY the review.
- Sound spontaneous.
- Include imperfections in expression naturally.

"""

    return prompt