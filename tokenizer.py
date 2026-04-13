def tokenize_phi(text: str, entities: list) -> dict:
    """Replace PHI spans with {{label_N}} tokens.

    Args:
        text: Original text.
        entities: List of dicts with keys: text, label, start, end.

    Returns:
        {"content": str, "phi": dict} where phi maps token names to original values.
    """
    # Build dedup map: (label, value) -> token name
    dedup: dict[tuple, str] = {}
    # Per-label counter
    counters: dict[str, int] = {}

    # Sort by start position to assign token names in document order
    sorted_entities = sorted(entities, key=lambda e: e["start"])

    for entity in sorted_entities:
        key = (entity["label"], entity["text"])
        if key not in dedup:
            label = entity["label"]
            counters[label] = counters.get(label, 0) + 1
            dedup[key] = f"{label}_{counters[label]}"

    # Build phi map: token name -> original value
    phi = {token: value for (_, value), token in dedup.items()}

    # Replace from end to start so earlier positions aren't shifted
    content = text
    for entity in sorted(sorted_entities, key=lambda e: e["start"], reverse=True):
        token = dedup[(entity["label"], entity["text"])]
        content = content[: entity["start"]] + "{{" + token + "}}" + content[entity["end"] :]

    return {"content": content, "phi": phi}
