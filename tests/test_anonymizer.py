"""
Unit tests for the PII and Sensitive Entity Anonymizer.
"""

from legal_ease.anonymizer import PIIAnonymizer


def test_email_redaction():
    anon = PIIAnonymizer()
    text = "Please send invoices to john.doe@enterprise.com and cc finance-ops@billing.org."
    res = anon.anonymize(text)
    assert "[EMAIL_1]" in res.redacted_text
    assert "[EMAIL_2]" in res.redacted_text
    assert "john.doe@enterprise.com" not in res.redacted_text
    assert "finance-ops@billing.org" not in res.redacted_text
    assert res.entity_counts["EMAIL"] == 2


def test_ssn_and_ein_redaction():
    anon = PIIAnonymizer()
    text = "Contractor SSN is 123-45-6789 and Employer EIN is 12-3456789."
    res = anon.anonymize(text)
    assert "[TAX_ID_1]" in res.redacted_text
    assert "[TAX_ID_2]" in res.redacted_text
    assert "123-45-6789" not in res.redacted_text
    assert "12-3456789" not in res.redacted_text


def test_financial_amounts_redaction():
    anon = PIIAnonymizer()
    text = "Total consulting fee shall be $125,000 USD, with a milestone deposit of $25,000."
    res = anon.anonymize(text)
    assert "[CONFIDENTIAL_AMOUNT_1]" in res.redacted_text
    assert "[CONFIDENTIAL_AMOUNT_2]" in res.redacted_text
    assert "$125,000" not in res.redacted_text


def test_phone_and_address_redaction():
    anon = PIIAnonymizer()
    text = "Contact Alice at (512) 555-0199 or visit our office at 123 Market Street, Suite 400, Austin, TX 78701."
    res = anon.anonymize(text)
    assert "[PHONE_1]" in res.redacted_text
    assert "[ADDRESS_1]" in res.redacted_text
    assert "(512) 555-0199" not in res.redacted_text


def test_deanonymization_restoration():
    anon = PIIAnonymizer()
    original = "Payment of $50,000 to user@example.com for services at 100 Main St."
    res = anon.anonymize(original)
    assert "[CONFIDENTIAL_AMOUNT_1]" in res.redacted_text

    restored = anon.deanonymize(res.redacted_text, res.entities)
    assert restored == original


def test_empty_string():
    anon = PIIAnonymizer()
    res = anon.anonymize("")
    assert res.redacted_text == ""
    assert len(res.entities) == 0
    assert res.privacy_score == 100.0
