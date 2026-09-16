"""
Unit tests for the contract version comparator.
"""

from legal_ease.comparator import ContractComparator
from legal_ease.sample_contracts import FREELANCE_HIGH_RISK, FREELANCE_NEGOTIATED


def test_comparison_detects_safer_trajectory():
    comparator = ContractComparator()
    # Comparing high-risk base against contractor-friendly negotiated revision
    res = comparator.compare(
        doc_v1_text=FREELANCE_HIGH_RISK,
        doc_v2_text=FREELANCE_NEGOTIATED,
        title_v1="High Risk Draft",
        title_v2="Negotiated Draft",
    )

    assert res.risk_index_v1 > res.risk_index_v2
    assert res.trajectory == "SAFER"
    assert res.risk_index_delta < 0
    assert len(res.clause_diffs) > 0
    assert len(res.summary_of_changes) > 0


def test_comparison_identical_text():
    comparator = ContractComparator()
    text = "1. INDEMNIFICATION\nEach party indemnifies the other.\n\n2. GOVERNING LAW\nLaws of New York."
    res = comparator.compare(text, text)
    assert res.risk_index_delta == 0
    assert res.trajectory == "NEUTRAL"
