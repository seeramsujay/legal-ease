"""
Pure Python Fallback Implementation for Fast Operations.
Used when native Cython C-binary extensions are not compiled in the runtime environment.
Guarantees 100% mathematical parity with the Cython C-implementation while maintaining
portable execution across arbitrary platforms.
"""

from typing import Dict, Any, Optional


def fast_levenshtein_distance(s1: Optional[str], s2: Optional[str]) -> int:
    """
    Computes Levenshtein edit distance using dynamic programming with O(min(m, n)) space.
    Defensively handles None and empty string inputs.
    """
    str1 = s1 if s1 is not None else ""
    str2 = s2 if s2 is not None else ""

    if len(str1) < len(str2):
        return fast_levenshtein_distance(str2, str1)

    if len(str2) == 0:
        return len(str1)

    previous_row = list(range(len(str2) + 1))
    for i, c1 in enumerate(str1):
        current_row = [i + 1]
        for j, c2 in enumerate(str2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]


def fast_token_similarity(s1: Optional[str], s2: Optional[str]) -> float:
    """
    Computes token-based Jaccard similarity between two texts.
    Returns a float from 0.0 (disjoint) to 1.0 (identical token sets).
    """
    str1 = s1 if s1 is not None else ""
    str2 = s2 if s2 is not None else ""

    if str1 == str2:
        return 1.0

    w1 = set(str1.lower().split())
    w2 = set(str2.lower().split())

    if not w1 and not w2:
        return 1.0
    if not w1 or not w2:
        return 0.0

    inter = len(w1.intersection(w2))
    union = len(w1.union(w2))
    return float(inter) / float(union) if union > 0 else 0.0


def get_cython_engine_status() -> Dict[str, Any]:
    """Returns fallback status when native C-binaries are not loaded."""
    return {
        "compiled": False,
        "engine": "Pure Python Fallback",
        "optimizations": ["standard-interpreter"],
    }
