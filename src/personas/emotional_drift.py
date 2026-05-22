# STEP 44 — COMPUTE RATING DRIFT
# We now measure whether users become harsher or softer over time.
# By computing the rating drift, we can identify trends in user behavior, 
# such as whether users tend to become more critical or more lenient in their reviews over time, 
# which can provide insights into changes in user expectations and satisfaction.

def compute_rating_drift(ratings):

    if len(ratings) < 2:
        return 0

    return ratings[-1] - ratings[0]


# ====================================================
# STEP 45 — COMPUTE SENTIMENT DRIFT
# We now measure the evolution of user sentiments over time.
# By computing the sentiment drift, we can identify trends in user emotions, 
# such as whether users tend to become more positive or more negative in their reviews over time, 
# which can provide insights into changes in user experiences and satisfaction.

def compute_sentiment_drift(sentiments):

    if len(sentiments) < 2:
        return 0

    return sentiments[-1] - sentiments[0]


# ====================================================


# STEP 55 — SPLIT EARLY VS RECENT BEHAVIOR
# We compare past self vs current self.

def split_temporal_preferences(user_df):

    user_df = user_df.sort_values("date")

    midpoint = len(user_df) // 2

    early = user_df.iloc[:midpoint]
    recent = user_df.iloc[midpoint:]

    return early, recent

# ===================================================


# STEP 56: DETECT PREFERENCE DRIFT

from collections import Counter

preference_drift_results = []

def detect_preference_drift(curated_reviews):
    for user_id, user_df in curated_reviews.groupby("user_id"):

        if len(user_df) < 6:
            continue

    early, recent = split_temporal_preferences(user_df)

    early_cuisines = [
        cuisine
        for sublist in early["cuisines"]
        for cuisine in sublist
    ]

    recent_cuisines = [
        cuisine
        for sublist in recent["cuisines"]
        for cuisine in sublist
    ]

    early_top = Counter(early_cuisines).most_common(3)
    recent_top = Counter(recent_cuisines).most_common(3)

    preference_drift_results.append({
        "user_id": user_id,
        "early_preferences": early_top,
        "recent_preferences": recent_top
    })