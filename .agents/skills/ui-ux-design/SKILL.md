---
name: ui-ux-design
description: Design system and UI/UX standards for Legal-Ease, ensuring high-fidelity visual aesthetics, Poppins typography, WCAG 2.1 AAA accessibility, glassmorphic dark-mode styling, and responsive micro-interactions.
---

# Legal-Ease UI/UX Design System Skill

## Core Principles
1. **Typography**: Google Poppins across all weights (300 to 800) for headers, body, buttons, and badges. JetBrains Mono exclusively for code/tokens.
2. **Aesthetic & Theme**: Deep obsidian / cyber-slate dark mode (`#070913`, `#0f172a`), subtle radial aurora backlights (indigo, violet, cyan), ultra-clean glassmorphic panels (`backdrop-blur-xl`, border-white/10).
3. **Accessibility (WCAG 2.1 AAA)**: Minimum 7:1 contrast for regular text, 4.5:1 for large text. Clear focus visible rings (`focus-visible:ring-2 focus-visible:ring-indigo-400`). Semantic HTML (`role="tablist"`, `aria-selected`, `aria-controls`, `role="status"`).
4. **Micro-Interactions**:
   - Smooth hover scaling and elevation shadows.
   - Animated glowing borders on primary cards and buttons.
   - Live visual feedback (toasts for copy actions, animated loading pulses during analysis).
   - Dynamic SVG risk gauges and interactive sliders with real-time value updates.
5. **Information Architecture**:
   - 5 Main Workspaces: Contract Risk Analyzer, Version Comparator, Legal Navigator AI, Privacy Vault, Impact & Estimated Savings.
   - Responsive, mobile-friendly tabs with scroll snapping.
   - Collapsible & filterable clause views for zero cognitive overload.
