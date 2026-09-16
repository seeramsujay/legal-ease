"""
Side-by-side contract comparison and liability shift analyzer.
Aligns clauses between contract revisions and highlights modified terms and risk shifts.
"""

import difflib
from typing import List, Dict, Optional
from legal_ease.models import (
    ContractComparisonResponse,
    ClauseDiff,
    DiffChangeType,
)
from legal_ease.clause_segmenter import ClauseSegmenter, RawClause
from legal_ease.risk_analyzer import RiskAnalyzer
from legal_ease.guardrails import get_standard_disclaimer


class ContractComparator:
    """
    Compares two contract versions (e.g. Original vs Counter-Proposal),
    identifying added, deleted, or modified obligations and scoring risk divergence.
    """

    def __init__(self):
        self.segmenter = ClauseSegmenter()
        self.analyzer = RiskAnalyzer()

    def compare(
        self,
        doc_v1_text: str,
        doc_v2_text: str,
        title_v1: str = "Original Version",
        title_v2: str = "Revised Proposal",
    ) -> ContractComparisonResponse:
        """
        Segment both versions, align clauses by title/category, and compute diffs and risk deltas.
        """
        clauses_v1 = self.segmenter.segment(doc_v1_text)
        clauses_v2 = self.segmenter.segment(doc_v2_text)

        evals_v1 = [self.analyzer.evaluate_clause(c) for c in clauses_v1]
        evals_v2 = [self.analyzer.evaluate_clause(c) for c in clauses_v2]

        overview_v1 = self.analyzer.calculate_overview(evals_v1)
        overview_v2 = self.analyzer.calculate_overview(evals_v2)

        risk_delta = overview_v2.legal_risk_index - overview_v1.legal_risk_index
        if risk_delta > 5:
            trajectory = "MORE_RISK"
        elif risk_delta < -5:
            trajectory = "SAFER"
        else:
            trajectory = "NEUTRAL"

        # Align clauses
        clause_diffs: List[ClauseDiff] = []
        summary_of_changes: List[str] = []

        # Map by normalized title/category
        v1_dict: Dict[str, Tuple[RawClause, int]] = {
            self._key(c): (c, evals_v1[i].risk_score) for i, c in enumerate(clauses_v1)
        }
        v2_dict: Dict[str, Tuple[RawClause, int]] = {
            self._key(c): (c, evals_v2[i].risk_score) for i, c in enumerate(clauses_v2)
        }

        matched_v2_keys = set()

        # Check all clauses from v1
        for k, (c1, score1) in v1_dict.items():
            if k in v2_dict:
                c2, score2 = v2_dict[k]
                matched_v2_keys.add(k)
                delta = score2 - score1

                # Check text similarity
                similarity = difflib.SequenceMatcher(None, c1.text, c2.text).ratio()

                if similarity > 0.98:
                    change_type = DiffChangeType.UNCHANGED
                    notes = "Clause text is substantially identical."
                else:
                    change_type = DiffChangeType.MODIFIED
                    if delta > 10:
                        notes = f"Significantly altered (+{delta} risk pts): Increased burden or liability exposure."
                        summary_of_changes.append(
                            f"Section '{c2.title}': Language modified, increasing risk from {score1} to {score2}."
                        )
                    elif delta < -10:
                        notes = f"Favorable modification ({delta} risk pts): Improved protections or reduced exposure."
                        summary_of_changes.append(
                            f"Section '{c2.title}': Language improved, lowering risk from {score1} to {score2}."
                        )
                    else:
                        notes = "Clause language tweaked with minor risk impact."

                clause_diffs.append(
                    ClauseDiff(
                        section_title=c2.title,
                        category=c2.category.value,
                        change_type=change_type,
                        text_v1=c1.text,
                        text_v2=c2.text,
                        risk_score_v1=score1,
                        risk_score_v2=score2,
                        risk_delta=delta,
                        analysis_notes=notes,
                    )
                )
            else:
                # Removed from v2
                summary_of_changes.append(f"Section '{c1.title}' was REMOVED in the revised draft.")
                clause_diffs.append(
                    ClauseDiff(
                        section_title=c1.title,
                        category=c1.category.value,
                        change_type=DiffChangeType.REMOVED,
                        text_v1=c1.text,
                        text_v2=None,
                        risk_score_v1=score1,
                        risk_score_v2=None,
                        risk_delta=-score1,
                        analysis_notes="Clause was omitted from the revised agreement.",
                    )
                )

        # Check clauses newly added in v2
        for k, (c2, score2) in v2_dict.items():
            if k not in matched_v2_keys:
                summary_of_changes.append(
                    f"Section '{c2.title}' was ADDED in the revised draft (Risk score: {score2})."
                )
                clause_diffs.append(
                    ClauseDiff(
                        section_title=c2.title,
                        category=c2.category.value,
                        change_type=DiffChangeType.ADDED,
                        text_v1=None,
                        text_v2=c2.text,
                        risk_score_v1=None,
                        risk_score_v2=score2,
                        risk_delta=score2,
                        analysis_notes=f"New provision inserted with risk score {score2}.",
                    )
                )

        if not summary_of_changes:
            summary_of_changes.append("No significant structural or risk changes detected between versions.")

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

    def _key(self, clause: RawClause) -> str:
        """Create a normalized key for matching clauses between revisions."""
        norm_title = "".join(c for c in clause.title.lower() if c.isalnum() or c.isspace())
        tokens = [t for t in norm_title.split() if not t.isdigit() and len(t) > 2]
        return f"{clause.category.value}_{'_'.join(tokens[:3])}"
