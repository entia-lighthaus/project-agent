"""
Cross-domain taste graph implementation.
"""
import math
import json
from collections import defaultdict
from typing import Dict, List, Tuple, Optional


class TasteGraph:
    """
    Manages user → aesthetic tag weights and tag → item mappings.
    """
    
    def __init__(self):
        # user_id → {tag → weight}
        self.user_tag_weights = defaultdict(lambda: defaultdict(float))
        
        # item_id → [tags]
        self.item_tags = {}
        
        # tag → {domain → [item_ids]}  (inverted index)
        self.tag_domain_index = defaultdict(lambda: defaultdict(list))
        
        # user_id → {domain → interaction_count}
        self.domain_interaction_counts = defaultdict(lambda: defaultdict(int))
    
    def load_item_tags(self, item_tags: Dict[str, List[str]], items_meta: List[Dict]):
        """
        Initialize from precomputed tag extraction.
        
        Args:
            item_tags: {item_id: [tag1, tag2, ...]}
            items_meta: [{id, category, ...}, ...]
        """
        self.item_tags = item_tags
        
        # Build inverted index
        for item in items_meta:
            item_id = item.get("id") or item.get("business_id")
            domain = item.get("category", "unknown")
            
            for tag in item_tags.get(item_id, []):
                self.tag_domain_index[tag][domain].append(item_id)
        
        print(f"Loaded {len(self.item_tags)} items across {len(self.tag_domain_index)} tags")
    
    def update_from_interaction(
        self,
        user_id: str,
        item_id: str,
        signal: float,
        timestamp: float,
        current_time: float,
        half_life_days: float = 60.0
    ):
        """
        Update user→tag edge weights from a single interaction.
        
        Args:
            user_id: User identifier
            item_id: Item identifier
            signal: +1.0 = loved, +0.5 = liked, -0.5 = disliked, -1.0 = hated
            timestamp: Unix timestamp of interaction
            current_time: Current unix timestamp (for decay calculation)
            half_life_days: How quickly old signals decay
        """
        tags = self.item_tags.get(item_id, [])
        if not tags:
            return
        
        # Temporal decay: older signals count less
        age_days = (current_time - timestamp) / 86400
        decay = math.exp(-0.693 * age_days / half_life_days)  # 0.693 = ln(2)
        decayed_signal = signal * decay
        
        # Distribute signal across all tags of the item
        per_tag_signal = decayed_signal / len(tags)
        
        for tag in tags:
            self.user_tag_weights[user_id][tag] += per_tag_signal
    
    def record_domain_interaction(self, user_id: str, domain: str):
        """Track that user interacted with an item in this domain."""
        self.domain_interaction_counts[user_id][domain] += 1
    
    def get_aesthetic_profile(self, user_id: str, top_n: int = 8) -> List[Tuple[str, float]]:
        """
        Returns sorted list of (tag, weight) for a user.
        Positive weights = affinity. Negative = aversion.
        """
        weights = self.user_tag_weights.get(user_id, {})
        return sorted(weights.items(), key=lambda x: x[1], reverse=True)[:top_n]
    
    def get_aversions(self, user_id: str, top_n: int = 4) -> List[str]:
        """Tags the user consistently dislikes."""
        weights = self.user_tag_weights.get(user_id, {})
        return [t for t, w in sorted(weights.items(), key=lambda x: x[1]) if w < 0][:top_n]
    
    def is_cold_start(self, user_id: str, min_interactions: int = 3) -> bool:
        """True if we don't have enough signal yet."""
        weights = self.user_tag_weights.get(user_id, {})
        return sum(1 for w in weights.values() if abs(w) > 0.1) < min_interactions
    
    def is_cold_start_in_domain(self, user_id: str, domain: str, min_interactions: int = 2) -> bool:
        """True if user hasn't interacted with this domain enough."""
        domain_interactions = self.domain_interaction_counts.get(user_id, {})
        return domain_interactions.get(domain, 0) < min_interactions
    
    def save(self, path: str):
        """Save graph to disk."""
        state = {
            "user_tag_weights": dict(self.user_tag_weights),
            "item_tags": self.item_tags,
            "tag_domain_index": dict(self.tag_domain_index),
            "domain_interaction_counts": dict(self.domain_interaction_counts),
        }
        with open(path, 'w') as f:
            json.dump(state, f)
        print(f"Saved taste graph to {path}")
    
    @classmethod
    def load(cls, path: str):
        """Load graph from disk."""
        with open(path) as f:
            state = json.load(f)
        
        graph = cls()
        graph.user_tag_weights = defaultdict(lambda: defaultdict(float), state["user_tag_weights"])
        graph.item_tags = state["item_tags"]
        graph.tag_domain_index = defaultdict(lambda: defaultdict(list), state["tag_domain_index"])
        graph.domain_interaction_counts = defaultdict(lambda: defaultdict(int), state["domain_interaction_counts"])
        
        print(f"Loaded taste graph from {path}")
        return graph