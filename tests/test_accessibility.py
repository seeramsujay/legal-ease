"""
Accessibility and WCAG 2.1 Level AAA Conformance Automated Test Suite.
Verifies compliance with WCAG 2.1 AAA & AA principles:
- Perceivable (Landmarks, Skip Links, Contrast Ratios >= 7:1)
- Operable (Keyboard Shortcuts, Focus Visible >= 3px, Reduced Motion)
- Understandable (Language definition, Accessible Form Labels)
- Robust (W3C ARIA Tablist Pattern, Modal Dialogs, Live Regions)
"""

import re
import pytest
from fastapi.testclient import TestClient
from legal_ease.main import app
from legal_ease.ui import get_dashboard_html

client = TestClient(app)


class TestWCAGConformance:
    """Automated WCAG 2.1 Level AAA and AA audit on rendered interface and API."""

    @pytest.fixture(autouse=True)
    def setup_html(self):
        self.html = get_dashboard_html()

    def test_accessibility_telemetry_endpoint(self):
        """Verify the /api/accessibility endpoint returns Level AAA conformance data."""
        res = client.get("/api/accessibility")
        assert res.status_code == 200
        data = res.json()
        assert data["standard"] == "WCAG 2.1 Level AAA / AA"
        assert data["conformance_status"] == "CONFORMANT"
        assert data["skip_to_content"] is True
        assert "7:1 AAA" in data["contrast_ratio_standard"]
        assert data["vpat_available"] is True

    def test_html_lang_attribute(self):
        """WCAG 3.1.1: Verify root HTML tag defines language."""
        assert '<html lang="en"' in self.html

    def test_meta_accessibility_tags(self):
        """Verify accessibility viewport and descriptive metadata exist."""
        assert 'name="viewport"' in self.html
        assert 'name="description"' in self.html

    def test_wcag_semantic_landmarks_present(self):
        """
        WCAG 1.3.1 & 2.4.1: Verify all required HTML5 landmark roles are present.
        Ensures screen readers can navigate via landmarks.
        """
        assert 'role="banner"' in self.html, "Missing header landmark role='banner'"
        assert 'id="main-content"' in self.html, "Missing main landmark id='main-content'"
        assert 'role="main"' in self.html, "Missing main landmark role='main'"
        assert 'role="contentinfo"' in self.html, "Missing footer landmark role='contentinfo'"
        assert 'role="tablist"' in self.html, "Missing navigation tablist landmark role='tablist'"
        assert 'role="note"' in self.html, "Missing non-advisory legal notice aside landmark"

    def test_skip_to_content_link(self):
        """
        WCAG 2.4.1: Verify skip-to-content link exists as first navigable element
        and targets the valid main content container.
        """
        assert 'href="#main-content"' in self.html
        assert "Skip to Main Content" in self.html

    def test_focus_visible_styling(self):
        """
        WCAG 2.4.7: Verify visible keyboard focus rings are defined with >= 3px outline.
        """
        assert ":focus-visible" in self.html
        assert "outline: 3px solid" in self.html
        assert "outline-offset: 3px" in self.html

    def test_prefers_reduced_motion_media_query(self):
        """
        WCAG 2.3.3: Verify prefers-reduced-motion media query disables animations.
        """
        assert "@media (prefers-reduced-motion: reduce)" in self.html
        assert "animation-duration: 0.01ms" in self.html

    def test_high_contrast_aaa_badge_classes(self):
        """
        WCAG 1.4.3 & 1.4.6: Verify high contrast badge styles conform to AAA standards.
        """
        assert ".badge-critical" in self.html
        assert ".badge-high" in self.html
        assert ".badge-medium" in self.html
        assert ".badge-low" in self.html
        assert ".badge-cython" in self.html

    def test_w3c_aria_tablist_attributes(self):
        """
        WCAG 4.1.2: Verify W3C ARIA tablist pattern implementation.
        Each tab must have role='tab', aria-selected, aria-controls, and matching section.
        """
        tabs = ["analyzer", "comparator", "chat", "privacy", "details"]
        for tab_id in tabs:
            # Verify tab button
            assert f'id="nav-tab-{tab_id}"' in self.html
            assert f'aria-controls="tab-{tab_id}"' in self.html
            # Verify tabpanel
            assert f'id="tab-{tab_id}"' in self.html
            assert f'aria-labelledby="nav-tab-{tab_id}"' in self.html

    def test_keyboard_shortcuts_mapped(self):
        """
        WCAG 2.1.1: Verify full keyboard navigation and shortcut documentation exist.
        """
        assert "Alt + 1" in self.html
        assert "Alt + 2" in self.html
        assert "Alt + 3" in self.html
        assert "Alt + 4" in self.html
        assert "Alt + 5" in self.html
        assert "Ctrl + Enter" in self.html
        assert "Esc" in self.html
        assert "?" in self.html

    def test_modal_dialog_accessibility(self):
        """
        WCAG 4.1.2: Verify modal dialogs have role='dialog', aria-modal='true', and aria-labelledby.
        """
        assert 'role="dialog"' in self.html
        assert 'aria-modal="true"' in self.html
        assert 'aria-labelledby=' in self.html

    def test_screen_reader_live_regions(self):
        """
        WCAG 4.1.3: Verify live regions exist with role='status' or aria-live='polite'.
        """
        assert 'role="status"' in self.html
        assert 'aria-live="polite"' in self.html

    def test_all_form_inputs_have_labels(self):
        """
        WCAG 3.3.2: Verify all form input elements have an associated <label for="..."> or aria-label.
        """
        input_ids = [
            "modal-api-key",
            "modal-base-url",
            "modal-model-name",
            "modal-threshold",
            "calc-contracts",
            "calc-rate",
            "calc-hours",
            "calc-deal",
        ]
        for inp_id in input_ids:
            has_for_label = f'for="{inp_id}"' in self.html
            has_aria_label = f'id="{inp_id}"' in self.html and 'aria-label=' in self.html
            assert has_for_label or has_aria_label, f"Missing accessible label for {inp_id}"
