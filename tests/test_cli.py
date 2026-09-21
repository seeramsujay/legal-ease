"""
Unit and Integration tests for Legal-Ease Command Line Interface (CLI).
Tests all subcommands: analyze, compare, anonymize, samples, help, and error handling.
"""

import sys
import tempfile
import pytest
from legal_ease.cli import main
from legal_ease.sample_contracts import FREELANCE_HIGH_RISK, FREELANCE_NEGOTIATED


class TestCLI:
    """Test CLI commands, argument parsing, execution paths, and error handling."""

    def test_cli_no_args_prints_help(self, monkeypatch, capsys):
        monkeypatch.setattr(sys, "argv", ["legal-ease"])
        with pytest.raises(SystemExit) as exc:
            main()
        assert exc.value.code == 0
        captured = capsys.readouterr()
        assert "Legal-Ease: Privacy-First AI Legal Navigator" in captured.out

    def test_cli_samples_command(self, monkeypatch, capsys):
        monkeypatch.setattr(sys, "argv", ["legal-ease", "samples"])
        main()
        captured = capsys.readouterr()
        assert "Bundled Realistic Contract Samples:" in captured.out
        assert "freelance_high_risk" in captured.out
        assert "freelance_negotiated" in captured.out

    def test_cli_analyze_command(self, monkeypatch, capsys):
        with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False) as f:
            f.write(FREELANCE_HIGH_RISK)
            f_path = f.name

        monkeypatch.setattr(sys, "argv", ["legal-ease", "analyze", f_path])
        main()
        captured = capsys.readouterr()
        assert "LEGAL-EASE CONTRACT ANALYSIS" in captured.out
        assert "Legal Risk Index:" in captured.out
        assert "Executive Summary:" in captured.out

    def test_cli_analyze_with_checklist(self, monkeypatch, capsys):
        with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False) as f:
            f.write("1. Term. 1 year agreement.\n2. Payment. Net 30 days.")
            f_path = f.name

        monkeypatch.setattr(sys, "argv", ["legal-ease", "analyze", f_path, "--checklist"])
        main()
        captured = capsys.readouterr()
        assert "ATTORNEY BRIEFING CHECKLIST:" in captured.out
        assert "NOTICE FOR COUNSEL" in captured.out

    def test_cli_analyze_nonexistent_file_exits_1(self, monkeypatch, capsys):
        monkeypatch.setattr(sys, "argv", ["legal-ease", "analyze", "non_existent_file_12345.txt"])
        with pytest.raises(SystemExit) as exc:
            main()
        assert exc.value.code == 1
        captured = capsys.readouterr()
        assert "Error reading" in captured.err

    def test_cli_compare_command(self, monkeypatch, capsys):
        with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False) as f1, \
             tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False) as f2:
            f1.write(FREELANCE_HIGH_RISK)
            f2.write(FREELANCE_NEGOTIATED)
            p1 = f1.name
            p2 = f2.name

        monkeypatch.setattr(sys, "argv", ["legal-ease", "compare", p1, p2])
        main()
        captured = capsys.readouterr()
        assert "LEGAL-EASE CONTRACT COMPARISON" in captured.out
        assert "Base Version:" in captured.out
        assert "Revised Version:" in captured.out
        assert "Risk Delta:" in captured.out

    def test_cli_compare_nonexistent_file_exits_1(self, monkeypatch, capsys):
        monkeypatch.setattr(sys, "argv", ["legal-ease", "compare", "fake1.txt", "fake2.txt"])
        with pytest.raises(SystemExit) as exc:
            main()
        assert exc.value.code == 1
        captured = capsys.readouterr()
        assert "Error reading files" in captured.err

    def test_cli_anonymize_command(self, monkeypatch, capsys):
        with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False) as f:
            f.write("Contact Jane Doe at jane.doe@techcorp.io or (555) 019-2834.")
            f_path = f.name

        monkeypatch.setattr(sys, "argv", ["legal-ease", "anonymize", f_path])
        main()
        captured = capsys.readouterr()
        assert "PII ANONYMIZATION AUDIT:" in captured.out
        assert "Total Sensitive Entities Redacted:" in captured.out
        assert "[EMAIL_1]" in captured.out

    def test_cli_anonymize_nonexistent_file_exits_1(self, monkeypatch, capsys):
        monkeypatch.setattr(sys, "argv", ["legal-ease", "anonymize", "ghost_file.txt"])
        with pytest.raises(SystemExit) as exc:
            main()
        assert exc.value.code == 1
        captured = capsys.readouterr()
        assert "Error reading" in captured.err
