"""
Pure Python fallback implementation for fast operations.
Used if native Cython binary extensions are not compiled.
"""

def fast_levenshtein_distance(s1: str, s2: str) -> int:
    """Computes Levenshtein distance using standard DP row swapping."""
    if len(s1) < len(s2):
        return fast_levenshtein_distance(s2, s1)

    if len(s2) == 0:
        return len(s1)

    previous_row = list(range(len(s2) + 1))
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]


def fast_token_similarity(s1: str, s2: str) -> float:
    """Computes token Jaccard similarity in Python."""
    if s1 == s2:
        return 1.0
    w1 = set(s1.lower().split())
    w2 = set(s2.lower().split())
    if not w1 and not w2:
        return 1.0
    if not w1 or not w2:
        return 0.0
    inter = len(w1.intersection(w2))
    union = len(w1.union(w2))
    return inter / union if union > 0 else 0.0


def get_cython_engine_status():
    """Returns fallback status."""
    return {
        "compiled": False,
        "engine": "Pure Python Fallback",
        "optimizations": ["standard-interpreter"],
    }
