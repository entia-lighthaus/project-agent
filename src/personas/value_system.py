# STEP 34 — Define Value Taxonomy
# This taxonomy will help us categorize and analyze the different aspects of restaurant reviews, 
# allowing us to extract meaningful insights about customer values, preferences, expectations, and experiences. 
# For each review it counts how often value-related language appears.

import re

def extract_value_signals(text, taxonomy):

    text = text.lower()

    scores = {}

    for category, keywords in taxonomy.items():

        score = 0

        for keyword in keywords:

            matches = re.findall(
                rf"\b{re.escape(keyword)}\b",
                text
            )

            score += len(matches)

        scores[category] = score

    return scores


# ===================================
# STEP 34A — Define Value Taxonomy
# Here we are defining a taxonomy of value-related keywords that can be used to analyze reviews.

value_taxonomy = {

    # Economic values
    "affordability": [
        "cheap", "affordable", "budget", "expensive", "overpriced", "pricey",
        "value for money", "manage", "cost", "naira", "save cost", "waste of money",
        "not worth it", "fair price", "discount", "original price", "market price"
    ],


    # Durability & quality expectations
    "durability": [
        "original", "fake", "counterfeit", "rugged", "last long", "strong",
        "weak", "fragile", "repair", "spare parts", "generator", "battery life",
        "heat up", "spoilt", "still working", "tested and trusted", "tokunbo", "new", "used"
    ],


    # Service & staff behaviour (restaurants, repairs, delivery)
    "service_quality": [
        "service", "staff", "waiter", "waitress", "attentive", "rude",
        "friendly", "slow service", "fast response", "customer care",
        "come and fix", "collect and vanish", "follow me around", "attention to detail", "attentive"
        "pushy seller", "polite", "helpful", "unhelpful", "knowledgeable", "incompetent", "courteous", "disrespectful"
    ],


    # Social proof & communal influence
    "social_proof": [
        "neighbour", "friend recommended", "landlord use am", "colleague",
        "family said", "word of mouth", "everybody buying", "popular",
        "trending", "see my neighbour", "trusted by many", "influencer", "celebrity endorsement", "social media hype"
    ],


    # Temporal / efficiency norms
    "time_efficiency": [
        "wait time", "delay", "fast delivery", "slow", "African time",
        "hours", "minutes", "late", "early", "prompt", "wasted my time",
        "traffic", "Lagos traffic", "delivered on time", "arrived late", 
        "arrived early", "on schedule", "behind schedule", "ahead of schedule"
    ],

    # Ambience & atmosphere (restaurants, events)
    "ambience": [
        "ambience", "atmosphere", "decor", "vibes", "music", "aesthetic", "cozy"
        "lighting", "cleanliness", "noise level", "comfortable seating", "romantic", 
        "family-friendly", "decoration choke", "overcrowded", "spacious", "intimate", "loud", "quiet"
    ],


    # Product‑specific attributes (food, electronics, fashion, books, etc.)
    "food_quality": [
        "delicious", "bland", "taste", "fresh", "flavor", "authentic", "portion",
        "presentation", "spicy", "sweet", "sour", "fresh", "salty", "umami", "overcooked",
        "undercooked", "stale", "rotten", "mouthwatering", "swallow", "fufu", "eba", 
        "soup", "rice", "portion size", "small",
    ],


    "electronics": [
        "generator", "inverter", "phone", "laptop", "battery", "charger",
        "NEPA", "light", "plug", "heating", "original charger", "waterproof"
        "power bank", "noise cancelling", "wireless", "durable", "fast charging", "long battery life"
    ],


    "fashion": [
        "lace", "ankara", "fabric quality", "zipper", "tailor", "sewn",
        "fit", "size", "colour fast", "shrink", "native wear", "casual wear", 
        "formal wear", "workwear", "party wear", "traditional attire"
    ],


    "books_media": [
        "motivational", "hustle", "inspirational", "educational", "story",
        "grammar", "chapters", "cover", "print quality", "prayer points"
    ],

    # Convenience & accessibility
    "convenience": [
        "fast", "quick", "parking", "location", "accessible", "easy",  "waiting time"
        "near me", "home delivery", "takeaway", "drive-thru", "curbside pickup", "self-service"
    ],

    # Social experience
    "social_experience": [
        "friends", "family", "date", "group", "celebration", "birthday", "hangout"
        "social gathering", "romantic dinner", "family outing", "friend meetup", "special occasion"
        "anniversary", "reunion", "casual hangout", "work event", "holiday celebration"
        "new spot to try", "place to see and be seen", "vibe for socializing", "perfect for groups", "intimate setting"
    ],

    # Aspirational & status‑related cues
    "luxury": [
        "premium", "luxury", "upscale", "fancy", "high-end", "exclusive", "luxurious", "opulent", 
        "lavish", "posh", "sophisticated", "elegant", "glamorous"
    ],

   # Sentiment polarity markers (Nigerian style exaggeration)
    "positive_exaggeration": [
        "the best", "amazing", "perfect", "excellent", "I love am",
        "changed my life", "highly recommend", "must buy" "refreshing", "life-changing", "unforgettable", "top-notch", "five stars", "beyond expectations"
    ],

    "negative_exaggeration": [
        "worst ever", "terrible", "useless", "waste of data", "I spit",
        "never again", "run away", "scam", "fake life"
    ],


    # Cold‑start & exploration signals
    "uncertainty": [
        "not sure", "maybe", "let me test", "first time", "trying",
        "I no know o", "time will tell", "hoping for the best", "heard good things", "heard bad things", "mixed reviews", "on the fence"
    ]

}



# ====================================================

# STEP 46 — CLASSIFY EMOTIONAL TRAJECTORIES
# We classify users based on their sentiment drift to understand their emotional trajectories over time.

def classify_drift(value):

    if value > 0.5:
        return "becoming_more_positive"

    elif value < -0.5:
        return "becoming_more_negative"

    else:
        return "emotionally_stable"
    
    
# ====================================================

# STEP 82 — CREATE RECOMMENDATION TENDENCY ENGINE
# Now we infer what these humans are likely to prefer.

def recommendation_tendency(row):

    dominant_value = row["dominant_value"]
    archetype = row["archetype"]

    if dominant_value == "ambience":
        return "prefers aesthetic and socially vibrant venues"

    elif dominant_value == "service":
        return "prefers highly reliable and respectful experiences"

    elif dominant_value == "food_quality":
        return "prioritizes authentic and high-quality meals"

    elif dominant_value == "affordability":
        return "seeks budget-friendly and high-value experiences"

    elif dominant_value == "social_experience":
        return "prefers lively social environments"

    elif dominant_value == "time_efficiency":
        return "values prompt service and hates unnecessary delays"

    elif dominant_value == "social_proof":
        return "trusts what friends, family, and popular opinion recommend"

    elif dominant_value == "service_quality":
        return "expects courteous, attentive, and reliable staff"

    elif dominant_value == "durability":
        return "prioritises long-lasting, rugged, and original products"

    elif dominant_value == "convenience":
        return "prefers easy access, fast delivery, and hassle‑free processes"

    elif dominant_value == "luxury":
        return "seeks premium, high‑status, and indulgent experiences"
    
    else:
        return "balanced preferences"