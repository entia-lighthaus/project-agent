import pandas as pd

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans


# HUMAN ARCHETYPE LABELS

cluster_names = {
    0: "Warm Optimist",
    1: "Reactive Reviewer",
    2: "Harsh Critic",
    3: "Emotional Storyteller",
    4: "Deep Experience Analyst"
}


# STEP 1 — CREATE CLUSTERING FEATURES

def prepare_clustering_features(persona_df):

    clustering_features = persona_df[
        [
            "avg_rating",
            "rating_variance",
            "avg_review_length",
            "avg_sentiment",
            "sentiment_variance"
        ]
    ].fillna(0)

    return clustering_features


# STEP 2 — SCALE FEATURES

def scale_features(clustering_features):

    scaler = StandardScaler()

    scaled_features = scaler.fit_transform(
        clustering_features
    )

    return scaled_features


# STEP 3 — RUN KMEANS CLUSTERING

def run_kmeans_clustering(
    persona_df,
    scaled_features,
    n_clusters=5
):

    kmeans = KMeans(
        n_clusters=n_clusters,
        random_state=42
    )

    persona_df["cluster"] = (
        kmeans.fit_predict(
            scaled_features
        )
    )

    return persona_df, kmeans


# STEP 4 — ASSIGN HUMAN ARCHETYPES

def assign_archetypes(persona_df):

    persona_df["archetype"] = (
        persona_df["cluster"]
        .map(cluster_names)
    )

    return persona_df


# ====================================================
# STEP 31A - Create Structured Behavioral Descriptors
# ====================================================

behavioral_descriptors = {

    0: {
        "archetype": "Warm Optimist",

        "traits": {
            "positivity": "high",
            "verbosity": "moderate",
            "emotional_stability": "stable",
            "review_style": "supportive",
            "expectation_level": "moderate",
            "decision_style": "emotionally positive"
        }
    },

    1: {
        "archetype": "Reactive Reviewer",

        "traits": {
            "positivity": "mixed",
            "verbosity": "moderate",
            "emotional_stability": "volatile",
            "review_style": "emotion-driven",
            "expectation_level": "variable",
            "decision_style": "experience-sensitive"
        }
    },

    2: {
        "archetype": "Harsh Critic",

        "traits": {
            "positivity": "low",
            "verbosity": "high",
            "emotional_stability": "critical",
            "review_style": "analytical",
            "expectation_level": "high",
            "decision_style": "detail-oriented"
        }
    },

    3: {
        "archetype": "Emotional Storyteller",

        "traits": {
            "positivity": "moderate",
            "verbosity": "high",
            "emotional_stability": "reflective",
            "review_style": "narrative",
            "expectation_level": "balanced",
            "decision_style": "emotionally expressive"
        }
    },

    4: {
        "archetype": "Deep Experience Analyst",

        "traits": {
            "positivity": "moderate",
            "verbosity": "very high",
            "emotional_stability": "stable",
            "review_style": "deeply descriptive",
            "expectation_level": "high",
            "decision_style": "deliberative"
        }
    }
}