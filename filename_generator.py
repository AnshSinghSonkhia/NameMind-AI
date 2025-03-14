from keybert import KeyBERT

kw_model = KeyBERT()

def generate_name(content, image_labels=None):
    """Generate filename from content and image labels"""
    components = []
    
    # Add image labels
    if image_labels:
        components.extend([label.replace(" ", "_") for label in image_labels])
    
    # Extract text keywords
    if content:
        keywords = kw_model.extract_keywords(
            content,
            keyphrase_ngram_range=(1, 2),
            stop_words='english'
        )
        components.extend([kw[0] for kw in keywords])
    
    # Clean and format
    seen = set()
    filtered = []
    for item in components:
        clean = "".join([c if c.isalnum() or c == '_' else '_' for c in item.lower()])
        if clean not in seen and len(clean) > 1:
            seen.add(clean)
            filtered.append(clean)
    
    return "_".join(filtered[:8])[:50] or "untitled"