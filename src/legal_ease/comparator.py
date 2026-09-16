"""
Contract diffing and version comparison engine.
Calculates liability deltas, identifies stealth clause alterations,
and computes overall contractual trajectory (SAFER / MORE_RISK / NEUTRAL).
Accelerated by native Cython C-extensions when available.
"""

from typing import List, Dict, Tuple, Optional
from legal_ease.clause_segmenter import ClauseSegmenter, RawClause
from legal_ease.risk_analyzer import RiskAnalyzer
from legal_ease.fast_ops_bridge import compute_similarity, is_cython_accelerated
from legal_ease.guardrails import get_standard_disclaimer
from legal_ease.models import (
    ContractComparisonResponse,
    ClauseDiff,
    DiffChangeType,
)


class ContractComparator:
    """
    Compares two contracts (e.g., Original vs Counter-Proposal),
    aligning clauses by semantic similarity, identifying additions,
    deletions, and modifications, and scoring risk delta.
    """

    def __init__(self):
        self.segmenter = ClauseSegmenter()
        self.analyzer = RiskAnalyzer()

    def compare(
        self,
        text_v1: Optional[str] = None,
        text_v2: Optional[str] = None,
        title_v1: str = "Original Version",
        title_v2: str = "Revised Proposal",
        doc_v1_text: Optional[str] = None,
        doc_v2_text: Optional[str] = None,
    ) -> ContractComparisonResponse:
        """Execute full comparison and trajectory analysis between two drafts."""
        v1 = text_v1 if text_v1 is not None else (doc_v1_text or "")
        v2 = text_v2 if text_v2 is not None else (doc_v2_text or "")

        clauses_v1 = self.segmenter.segment(v1)
        clauses_v2 = self.segmenter.segment(v2)

        evals_v1 = [self.analyzer.evaluate_clause(c) for c in clauses_v1]
        evals_v2 = [self.analyzer.evaluate_clause(c) for c in clauses_v2]

        overview_v1 = self.analyzer.calculate_overview(evals_v1)
        overview_v2 = self.analyzer.calculate_overview(evals_v2)

        risk_delta = overview_v2.legal_risk_index - overview_v1.legal_risk_index

        if risk_delta <= -8:
            trajectory = "SAFER"
        elif risk_delta >= 8:
            trajectory = "MORE_RISK"
        else:
            trajectory = "NEUTRAL"

        clause_diffs: List[ClauseDiff] = []
        matched_v2_indices = set()
        summary_of_changes: List[str] = []

        for i, c1 in enumerate(clauses_v1):
            e1 = evals_v1[i]
            # Find best match in v2
            best_match_idx = None
            best_sim = 0.0

            for j, c2 in enumerate(clauses_v2):
                if j in matched_v2_indices:
                    continue
                # Calculate similarity via accelerated Cython engine
                sim = self._text_similarity(c1.text, c2.text)
                if c1.category == c2.category:
                    sim += 0.25
                if sim > best_sim and sim >= 0.40:
                    best_sim = sim
                    best_match_idx = j

            if best_match_idx is not None:
                matched_v2_indices.add(best_match_idx)
                c2 = clauses_v2[best_match_idx]
                e2 = evals_v2[best_match_idx]
                c_delta = e2.risk_score - e1.risk_score

                if c1.text.strip() == c2.text.strip():
                    change_type = DiffChangeType.UNCHANGED
                    notes = "Clause terms remain identical between versions."
                else:
                    change_type = DiffChangeType.MODIFIED
                    if c_delta < 0:
                        notes = f"Favorable modification: Risk decreased by {abs(c_delta)} points."
                    elif c_delta > 0:
                        notes = f"Unfavorable modification: Risk increased by {c_delta} points."
                    else:
                        notes = "Wording adjusted with neutral risk impact."

                    summary_of_changes.append(
                        f"Modified '{c1.title}': {notes}"
                    )

                clause_diffs.append(
                    ClauseDiff(
                        section_title=c1.title,
                        category=c1.category.value,
                        change_type=change_type,
                        text_v1=c1.text,
                        text_v2=c2.text,
                        risk_score_v1=e1.risk_score,
                        risk_score_v2=e2.risk_score,
                        risk_delta=c_delta,
                        analysis_notes=notes,
                    )
                )
            else:
                # Clause in v1 was removed in v2
                summary_of_changes.append(
                    f"Removed '{c1.title}' (was {e1.risk_score} risk points in v1)."
                )
                clause_diffs.append(
                    ClauseDiff(
                        section_title=c1.title,
                        category=c1.category.value,
                        change_type=DiffChangeType.REMOVED,
                        text_v1=c1.text,
                        text_v2=None,
                        risk_score_v1=e1.risk_score,
                        risk_score_v2=None,
                        risk_delta=-e1.risk_score,
                        analysis_notes="Clause was deleted from the revised version.",
                    )
                )

        # Catch newly added clauses in v2
        for j, c2 in enumerate(clauses_v2):
            if j not in matched_v2_indices:
                e2 = evals_v2[j]
                summary_of_changes.append(
                    f"Added new clause '{c2.title}' with risk score of {e2.risk_score}/100."
                )
                clause_diffs.append(
                    ClauseDiff(
                        section_title=c2.title,
                        category=c2.category.value,
                        change_type=DiffChangeType.ADDED,
                        text_v1=None,
                        text_v2=c2.text,
                        risk_score_v1=None,
                        risk_score_v2=e2.risk_score,
                        risk_delta=e2.risk_score,
                        analysis_notes="New clause introduced in the revised version.",
                    )
                )

        if not summary_of_changes:
            summary_of_changes.append("No significant structural or textual alterations detected.")

        return ContractComparisonResponse(
            document_title_v1=title_v1,
            document_title_v2=title_v2,
            disclaimer=get_standard_disclaimer(),
            risk_index_v1=overview_v1.legal_risk_index,
            risk_index_v2=overview_v2.legal_risk_index,
            risk_index_delta=risk_delta,
            trajectory=trajectory,
            summary_of_changes=summary_of_changes,
            clause_diffs=clause_diffs,
        )

    def _text_similarity(self, a: str, b: str) -> float:
        """High-performance Jaccard similarity via Cython or Python fallback."""
        return compute_similarity(a, b)
