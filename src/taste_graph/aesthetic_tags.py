"""
Aesthetic tag ontology for cross-domain taste modeling.
Tags are domain-agnostic — they describe vibe, not category.
"""

AESTHETIC_TAGS = {
    # Ambiance / atmosphere
    "minimalist": "Clean, sparse, uncluttered design",
    "maximalist": "Rich, layered, ornate presentation",
    "cozy": "Warm, intimate, snug atmosphere",
    "high-energy": "Loud, buzzy, lively environment",
    "avant-garde": "Experimental, boundary-pushing, unconventional",
    "traditional": "Classic, time-tested, familiar",
    "hidden-gem": "Obscure, off-the-beaten-path, local favorite",
    "mainstream": "Popular, well-known, crowd-pleasing",
    
    # Price / exclusivity
    "budget": "Affordable, value-focused",
    "mid-range": "Moderate pricing, balanced value",
    "premium": "High quality, elevated experience",
    "luxury": "Exclusive, status-oriented, high-end",
    
    # Social context
    "solo-friendly": "Good for one person, relaxed",
    "group-oriented": "Designed for parties/crowds",
    "romantic": "Intimate, date-appropriate",
    "family-friendly": "Welcoming to children, casual",
    
    # Sensory profile
    "bold-flavors": "Intense, strong, unapologetic taste",
    "subtle": "Nuanced, delicate, refined",
    "adventurous": "Unusual ingredients, unexpected combinations",
    "comfort-first": "Familiar, safe, satisfying",
    
    # Pacing / intensity
    "fast": "Quick, efficient, no-fuss service",
    "slow": "Leisurely, experience-focused, unhurried",
}

def get_tag_list():
    """Returns list of valid tag names."""
    return list(AESTHETIC_TAGS.keys())

def get_tag_description(tag: str) -> str:
    """Returns human-readable description of a tag."""
    return AESTHETIC_TAGS.get(tag, "Unknown tag")