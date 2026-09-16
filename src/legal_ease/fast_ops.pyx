# cython: language_level=3
# cython: boundscheck=False
# cython: wraparound=False
# cython: cdivision=True

from libc.stdlib cimport malloc, free

def fast_levenshtein_distance(str s1, str s2):
    """
    Computes Levenshtein distance between two strings in pure C with dynamic memory allocation.
    Highly optimized with O(min(m,n)) space complexity.
    """
    cdef Py_ssize_t len1 = len(s1)
    cdef Py_ssize_t len2 = len(s2)

    if len1 == 0:
        return len2
    if len2 == 0:
        return len1

    # Ensure s1 is the shorter string for space optimization
    if len1 > len2:
        s1, s2 = s2, s1
        len1, len2 = len2, len1

    cdef int *current_row = <int *>malloc((len1 + 1) * sizeof(int))
    cdef int *previous_row = <int *>malloc((len1 + 1) * sizeof(int))
    
    if not current_row or not previous_row:
        if current_row:
            free(current_row)
        if previous_row:
            free(previous_row)
        raise MemoryError("Failed to allocate memory for Levenshtein computation")

    cdef Py_ssize_t i, j
    cdef int cost, add, delete, change
    cdef Py_UCS4 c1, c2

    for i in range(len1 + 1):
        previous_row[i] = i

    for j in range(1, len2 + 1):
        c2 = ord(s2[j - 1])
        current_row[0] = j

        for i in range(1, len1 + 1):
            c1 = ord(s1[i - 1])
            cost = 0 if c1 == c2 else 1
            add = previous_row[i] + 1
            delete = current_row[i - 1] + 1
            change = previous_row[i - 1] + cost

            if add < delete:
                current_row[i] = add if add < change else change
            else:
                current_row[i] = delete if delete < change else change

        for i in range(len1 + 1):
            previous_row[i] = current_row[i]

    cdef int result = current_row[len1]
    free(current_row)
    free(previous_row)
    return result


def fast_token_similarity(str s1, str s2):
    """
    Computes token-based Jaccard similarity between two texts.
    Returns float from 0.0 (disjoint) to 1.0 (identical).
    """
    if s1 == s2:
        return 1.0

    cdef list words1 = s1.lower().split()
    cdef list words2 = s2.lower().split()

    if not words1 and not words2:
        return 1.0
    if not words1 or not words2:
        return 0.0

    cdef set set1 = set(words1)
    cdef set set2 = set(words2)

    cdef Py_ssize_t intersection_len = len(set1.intersection(set2))
    cdef Py_ssize_t union_len = len(set1.union(set2))

    if union_len == 0:
        return 0.0
    return <float>intersection_len / <float>union_len


def get_cython_engine_status():
    """Returns confirmation that native C extensions are compiled and active."""
    return {
        "compiled": True,
        "engine": "Cython C-Extension (-O3 Native)",
        "optimizations": ["boundscheck=False", "wraparound=False", "ffast-math"],
    }
