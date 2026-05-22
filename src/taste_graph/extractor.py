"""
Extract aesthetic tags from items using LLM.
"""
import json
import re
import time
from typing import List, Dict
import os
from dotenv import load_dotenv
import google.generativeai as genai

from .aesthetic_tags import get_tag_list

# Load environment variables so the Gemini API key is available at import time
load_dotenv()

# Configure Gemini
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

MODEL_CANDIDATES = [
    'models/gemini-2.5-flash',
    'models/gemini-2.5-flash-lite',
    'models/gemini-flash-latest',
    'models/gemini-flash-lite-latest',
]

_model = None

def _select_gemini_model() -> genai.GenerativeModel:
    global _model
    if _model is not None:
        return _model

    test_prompt = 'Say hello in one word.'
    last_error = None
    for model_name in MODEL_CANDIDATES:
        try:
            candidate = genai.GenerativeModel(model_name)
            response = candidate.generate_content(test_prompt)
            if response and getattr(response, 'text', '').strip():
                print(f"Using Gemini model: {model_name}")
                _model = candidate
                return _model
        except Exception as e:
            last_error = e
            print(f"Model {model_name} failed: {e}")
            continue

    raise RuntimeError(
        "No Gemini model could be selected. "
        "Check your API key, quota, and available models. "
        f"Last error: {last_error}"
    )


def _get_model() -> genai.GenerativeModel:
    return _select_gemini_model()


def extract_tags_for_item(item: Dict) -> List[str]:
    """
    Extract aesthetic tags for a single item using Gemini.
    
    Args:
        item: {
            "name": str,
            "category": str,
            "description": str (optional),
            "reviews": List[str] (optional - sample of review texts),
            "avg_rating": float (optional)
        }
    
    Returns:
        List of aesthetic tag strings
    """
    valid_tags = get_tag_list()
    
    # Build rich context from available fields
    review_sample = ""
    if item.get("reviews"):
        review_sample = " ".join(item["reviews"][:5])
    
    prompt = f"""You are tagging items with aesthetic attributes for a cross-domain recommendation system.

Item name: {item.get('name', 'Unknown')}
Category: {item.get('category', 'Unknown')}
Description: {item.get('description', 'N/A')}
Sample reviews: {review_sample or 'N/A'}

Valid tags: {json.dumps(valid_tags)}

Return ONLY a JSON array of the most applicable tags (3-7 tags).
Choose tags that describe the VIBE and AESTHETIC, not the category.
Example: ["minimalist", "premium", "solo-friendly", "subtle"]

Respond with ONLY the JSON array, nothing else."""

    retry_attempts = 3
    for attempt in range(retry_attempts):
        try:
            response = _get_model().generate_content(prompt)
            raw = response.text.strip()
            
            # Handle markdown fences if present
            if raw.startswith("```"):
                raw = raw.split("```")[1]
                if raw.startswith("json"):
                    raw = raw[4:]
            
            tags = json.loads(raw.strip())
            
            # Validate — keep only known tags
            return [t for t in tags if t in valid_tags]
        except Exception as e:
            error_text = str(e)
            is_rate_limit = (
                '429' in error_text or
                'quota' in error_text.lower() or
                'rate limit' in error_text.lower() or
                'resourceexhausted' in error_text.lower()
            )
            if is_rate_limit and attempt < retry_attempts - 1:
                wait_seconds = 35
                match = re.search(r'retry in (\d+)', error_text, re.IGNORECASE)
                if match:
                    wait_seconds = int(match.group(1)) + 5
                print(f"Rate limited on {item.get('name', 'unknown')}: waiting {wait_seconds}s before retry {attempt+2}/{retry_attempts}...")
                time.sleep(wait_seconds)
                continue
            print(f"Error extracting tags for {item.get('name', 'unknown')}: {e}")
            return None


def batch_extract_tags(
    items: List[Dict],
    save_path: str = None,
    resume: bool = True
) -> Dict[str, List[str]]:
    """
    Extract tags for a batch of items with caching.
    
    Args:
        items: List of item dicts
        save_path: Path to save/resume from (optional)
        resume: If True, load existing tags and continue
    
    Returns:
        {item_id: [tags]}
    """
    item_tags = {}
    
    # Load existing cache if resuming
    if resume and save_path:
        try:
            with open(save_path) as f:
                item_tags = json.load(f)
            print(f"Resuming from cache: {len(item_tags)} items already tagged")
        except FileNotFoundError:
            pass
    
    for i, item in enumerate(items):
        item_id = item.get("id") or item.get("business_id")
        
        if not item_id:
            print(f"Skipping item without ID: {item.get('name')}")
            continue
        
        # Skip only if already processed with non-empty tags
        if item_id in item_tags and item_tags[item_id]:
            continue
        
        tags = extract_tags_for_item(item)
        if tags is None:
            print(f"[{i+1}/{len(items)}] {item.get('name', 'unknown')}: extraction failed, will retry later")
            continue
        
        item_tags[item_id] = tags
        
        print(f"[{i+1}/{len(items)}] {item.get('name', 'unknown')}: {tags}")
        
        # Save checkpoint every 10 items
        if save_path and (i + 1) % 10 == 0:
            with open(save_path, 'w') as f:
                json.dump(item_tags, f, indent=2)
    
    # Final save
    if save_path:
        with open(save_path, 'w') as f:
            json.dump(item_tags, f, indent=2)
        print(f"Saved {len(item_tags)} item tags to {save_path}")
    
    return item_tags