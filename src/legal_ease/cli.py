"""
Command Line Interface for Legal-Ease.
Allows developers and users to analyze, compare, and redact contracts directly from the shell.
"""

import sys
import argparse
from legal_ease.pipeline import LegalAnalysisPipeline
from legal_ease.comparator import ContractComparator
from legal_ease.anonymizer import PIIAnonymizer
from legal_ease.sample_contracts import get_all_samples


def main():
    parser = argparse.ArgumentParser(
        prog="legal-ease",
        description="Legal-Ease: Privacy-First AI Legal Navigator & Contract Risk Analyzer",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

    # Analyze subcommand
    analyze_parser = subparsers.add_parser("analyze", help="Analyze a contract file")
    analyze_parser.add_argument("file", help="Path to contract text file")
    analyze_parser.add_argument(
        "--checklist", action="store_true", help="Print the attorney checklist markdown"
    )

    # Compare subcommand
    compare_parser = subparsers.add_parser("compare", help="Compare two contract versions")
    compare_parser.add_argument("file1", help="Path to base/original contract file")
    compare_parser.add_argument("file2", help="Path to revised contract file")

    # Anonymize subcommand
    anon_parser = subparsers.add_parser("anonymize", help="Test local PII redaction on a contract")
    anon_parser.add_argument("file", help="Path to contract text file")

    # Samples subcommand
    subparsers.add_parser("samples", help="List bundled sample contracts")

    # Serve subcommand
    serve_parser = subparsers.add_parser("serve", help="Launch the Web Application server")
    serve_parser.add_argument("--port", type=int, default=8000, help="Port to bind (default: 8000)")
    serve_parser.add_argument("--host", default="0.0.0.0", help="Host address (default: 0.0.0.0)")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    if args.command == "samples":
        samples = get_all_samples()
        print("\n📂 Bundled Realistic Contract Samples:")
        for s in samples:
            print(f"  • [{s.id}] {s.title} ({s.category})")
        print("\nTip: Run 'legal-ease serve' to explore these samples in the interactive web UI.\n")
        return

    if args.command == "analyze":
        try:
            with open(args.file, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception as e:
            print(f"Error reading {args.file}: {e}", file=sys.stderr)
            sys.exit(1)

        pipeline = LegalAnalysisPipeline()
        res = pipeline.analyze(content)

        print("\n" + "=" * 60)
        print(f"⚖️ LEGAL-EASE CONTRACT ANALYSIS: {args.file}")
        print("=" * 60)
        print(f"Legal Risk Index: {res.risk_overview.legal_risk_index}/100 [{res.risk_overview.risk_level.value}]")
        print(f"Clauses Analyzed: {res.risk_overview.total_clauses}")
        print(f"High Risk: {res.risk_overview.high_risk_count} | Medium Risk: {res.risk_overview.medium_risk_count} | Low Risk: {res.risk_overview.low_risk_count}")
        print(f"PII Redactions: {len(res.anonymization.entities)} sensitive entities masked locally")
        print("\nExecutive Summary:")
        print(res.risk_overview.executive_summary)

        print("\nTop Critical Flags:")
        for flag in res.risk_overview.critical_findings:
            print(f"  🚨 {flag}")

        if args.checklist:
            print("\n" + "=" * 60)
            print("ATTORNEY BRIEFING CHECKLIST:")
            print("=" * 60)
            print(res.attorney_checklist.markdown_report)
        return

    if args.command == "compare":
        try:
            with open(args.file1, "r", encoding="utf-8") as f1, open(args.file2, "r", encoding="utf-8") as f2:
                c1 = f1.read()
                c2 = f2.read()
        except Exception as e:
            print(f"Error reading files: {e}", file=sys.stderr)
            sys.exit(1)

        comparator = ContractComparator()
        res = comparator.compare(c1, c2, title_v1=args.file1, title_v2=args.file2)

        print("\n" + "=" * 60)
        print("⚖️ LEGAL-EASE CONTRACT COMPARISON")
        print("=" * 60)
        print(f"Base Version:    {res.risk_index_v1}/100")
        print(f"Revised Version: {res.risk_index_v2}/100")
        print(f"Risk Delta:      {res.risk_index_delta:+d} points ({res.trajectory})")
        print("\nSummary of Key Changes:")
        for ch in res.summary_of_changes:
            print(f"  • {ch}")
        return

    if args.command == "anonymize":
        try:
            with open(args.file, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception as e:
            print(f"Error reading {args.file}: {e}", file=sys.stderr)
            sys.exit(1)

        anon = PIIAnonymizer()
        res = anon.anonymize(content)
        print("\n🛡️ PII ANONYMIZATION AUDIT:")
        print(f"Total Sensitive Entities Redacted: {len(res.entities)}")
        print(f"Breakdown: {res.entity_counts}")
        print("\nRedacted Text Preview (first 500 chars):")
        print("-" * 40)
        print(res.redacted_text[:500] + "...")
        print("-" * 40)
        return

    if args.command == "serve":
        import uvicorn
        print(f"🚀 Starting Legal-Ease Web Dashboard on http://{args.host}:{args.port}")
        uvicorn.run("legal_ease.main:app", host=args.host, port=args.port, reload=False)


if __name__ == "__main__":
    main()
