"""
Intelligent Semantic Vector & Obfuscation Analysis Engine.
Detects twisted, euphemistic, or obfuscated legal language by projecting clauses
into high-dimensional sub-word n-gram vector spaces and computing cosine similarities
against predatory legal archetypes. Flags clauses disguised by deceptive drafting
to trigger automated LLM escalation.
"""

import math
import re
from typing import Dict, List, Tuple, Optional, Pattern, Any
from pydantic import BaseModel, Field


class SemanticArchetype:
    """Canonical archetype identifiers representing predatory contract strategies."""
    UNILATERAL_INDEMNITY = "unilateral_indemnity"
    ASYMMETRIC_LIABILITY = "asymmetric_liability"
    STEALTH_NON_COMPETE = "stealth_non_compete"
    DISCRETIONARY_TERMINATION = "discretionary_termination"
    PREEXISTING_IP_FORFEITURE = "preexisting_ip_forfeiture"
    EXTREME_PAYMENT_WITHHOLDING = "extreme_payment_withholding"
    MANDATORY_DISPUTE_SURRENDER = "mandatory_dispute_surrender"
    EUPHEMISTIC_BOILERPLATE_TRAP = "euphemistic_boilerplate_trap"


# Comprehensive legal reference corpora representing predatory contract strategies.
ARCHETYPE_DESCRIPTIONS: Dict[str, str] = {
    SemanticArchetype.UNILATERAL_INDEMNITY: (
        "hold harmless defend and insulate counterparty from any and all claims liabilities losses "
        "damages proceedings expenses attorney legal costs fees arising out of or related to engagement "
        "without reciprocal protection or bilateral defense obligation"
    ),
    SemanticArchetype.ASYMMETRIC_LIABILITY: (
        "counterparty aggregate total maximum liability strictly circumscribed limited to nominal token sum "
        "or fees paid in preceding month whereas contractor consultant recipient liability remains completely "
        "uncapped unmitigated unbounded with no exclusion of consequential damages"
    ),
    SemanticArchetype.STEALTH_NON_COMPETE: (
        "refrain abstain from directly indirectly rendering assistance counsel guidance expertise "
        "or participating in any entity venture commercial domain territory worldwide in perpetuity "
        "or extended multi-year duration following cessation of services"
    ),
    SemanticArchetype.DISCRETIONARY_TERMINATION: (
        "sole discretion unreviewable prerogative absolute authority to terminate discontinue cease "
        "forthwith immediately without cause reason preliminary notice or opportunity to cure any alleged deficiency"
    ),
    SemanticArchetype.PREEXISTING_IP_FORFEITURE: (
        "irrevocably assign cede transfer convey relinquish all rights title interest in any and all "
        "inventions tools libraries code frameworks background methodologies moral rights whenever conceived "
        "throughout universe in perpetuity without exclusion of prior property"
    ),
    SemanticArchetype.EXTREME_PAYMENT_WITHHOLDING: (
        "payment terms net sixty ninety one hundred twenty days counterparty reserves right to withhold "
        "disallow offset fees based on subjective satisfaction sole unreviewable acceptance criteria"
    ),
    SemanticArchetype.MANDATORY_DISPUTE_SURRENDER: (
        "waive right to jury trial court adjudication participate in class collective consolidated action "
        "submit exclusively to confidential binding arbitration at designated remote counterparty venue"
    ),
    SemanticArchetype.EUPHEMISTIC_BOILERPLATE_TRAP: (
        "notwithstanding anything to contrary in agreement or any statement of work survivor clauses "
        "draconian covenants remain in full force effect in perpetuity without right of setoff or recourse"
    ),
}

# Pre-compiled regex patterns for deceptive euphemisms used by predatory drafters.
# Pre-compilation at module import achieves O(1) regex construction overhead.
_EUPHEMISM_DEFINITIONS: List[Tuple[str, str, float]] = [
    (r"hold\s+harmless\s+(?:and\s+defend\s+)?(?:\w+\s+)*(?:from|against|without\s+limitation)", "Euphemistic Indemnity Shield", 0.45),
    (r"at\s+(?:its|company's?|client's?)\s+(?:sole|unreviewable|absolute)\s+(?:prerogative|discretion|determination)", "Unreviewable Discretion", 0.40),
    (r"without\s+necessity\s+of\s+(?:prior\s+notice|cause|demonstrating\s+breach)", "Zero-Notice Deprivation", 0.40),
    (r"in\s+perpetuity\s+(?:throughout|across)\s+the\s+(?:universe|world)", "Perpetual Rights Extinguishment", 0.50),
    (r"conveys?,\s+cedes?,\s+(?:and\s+)?relinquishes?", "Surrender of Rights", 0.40),
    (r"remedies\s+shall\s+be\s+strictly\s+circumscribed", "Masked Liability Cap", 0.35),
    (r"unmitigated\s+and\s+exhaustive\s+accountability", "Uncapped Exposure", 0.45),
    (r"abstain\s+from\s+(?:rendering|participating\s+in)", "Disguised Non-Compete", 0.40),
    (r"subjective\s+(?:satisfaction|approval)\s+prior\s+to\s+disbursement", "Conditional Payment Trap", 0.40),
    (r"irrevocably\s+and\s+unconditionally\s+waives?", "Absolute Rights Forfeiture", 0.45),
    (r"without\s+recourse\s+to\s+ordinary\s+tribunals", "Court Access Deprivation", 0.40),
    (r"survives?\s+the\s+expiration\s+or\s+earlier\s+termination\s+indefinitely", "Indefinite Post-Termination Trap", 0.35),
]

# Pre-compiled tuple of (compiled_pattern, label, weight) for maximal search velocity
COMPILED_EUPHEMISMS: List[Tuple[Pattern[str], str, float]] = [
    (re.compile(pat, re.IGNORECASE), label, weight)
    for pat, label, weight in _EUPHEMISM_DEFINITIONS
]

# Pre-compiled tokenizers and syntactic complexity splitters
_WORD_TOKEN_PATTERN = re.compile(r"\b[a-z]{3,}\b")
_SENTENCE_SPLIT_PATTERN = re.compile(r"[.;:]+")
_NESTING_PATTERN = re.compile(
    r"(?:provided\s+(?:however|that)|notwithstanding\s+the\s+foregoing|in\s+the\s+event\s+that)",
    re.IGNORECASE,
)


class SemanticClauseInsight(BaseModel):
    """Linguistic and vector-space telemetry resulting from semantic analysis."""
    is_twisted: bool = Field(default=False, description="Whether twisted or euphemistic drafting was detected")
    obfuscation_score: float = Field(default=0.0, description="Obfuscation / complexity index from 0.0 (clear) to 1.0 (heavily disguised)")
    archetype_scores: Dict[str, float] = Field(default_factory=dict, description="Cosine similarity to each trap archetype")
    top_archetype: Optional[str] = Field(default=None, description="Dominant predatory archetype detected")
    top_archetype_similarity: float = Field(default=0.0, description="Cosine similarity score of top archetype match")
    detected_euphemisms: List[str] = Field(default_factory=list, description="Specific euphemistic deceptive phrases detected")
    escalation_recommended: bool = Field(default=False, description="Whether complexity and obfuscation mandate LLM escalation")
    explanation: Optional[str] = Field(default=None, description="Detailed explanation of the linguistic disguise")


class SemanticVectorModel:
    """
    High-Performance Sub-word N-gram & Term Frequency Vector Space Model.
    
    Mathematical Formulation:
    - Normalizes token sequences and extracts sub-word 4-gram and 5-gram roots.
    - Computes L2-normalized vector representations: v_norm = v / ||v||_2.
    - Evaluates Cosine Similarity via inner product: sim(u, v) = u . v.
    - Benchmarks incoming clauses against pre-indexed predatory legal archetypes in O(|tokens|) time.
    """

    def __init__(self) -> None:
        # Precompute archetype vectors once during singleton initialization
        self.archetype_vectors: Dict[str, Dict[str, float]] = {}
        for name, text in ARCHETYPE_DESCRIPTIONS.items():
            self.archetype_vectors[name] = self._vectorize(text)

    def _tokenize(self, text: Optional[str]) -> List[str]:
        """
        Extracts lowercase words and appends character 4-gram and 5-gram stems.
        Enables robust matching against morphological variations (e.g. 'indemnif' -> 'indemn', 'indem').
        """
        if not text:
            return []
            
        words = _WORD_TOKEN_PATTERN.findall(text.lower())
        tokens: List[str] = list(words)
        
        for w in words:
            w_len = len(w)
            if w_len >= 5:
                tokens.append(w[:4])
                tokens.append(w[:5])
        return tokens

    def _vectorize(self, text: Optional[str]) -> Dict[str, float]:
        """
        Transforms text into an L2-normalized sparse vector mapping token -> weight.
        Guarantees ||v||_2 = 1.0 for non-empty vectors.
        """
        tokens = self._tokenize(text)
        if not tokens:
            return {}
            
        counts: Dict[str, int] = {}
        for t in tokens:
            counts[t] = counts.get(t, 0) + 1

        # Calculate Euclidean (L2) Norm: sqrt(sum(c_i^2))
        sq_sum = sum(c * c for c in counts.values())
        norm = math.sqrt(sq_sum) if sq_sum > 0 else 1.0
        
        return {t: float(c) / norm for t, c in counts.items()}

    def cosine_similarity(self, vec1: Dict[str, float], vec2: Dict[str, float]) -> float:
        """
        Computes cosine similarity between two L2-normalized sparse vectors.
        Optimized to iterate over the smaller vector for minimal dictionary lookups.
        """
        if not vec1 or not vec2:
            return 0.0
            
        # Swap so vec1 is always the smaller map to minimize loop iterations
        if len(vec1) > len(vec2):
            vec1, vec2 = vec2, vec1
            
        dot_product = sum(weight * vec2.get(token, 0.0) for token, weight in vec1.items())
        return max(0.0, min(1.0, dot_product))

    def evaluate_semantics(self, text: Optional[str], section_title: Optional[str] = "") -> SemanticClauseInsight:
        """
        Evaluates a contract clause for predatory semantics, euphemistic drafting, and obfuscation.
        Returns detailed insight including archetype similarities and escalation flags.
        """
        safe_text = str(text) if text is not None else ""
        safe_title = str(section_title) if section_title is not None else ""
        
        full_text = f"{safe_title} {safe_text}".lower()
        clause_vec = self._vectorize(full_text)

        # 1. Cosine similarity against all predatory archetypes
        archetype_scores: Dict[str, float] = {}
        top_archetype: Optional[str] = None
        top_sim: float = 0.0

        for name, arch_vec in self.archetype_vectors.items():
            sim = self.cosine_similarity(clause_vec, arch_vec)
            rounded_sim = round(sim, 3)
            archetype_scores[name] = rounded_sim
            if sim > top_sim:
                top_sim = sim
                top_archetype = name

        # 2. Match deceptive euphemisms using pre-compiled regex objects
        detected_euphemisms: List[str] = []
        euphemism_weight: float = 0.0
        for compiled_pat, label, weight in COMPILED_EUPHEMISMS:
            if compiled_pat.search(full_text):
                detected_euphemisms.append(label)
                euphemism_weight += weight

        # 3. Structural complexity analysis
        sentences = [s.strip() for s in _SENTENCE_SPLIT_PATTERN.split(safe_text) if s.strip()]
        total_sentences = max(1, len(sentences))
        avg_sentence_len = sum(len(s.split()) for s in sentences) / total_sentences
        has_deep_nesting = bool(_NESTING_PATTERN.search(full_text))

        complexity_factor = 0.0
        if avg_sentence_len > 35:
            complexity_factor += 0.25
        if has_deep_nesting:
            complexity_factor += 0.20
        if len(sentences) >= 4 and avg_sentence_len > 25:
            complexity_factor += 0.15

        # 4. Synthesize Obfuscation Score (0.0 to 1.0)
        # Combines semantic alignment with predatory archetypes (45%),
        # detected euphemisms (35%), and syntactic complexity (20%)
        raw_obfuscation = (
            (top_sim * 0.45)
            + (min(1.0, euphemism_weight) * 0.35)
            + (complexity_factor * 0.20)
        )
        obfuscation_score = round(max(0.0, min(1.0, raw_obfuscation)), 2)

        # 5. Determine if clause is twisted or deceptive
        is_twisted = (
            len(detected_euphemisms) > 0
            or top_sim >= 0.50
            or (top_sim >= 0.35 and obfuscation_score >= 0.40)
            or (obfuscation_score >= 0.55)
        )

        # 6. LLM escalation recommendation
        escalation_recommended = is_twisted and (
            obfuscation_score >= 0.45 or top_sim >= 0.35
        )

        explanation: Optional[str] = None
        if is_twisted:
            archetype_name_clean = (
                top_archetype.replace("_", " ").title() if top_archetype else "Predatory Term"
            )
            euphemism_str = (
                f" Detected euphemistic drafting: {', '.join(detected_euphemisms)}."
                if detected_euphemisms
                else ""
            )
            explanation = (
                f"Semantic embedding vectors indicate strong alignment ({int(top_sim * 100)}%) with "
                f"{archetype_name_clean} despite evasive/obfuscated wording.{euphemism_str} "
                f"Obfuscation index: {int(obfuscation_score * 100)}%."
            )

        return SemanticClauseInsight(
            is_twisted=is_twisted,
            obfuscation_score=obfuscation_score,
            archetype_scores=archetype_scores,
            top_archetype=top_archetype,
            top_archetype_similarity=round(top_sim, 3),
            detected_euphemisms=detected_euphemisms,
            escalation_recommended=escalation_recommended,
            explanation=explanation,
        )


# Global singleton instance for high-speed reuse across requests
_semantic_model: SemanticVectorModel = SemanticVectorModel()


def get_semantic_model() -> SemanticVectorModel:
    """Returns the globally pre-computed and indexed SemanticVectorModel singleton."""
    return _semantic_model
