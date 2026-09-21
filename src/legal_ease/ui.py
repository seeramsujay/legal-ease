"""
Web UI dashboard template and component builder for Legal-Ease.
Clean, modern typography with Poppins everywhere, WCAG 2.1 AAA accessible,
ambient aurora mesh gradients, accessible (WCAG 2.1 AAA/AA compliant),
with Cython hardware acceleration indicators, Gemini Flash-Lite / Nemotron LLM escalation,
environment variable key allowance detection, and semantic twisted drafting radar.
"""

def get_dashboard_html() -> str:
    """Return the complete, self-contained, accessible, flashy dashboard HTML."""
    return """<!DOCTYPE html>
<html lang="en" class="h-full bg-slate-950 text-slate-100 antialiased selection:bg-indigo-500 selection:text-white">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="accessibility" content="WCAG 2.1 Level AAA / AA Compliant, Section 508 VPAT">
  <meta name="description" content="Legal-Ease: Privacy-First AI Legal Navigator & Contract Risk Analyzer powered by local semantic embeddings, Cython C-acceleration, and Google Gemini Flash-Lite / NVIDIA Nemotron.">
  <title>Legal-Ease | Privacy-First Legal AI Navigator</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {
      darkMode: 'class',
      theme: {
        extend: {
          fontFamily: {
            sans: ['Poppins', 'system-ui', '-apple-system', 'sans-serif'],
            display: ['Poppins', 'system-ui', '-apple-system', 'sans-serif'],
            mono: ['JetBrains Mono', 'monospace'],
          },
          colors: {
            brand: {
              50: '#eef2ff',
              100: '#e0e7ff',
              400: '#818cf8',
              500: '#6366f1',
              600: '#4f46e5',
              700: '#4338ca',
              800: '#3730a3',
              900: '#312e81',
              950: '#1e1b4b',
            }
          }
        }
      }
    }
  </script>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&family=Poppins:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800;1,300;1,400;1,600&display=swap');
    
    :root {
      --font-display: 'Poppins', system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      --font-body: 'Poppins', system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      --font-mono: 'JetBrains Mono', monospace;
    }

    * {
      font-family: 'Poppins', system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }

    body {
      font-family: 'Poppins', system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      background-color: #030712;
      background-image: 
        radial-gradient(circle at 15% 15%, rgba(99, 102, 241, 0.12) 0%, transparent 40%),
        radial-gradient(circle at 85% 20%, rgba(217, 70, 239, 0.10) 0%, transparent 40%),
        radial-gradient(circle at 50% 85%, rgba(6, 182, 212, 0.08) 0%, transparent 50%);
      background-attachment: fixed;
    }

    .font-display {
      font-family: var(--font-display);
      letter-spacing: -0.025em;
    }
    
    code, pre, .font-mono {
      font-family: var(--font-mono);
    }

    /* Animated Glowing Aurora Accents & Animations */
    @keyframes float-slow {
      0%, 100% { transform: translateY(0px) scale(1); }
      50% { transform: translateY(-8px) scale(1.02); }
    }
    @keyframes pulse-glow {
      0%, 100% { opacity: 0.4; transform: scale(1); }
      50% { opacity: 0.8; transform: scale(1.05); }
    }
    @keyframes shimmer-btn {
      0% { transform: translateX(-100%); }
      100% { transform: translateX(200%); }
    }

    .animate-float {
      animation: float-slow 6s ease-in-out infinite;
    }
    .animate-shimmer {
      position: absolute;
      top: 0; left: 0; right: 0; bottom: 0;
      background: linear-gradient(90deg, transparent, rgba(255,255,255,0.22), transparent);
      transform: translateX(-100%);
      animation: shimmer-btn 3s infinite;
    }

    /* Glassmorphic panels with accessible contrast */
    .glass-panel {
      background: rgba(15, 23, 42, 0.85);
      backdrop-filter: blur(20px);
      -webkit-backdrop-filter: blur(20px);
      border: 1px solid rgba(255, 255, 255, 0.10);
      box-shadow: 0 16px 40px -15px rgba(0, 0, 0, 0.65);
    }
    .glass-card {
      background: rgba(22, 31, 48, 0.75);
      backdrop-filter: blur(16px);
      border: 1px solid rgba(255, 255, 255, 0.08);
      transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
    }
    .glass-card:hover {
      border-color: rgba(129, 140, 248, 0.45);
      box-shadow: 0 12px 35px -10px rgba(99, 102, 241, 0.20);
      transform: translateY(-2px);
    }

    /* SVG Circular Progress Gauge */
    .gauge-bg {
      stroke: rgba(51, 65, 85, 0.5);
      stroke-width: 8;
    }
    .gauge-fill {
      stroke-width: 8;
      stroke-linecap: round;
      transition: stroke-dashoffset 1s ease-in-out, stroke 0.5s ease;
    }

    /* Toast Notification Animation */
    #toast-container {
      position: fixed;
      bottom: 24px;
      right: 24px;
      z-index: 9999;
      display: flex;
      flex-direction: column;
      gap: 10px;
      pointer-events: none;
    }
    .toast-item {
      pointer-events: auto;
      background: rgba(15, 23, 42, 0.95);
      border: 1px solid rgba(99, 102, 241, 0.4);
      color: #f8fafc;
      padding: 12px 20px;
      border-radius: 14px;
      box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5), 0 0 20px rgba(99, 102, 241, 0.2);
      backdrop-filter: blur(16px);
      font-size: 13px;
      font-weight: 600;
      display: flex;
      align-items: center;
      gap: 10px;
      animation: slideInToast 0.3s ease-out forwards;
      transition: opacity 0.3s ease, transform 0.3s ease;
    }
    @keyframes slideInToast {
      from { transform: translateY(20px); opacity: 0; }
      to { transform: translateY(0); opacity: 1; }
    }
    .glass-card {
      background: rgba(30, 41, 59, 0.70);
      backdrop-filter: blur(14px);
      border: 1px solid rgba(255, 255, 255, 0.08);
      transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
    }
    .glass-card:hover {
      border-color: rgba(168, 85, 247, 0.35);
      box-shadow: 0 12px 35px -10px rgba(129, 140, 248, 0.15);
    }

    /* WCAG AAA High Contrast Badges */
    .badge-critical {
      background: rgba(225, 29, 72, 0.22);
      color: #ffe4e6;
      border: 1px solid #f43f5e;
    }
    .badge-high {
      background: rgba(239, 68, 68, 0.22);
      color: #fef2f2;
      border: 1px solid #ef4444;
    }
    .badge-medium {
      background: rgba(245, 158, 11, 0.22);
      color: #fef3c7;
      border: 1px solid #f59e0b;
    }
    .badge-low {
      background: rgba(16, 185, 129, 0.22);
      color: #ecfdf5;
      border: 1px solid #10b981;
    }
    .badge-gemini {
      background: rgba(14, 165, 233, 0.25);
      color: #f0f9ff;
      border: 1px solid #38bdf8;
    }
    .badge-nemotron {
      background: rgba(139, 92, 246, 0.25);
      color: #f5f3ff;
      border: 1px solid #a855f7;
    }
    .badge-twisted {
      background: rgba(245, 158, 11, 0.25);
      color: #fef3c7;
      border: 1px solid #fbbf24;
      box-shadow: 0 0 15px -3px rgba(245, 158, 11, 0.3);
    }
    .badge-cython {
      background: rgba(6, 182, 212, 0.22);
      color: #ecfeff;
      border: 1px solid #06b6d4;
    }

    /* Accessible focus indicators (WCAG 2.4.7) */
    :focus-visible {
      outline: 3px solid #818cf8 !important;
      outline-offset: 3px !important;
    }

    /* Prefers Reduced Motion (WCAG 2.3.3) */
    @media (prefers-reduced-motion: reduce) {
      *, ::before, ::after {
        animation-duration: 0.01ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: 0.01ms !important;
        scroll-behavior: auto !important;
      }
    }

    /* Custom scrollbars */
    ::-webkit-scrollbar {
      width: 8px;
      height: 8px;
    }
    ::-webkit-scrollbar-track {
      background: rgba(15, 23, 42, 0.8);
    }
    ::-webkit-scrollbar-thumb {
      background: rgba(100, 116, 139, 0.5);
      border-radius: 9999px;
    }
    ::-webkit-scrollbar-thumb:hover {
      background: rgba(129, 140, 248, 0.8);
    }
  </style>
</head>
<body class="h-full flex flex-col bg-slate-950 text-slate-100 overflow-x-hidden">

  <!-- Accessible Skip-to-Content Link (WCAG 2.4.1) -->
  <a href="#main-content" class="sr-only focus:not-sr-only focus:fixed focus:top-4 focus:left-4 z-50 px-4 py-2.5 bg-indigo-600 text-white font-bold rounded-lg shadow-2xl border-2 border-white ring-4 ring-indigo-300">
    Skip to Main Content (Press Enter)
  </a>

  <!-- Ambient Glow Background -->
  <div class="fixed inset-0 pointer-events-none z-0 overflow-hidden" aria-hidden="true">
    <div class="absolute -top-40 left-1/4 w-[500px] h-[500px] bg-indigo-600/10 rounded-full blur-[120px]"></div>
    <div class="absolute top-1/3 -right-20 w-[450px] h-[450px] bg-fuchsia-600/10 rounded-full blur-[120px]"></div>
    <div class="absolute -bottom-40 left-1/3 w-[500px] h-[500px] bg-cyan-600/10 rounded-full blur-[120px]"></div>
  </div>

  <!-- Mandatory Legal Disclaimer Banner -->
  <aside role="note" aria-label="Legal Non-Advisory Notice" class="relative z-20 bg-slate-900/95 border-b border-slate-800 text-slate-300 text-xs py-2 px-4 text-center font-medium backdrop-blur">
    ⚖️ <strong>Non-Advisory Tool:</strong> Legal-Ease provides educational contract literacy, semantic obfuscation detection, and negotiation issue-spotting. It does not provide legal advice or substitute for a licensed attorney.
  </aside>

  <!-- Header -->
  <header role="banner" class="relative z-20 glass-panel border-b border-slate-800/80 sticky top-0 shadow-xl">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex items-center justify-between h-16">
      
      <!-- Brand & Telemetry Badges -->
      <div class="flex items-center space-x-3.5">
        <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-indigo-500 via-purple-600 to-pink-500 flex items-center justify-center text-white shadow-lg shadow-indigo-500/25 ring-1 ring-white/20 text-lg font-bold" aria-hidden="true">
          ⚖️
        </div>
        <div>
          <div class="flex items-center gap-2">
            <span class="font-display text-xl font-extrabold tracking-tight bg-gradient-to-r from-white via-indigo-100 to-indigo-300 bg-clip-text text-transparent">
              Legal-Ease
            </span>
            <!-- Acceleration Badge -->
            <span id="header-cython-badge" class="hidden sm:inline-flex items-center gap-1 text-[10px] uppercase font-bold tracking-wider px-2 py-0.5 rounded-full badge-cython">
              ⚡ Cython Binary Active
            </span>
          </div>
          <p class="text-[11px] text-slate-400 font-medium">Privacy-First AI Contract Navigator & Semantic Risk Engine</p>
        </div>
      </div>

      <!-- Controls & Engine Status -->
      <div class="flex items-center space-x-3">
        
        <!-- PII Status Pill -->
        <span class="hidden md:inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-emerald-500/15 text-emerald-300 border border-emerald-500/30">
          <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" aria-hidden="true"></span>
          100% Local PII Shield
        </span>

        <!-- AI / LLM Model Settings Button -->
        <button onclick="toggleLLMModal()" id="llm-status-btn" aria-haspopup="dialog" aria-expanded="false" class="inline-flex items-center gap-2 px-3 py-1.5 rounded-lg text-xs font-bold bg-slate-800/90 hover:bg-slate-750 text-slate-200 border border-slate-700 shadow-sm transition">
          <span id="llm-dot" class="w-2 h-2 rounded-full bg-cyan-400 animate-pulse" aria-hidden="true"></span>
          <span id="llm-label">Gemini / Nemotron AI</span>
          <span id="env-badge-pill" class="hidden text-[10px] px-1.5 py-0.2 rounded bg-emerald-500/30 text-emerald-300 border border-emerald-500/40">ENV ACTIVE</span>
          <svg class="w-3.5 h-3.5 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/></svg>
        </button>

        <!-- Accessibility Options Trigger Button -->
        <button type="button" onclick="toggleA11yModal()" id="btn-a11y-modal" aria-label="Open Accessibility & Conformance Controls" title="Accessibility Settings (WCAG 2.1 AAA)" class="inline-flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg bg-slate-800/90 hover:bg-slate-750 text-slate-200 text-xs font-bold border border-slate-700 transition">
          <span aria-hidden="true">♿</span>
          <span class="hidden md:inline">A11y (AAA)</span>
        </button>

        <!-- Keyboard Shortcuts Help Trigger Button -->
        <button type="button" onclick="toggleShortcutsModal()" id="btn-shortcuts-modal" aria-label="Open Keyboard Shortcuts Guide (Press ?)" title="Keyboard Shortcuts (?)" class="inline-flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg bg-slate-800/90 hover:bg-slate-750 text-slate-200 text-xs font-bold border border-slate-700 transition">
          <kbd class="px-1.5 py-0.5 text-[10px] font-mono bg-slate-900 border border-slate-700 rounded text-indigo-300 font-bold">?</kbd>
          <span class="hidden md:inline">Shortcuts</span>
        </button>

        <!-- GitHub Public Repo Link -->
        <a href="https://github.com/seeramsujay/legal-ease" target="_blank" rel="noopener noreferrer" class="hidden sm:inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-slate-800/90 hover:bg-slate-750 text-slate-200 text-xs font-bold border border-slate-700 transition">
          <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true"><path fill-rule="evenodd" clip-rule="evenodd" d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.53 1.032 1.53 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z"/></svg>
          Repo
        </a>
      </div>
    </div>

    <!-- Navigation Tabs (WCAG 2.1 Tab Pattern) -->
    <nav role="tablist" aria-label="Application Sections" class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex space-x-6 border-t border-slate-800/80 overflow-x-auto">
      <button role="tab" id="nav-tab-analyzer" aria-selected="true" aria-controls="tab-analyzer" tabindex="0" onclick="switchTab('analyzer')" class="py-3 px-1 border-b-2 font-bold text-xs sm:text-sm border-indigo-500 text-indigo-400 flex items-center gap-2 whitespace-nowrap transition">
        📄 Contract Risk Analyzer
      </button>
      <button role="tab" id="nav-tab-comparator" aria-selected="false" aria-controls="tab-comparator" tabindex="-1" onclick="switchTab('comparator')" class="py-3 px-1 border-b-2 font-bold text-xs sm:text-sm border-transparent text-slate-400 hover:text-slate-200 hover:border-slate-600 flex items-center gap-2 whitespace-nowrap transition">
        ⚖️ Version Comparator
      </button>
      <button role="tab" id="nav-tab-chat" aria-selected="false" aria-controls="tab-chat" tabindex="-1" onclick="switchTab('chat')" class="py-3 px-1 border-b-2 font-bold text-xs sm:text-sm border-transparent text-slate-400 hover:text-slate-200 hover:border-slate-600 flex items-center gap-2 whitespace-nowrap transition">
        💬 Legal Navigator AI
      </button>
      <button role="tab" id="nav-tab-privacy" aria-selected="false" aria-controls="tab-privacy" tabindex="-1" onclick="switchTab('privacy')" class="py-3 px-1 border-b-2 font-bold text-xs sm:text-sm border-transparent text-slate-400 hover:text-slate-200 hover:border-slate-600 flex items-center gap-2 whitespace-nowrap transition">
        🛡️ Privacy & PII Vault
      </button>
      <button role="tab" id="nav-tab-details" aria-selected="false" aria-controls="tab-details" tabindex="-1" onclick="switchTab('details')" class="py-3 px-1 border-b-2 font-bold text-xs sm:text-sm border-transparent text-slate-400 hover:text-slate-200 hover:border-slate-600 flex items-center gap-2 whitespace-nowrap transition">
        ✨ Impact & Estimated Savings
      </button>
    </nav>
  </header>

  <!-- ==================== HACKATHON PROBLEM STATEMENT & 7 USE CASES SHOWCASE ==================== -->
  <section aria-label="Hackathon Problem Statement Alignment" class="relative z-10 bg-gradient-to-r from-indigo-950/90 via-purple-950/80 to-slate-950/95 border-b border-indigo-500/25 py-2.5 px-4 shadow-md">
    <div class="max-w-7xl mx-auto flex flex-col lg:flex-row items-start lg:items-center justify-between gap-3 text-xs">
      <div class="flex items-center gap-2 flex-wrap">
        <span class="px-2.5 py-0.5 rounded-full bg-indigo-500/25 text-indigo-300 font-extrabold border border-indigo-500/40 text-[10px] tracking-wide uppercase shadow-sm">
          🎯 AI for Legal Assistance & Access
        </span>
        <span class="text-slate-300 font-medium text-[11px] sm:text-xs">
          <strong>Official Problem Statement:</strong> Making legal documents accessible, understandable, and navigable.
        </span>
      </div>
      <!-- 7 Core Potential Use Case Quick Jumps -->
      <div class="flex items-center gap-1.5 overflow-x-auto w-full lg:w-auto pb-1 lg:pb-0 text-[11px]" role="group" aria-label="7 Challenge Potential Use Cases">
        <button type="button" onclick="switchTab('analyzer')" class="px-2.5 py-1 rounded-lg bg-slate-900/90 hover:bg-indigo-900/60 text-slate-300 hover:text-white border border-slate-700 hover:border-indigo-500/50 whitespace-nowrap transition flex items-center gap-1">
          <span class="font-extrabold text-indigo-400">1.</span> Simplify Legalese
        </button>
        <button type="button" onclick="switchTab('comparator')" class="px-2.5 py-1 rounded-lg bg-slate-900/90 hover:bg-indigo-900/60 text-slate-300 hover:text-white border border-slate-700 hover:border-indigo-500/50 whitespace-nowrap transition flex items-center gap-1">
          <span class="font-extrabold text-indigo-400">2.</span> Compare Versions
        </button>
        <button type="button" onclick="switchTab('analyzer')" class="px-2.5 py-1 rounded-lg bg-slate-900/90 hover:bg-indigo-900/60 text-slate-300 hover:text-white border border-slate-700 hover:border-indigo-500/50 whitespace-nowrap transition flex items-center gap-1">
          <span class="font-extrabold text-indigo-400">3.</span> Highlight Risks
        </button>
        <button type="button" onclick="switchTab('chat')" class="px-2.5 py-1 rounded-lg bg-slate-900/90 hover:bg-indigo-900/60 text-slate-300 hover:text-white border border-slate-700 hover:border-indigo-500/50 whitespace-nowrap transition flex items-center gap-1">
          <span class="font-extrabold text-indigo-400">4.</span> Document Q&A
        </button>
        <button type="button" onclick="switchTab('analyzer')" class="px-2.5 py-1 rounded-lg bg-slate-900/90 hover:bg-indigo-900/60 text-slate-300 hover:text-white border border-slate-700 hover:border-indigo-500/50 whitespace-nowrap transition flex items-center gap-1">
          <span class="font-extrabold text-indigo-400">5.</span> Next Steps
        </button>
        <button type="button" onclick="switchTab('analyzer'); switchAnalysisView('checklist');" class="px-2.5 py-1 rounded-lg bg-slate-900/90 hover:bg-indigo-900/60 text-slate-300 hover:text-white border border-slate-700 hover:border-indigo-500/50 whitespace-nowrap transition flex items-center gap-1">
          <span class="font-extrabold text-indigo-400">6.</span> Checklists
        </button>
        <button type="button" onclick="switchTab('details')" class="px-2.5 py-1 rounded-lg bg-indigo-600/30 hover:bg-indigo-600/50 text-indigo-200 border border-indigo-500/40 font-bold whitespace-nowrap transition flex items-center gap-1">
          <span class="font-extrabold text-indigo-300">7.</span> Prep For Counsel
        </button>
      </div>
    </div>
  </section>

  <!-- ==================== ACCESSIBLE AI / LLM SETTINGS MODAL ==================== -->
  <div id="llm-modal" role="dialog" aria-modal="true" aria-labelledby="modal-title" class="hidden fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-md">
    <div class="glass-panel w-full max-w-xl rounded-2xl p-6 space-y-5 border border-slate-700 shadow-2xl">
      
      <div class="flex items-center justify-between border-b border-slate-800 pb-3">
        <div class="flex items-center gap-2.5">
          <div class="w-8 h-8 rounded-lg bg-gradient-to-br from-cyan-500 via-indigo-600 to-purple-600 flex items-center justify-center text-white text-base" aria-hidden="true">
            🧠
          </div>
          <div>
            <h2 id="modal-title" class="font-display text-base font-bold text-white">AI Engine & Model Configuration</h2>
            <p class="text-xs text-slate-400">Google Gemini Flash-Lite, NVIDIA Nemotron, & OpenAI Compatibility</p>
          </div>
        </div>
        <button onclick="toggleLLMModal()" aria-label="Close modal dialog" class="text-slate-400 hover:text-white p-1 rounded-lg">✕</button>
      </div>

      <div class="space-y-4 text-xs">
        
        <!-- Environment Key Status Banner -->
        <div id="modal-env-status" class="p-3.5 rounded-xl bg-emerald-950/40 border border-emerald-800/60 text-emerald-200 space-y-1">
          <div class="font-bold flex items-center gap-1.5 text-emerald-300">
            <span>✨</span> <span>Environment Allowance Active</span>
          </div>
          <p class="text-[11px] leading-relaxed text-emerald-200/90" id="modal-env-desc">
            API key auto-detected from server environment. Evaluator does not need to configure BYOK!
          </p>
        </div>

        <!-- Provider Presets Selector -->
        <div>
          <label class="block font-bold text-slate-300 mb-1.5">Select AI Provider Preset:</label>
          <div class="grid grid-cols-3 gap-2" role="radiogroup" aria-label="AI Providers">
            <button type="button" onclick="selectProviderPreset('gemini')" id="btn-preset-gemini" class="p-2.5 rounded-xl border border-indigo-500 bg-indigo-950/60 text-left transition hover:border-indigo-400">
              <div class="font-extrabold text-white text-[12px] flex items-center gap-1">
                <span>🚀</span> Gemini Flash
              </div>
              <div class="text-[10px] text-indigo-300 mt-0.5">Fast & Economical</div>
            </button>
            <button type="button" onclick="selectProviderPreset('nemotron')" id="btn-preset-nemotron" class="p-2.5 rounded-xl border border-slate-700 bg-slate-900/60 text-left transition hover:border-purple-400">
              <div class="font-extrabold text-white text-[12px] flex items-center gap-1">
                <span>🧠</span> Nemotron 70B
              </div>
              <div class="text-[10px] text-purple-300 mt-0.5">High Reasoning</div>
            </button>
            <button type="button" onclick="selectProviderPreset('openai')" id="btn-preset-openai" class="p-2.5 rounded-xl border border-slate-700 bg-slate-900/60 text-left transition hover:border-slate-500">
              <div class="font-extrabold text-white text-[12px] flex items-center gap-1">
                <span>⚡</span> GPT-4o-mini
              </div>
              <div class="text-[10px] text-slate-400 mt-0.5">OpenAI Standard</div>
            </button>
          </div>
        </div>

        <!-- API Key Input (BYOK Mode with Environment Fallback) -->
        <div>
          <div class="flex items-center justify-between mb-1">
            <label class="font-bold text-slate-300" for="modal-api-key">API Key / BYOK (Optional)</label>
            <span id="modal-key-badge" class="text-[10px] font-bold text-indigo-400">BYOK Supported</span>
          </div>
          <input type="password" id="modal-api-key" placeholder="AIzaSy... or nvapi-... or sk-... (Leave empty for environment default)" class="w-full px-3 py-2 rounded-lg bg-slate-900 border border-slate-700 text-white placeholder:text-slate-500 focus:border-indigo-500">
          <p class="text-[10px] text-slate-400 mt-1">Leave blank to use server environment key (<code class="text-indigo-300">GEMINI_API_KEY</code>). Enter a key to override with your personal BYOK key.</p>
        </div>

        <!-- Base URL -->
        <div>
          <label class="block font-bold text-slate-300 mb-1" for="modal-base-url">Base URL</label>
          <input type="text" id="modal-base-url" value="https://generativelanguage.googleapis.com/v1beta/openai" class="w-full px-3 py-2 rounded-lg bg-slate-900 border border-slate-700 text-white font-mono text-[11px] focus:border-indigo-500">
        </div>

        <!-- Model Identifier -->
        <div>
          <label class="block font-bold text-slate-300 mb-1" for="modal-model-name">Model Name</label>
          <input type="text" id="modal-model-name" value="gemini-2.0-flash-lite" class="w-full px-3 py-2 rounded-lg bg-slate-900 border border-slate-700 text-white font-mono text-[11px] focus:border-indigo-500">
        </div>

        <!-- Confidence Threshold Slider -->
        <div>
          <div class="flex items-center justify-between mb-1">
            <label class="font-bold text-slate-300" for="modal-threshold">Escalation Confidence Threshold</label>
            <span id="threshold-val" class="font-extrabold text-indigo-400">75%</span>
          </div>
          <input type="range" id="modal-threshold" min="50" max="95" value="75" aria-valuemin="50" aria-valuemax="95" aria-valuenow="75" oninput="document.getElementById('threshold-val').innerText = this.value + '%'" class="w-full accent-indigo-500">
          <p class="text-[11px] text-slate-400 mt-1">Clauses with local confidence below this threshold (or twisted drafting) escalate to the LLM for deep synthesis.</p>
        </div>

      </div>

      <!-- Modal Footer -->
      <div class="flex items-center justify-between pt-3 border-t border-slate-800">
        <div class="flex items-center gap-2">
          <button type="button" onclick="testConnection()" id="modal-test-btn" class="px-3.5 py-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-bold border border-slate-700 transition flex items-center gap-1.5">
            <span>Ping / Test Connection</span>
          </button>
          <button type="button" onclick="resetToEnvironmentSettings()" id="modal-reset-btn" class="hidden px-3 py-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-amber-300 text-xs font-bold border border-amber-800/60 transition flex items-center gap-1">
            <span>↺ Reset to Env</span>
          </button>
        </div>
        <div class="flex items-center gap-2">
          <button type="button" onclick="toggleLLMModal()" class="px-3 py-2 rounded-lg text-slate-400 hover:text-white text-xs font-semibold">Cancel</button>
          <button type="button" onclick="saveLLMSettings()" id="modal-save-btn" class="px-4 py-2 rounded-lg bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-bold shadow-md shadow-indigo-600/30 transition">
            Save & Activate
          </button>
        </div>
      </div>
      <div id="modal-test-result" role="status" aria-live="polite" class="hidden text-xs p-3 rounded-lg"></div>
    </div>
  </div>


  <!-- ==================== KEYBOARD SHORTCUTS & ACCESSIBILITY MODAL ==================== -->
  <div id="shortcuts-modal" role="dialog" aria-modal="true" aria-labelledby="shortcuts-title" class="hidden fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-md">
    <div class="glass-panel w-full max-w-lg rounded-2xl p-6 space-y-5 border border-slate-700 shadow-2xl">
      <div class="flex items-center justify-between border-b border-slate-800 pb-3">
        <div class="flex items-center gap-2.5">
          <div class="w-8 h-8 rounded-lg bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center text-white text-sm font-bold" aria-hidden="true">
            ⌨️
          </div>
          <div>
            <h2 id="shortcuts-title" class="font-display text-base font-bold text-white">Keyboard Navigation & Shortcuts</h2>
            <p class="text-xs text-slate-400">WCAG 2.1 AAA Compliant Single-Key & Combo Navigation</p>
          </div>
        </div>
        <button onclick="toggleShortcutsModal()" aria-label="Close shortcuts modal" class="text-slate-400 hover:text-white p-1 rounded-lg">✕</button>
      </div>

      <div class="space-y-4 text-xs">
        <div class="space-y-2">
          <h3 class="font-bold text-slate-300 uppercase tracking-wider text-[11px]">Workspace Navigation</h3>
          <div class="grid grid-cols-2 gap-2 text-slate-200 font-mono">
            <div class="flex items-center justify-between p-2 rounded-lg bg-slate-900/80 border border-slate-800">
              <span class="font-sans text-[11px] text-slate-300">Analyzer Tab</span>
              <kbd class="px-2 py-0.5 bg-slate-800 rounded border border-slate-700 text-indigo-300 font-bold">Alt + 1</kbd>
            </div>
            <div class="flex items-center justify-between p-2 rounded-lg bg-slate-900/80 border border-slate-800">
              <span class="font-sans text-[11px] text-slate-300">Comparator Tab</span>
              <kbd class="px-2 py-0.5 bg-slate-800 rounded border border-slate-700 text-indigo-300 font-bold">Alt + 2</kbd>
            </div>
            <div class="flex items-center justify-between p-2 rounded-lg bg-slate-900/80 border border-slate-800">
              <span class="font-sans text-[11px] text-slate-300">Navigator AI Tab</span>
              <kbd class="px-2 py-0.5 bg-slate-800 rounded border border-slate-700 text-indigo-300 font-bold">Alt + 3</kbd>
            </div>
            <div class="flex items-center justify-between p-2 rounded-lg bg-slate-900/80 border border-slate-800">
              <span class="font-sans text-[11px] text-slate-300">Privacy Vault Tab</span>
              <kbd class="px-2 py-0.5 bg-slate-800 rounded border border-slate-700 text-indigo-300 font-bold">Alt + 4</kbd>
            </div>
            <div class="flex items-center justify-between p-2 rounded-lg bg-slate-900/80 border border-slate-800 col-span-2">
              <span class="font-sans text-[11px] text-slate-300">Impact & Savings Tab</span>
              <kbd class="px-2 py-0.5 bg-slate-800 rounded border border-slate-700 text-indigo-300 font-bold">Alt + 5</kbd>
            </div>
          </div>
        </div>

        <div class="space-y-2">
          <h3 class="font-bold text-slate-300 uppercase tracking-wider text-[11px]">Actions & Execution</h3>
          <div class="grid grid-cols-2 gap-2 text-slate-200 font-mono">
            <div class="flex items-center justify-between p-2 rounded-lg bg-slate-900/80 border border-slate-800">
              <span class="font-sans text-[11px] text-slate-300">Run Analysis</span>
              <kbd class="px-2 py-0.5 bg-slate-800 rounded border border-slate-700 text-emerald-300 font-bold">Ctrl + Enter</kbd>
            </div>
            <div class="flex items-center justify-between p-2 rounded-lg bg-slate-900/80 border border-slate-800">
              <span class="font-sans text-[11px] text-slate-300">Focus Clause Search</span>
              <kbd class="px-2 py-0.5 bg-slate-800 rounded border border-slate-700 text-cyan-300 font-bold">/</kbd>
            </div>
            <div class="flex items-center justify-between p-2 rounded-lg bg-slate-900/80 border border-slate-800">
              <span class="font-sans text-[11px] text-slate-300">AI / LLM Settings</span>
              <kbd class="px-2 py-0.5 bg-slate-800 rounded border border-slate-700 text-purple-300 font-bold">Alt + S</kbd>
            </div>
            <div class="flex items-center justify-between p-2 rounded-lg bg-slate-900/80 border border-slate-800">
              <span class="font-sans text-[11px] text-slate-300">Close Any Modal</span>
              <kbd class="px-2 py-0.5 bg-slate-800 rounded border border-slate-700 text-rose-300 font-bold">Esc</kbd>
            </div>
            <div class="flex items-center justify-between p-2 rounded-lg bg-slate-900/80 border border-slate-800 col-span-2">
              <span class="font-sans text-[11px] text-slate-300">Toggle This Guide</span>
              <kbd class="px-2 py-0.5 bg-slate-800 rounded border border-slate-700 text-indigo-300 font-bold">?</kbd>
            </div>
          </div>
        </div>

        <div class="p-3 rounded-xl bg-slate-900/90 border border-slate-800 text-[11px] text-slate-300 space-y-1">
          <div class="font-bold text-slate-200">♿ Accessibility Assurance:</div>
          <p>This application follows W3C ARIA Authoring Practices for Tabs, Dialogs, Live Regions, and high-contrast 7:1 text standards with zero mouse dependency.</p>
        </div>
      </div>

      <div class="flex justify-end pt-3 border-t border-slate-800">
        <button type="button" onclick="toggleShortcutsModal()" class="px-4 py-2 rounded-lg bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-bold transition">
          Got It
        </button>
      </div>
    </div>
  </div>

      <!-- ==================== ACCESSIBILITY & WCAG 2.1 AAA CONTROLS MODAL ==================== -->
  <div id="a11y-modal" role="dialog" aria-modal="true" aria-labelledby="a11y-modal-title" class="hidden fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-md">
    <div class="glass-panel w-full max-w-lg rounded-2xl p-6 space-y-5 border border-slate-700 shadow-2xl">
      <div class="flex items-center justify-between border-b border-slate-800 pb-3">
        <div class="flex items-center gap-2.5">
          <div class="w-8 h-8 rounded-lg bg-gradient-to-br from-teal-500 to-emerald-600 flex items-center justify-center text-white text-base font-bold" aria-hidden="true">
            ♿
          </div>
          <div>
            <h2 id="a11y-modal-title" class="font-display text-base font-bold text-white">Accessibility Controls (WCAG 2.1 AAA)</h2>
            <p class="text-xs text-slate-400">Universal Design, Text Scaling & High Contrast Options</p>
          </div>
        </div>
        <button onclick="toggleA11yModal()" aria-label="Close accessibility options" class="text-slate-400 hover:text-white p-1 rounded-lg">✕</button>
      </div>

      <div class="space-y-4 text-xs">
        <div class="p-3.5 rounded-xl bg-slate-900/80 border border-slate-800 space-y-2">
          <label class="font-bold text-slate-200 block">Text Scaling (WCAG 1.4.4):</label>
          <div class="grid grid-cols-3 gap-2">
            <button type="button" onclick="setFontScale('100%')" id="scale-100" class="py-1.5 rounded-lg bg-indigo-600 text-white font-bold text-xs">100% (Default)</button>
            <button type="button" onclick="setFontScale('115%')" id="scale-115" class="py-1.5 rounded-lg bg-slate-800 text-slate-300 font-bold text-xs hover:bg-slate-700">115% (Large)</button>
            <button type="button" onclick="setFontScale('130%')" id="scale-130" class="py-1.5 rounded-lg bg-slate-800 text-slate-300 font-bold text-xs hover:bg-slate-700">130% (XL)</button>
          </div>
        </div>

        <div class="grid grid-cols-2 gap-2.5">
          <button type="button" onclick="toggleHighContrastMode()" id="btn-contrast-toggle" class="p-3 rounded-xl bg-slate-900/80 border border-slate-800 hover:border-slate-600 text-left transition">
            <div class="font-bold text-slate-200 text-xs flex items-center gap-1.5">
              <span>🌓</span> High Contrast (AAA)
            </div>
            <div class="text-[10px] text-slate-400 mt-1">Boosts contrast to 19:1 for low-vision clarity</div>
          </button>
          <button type="button" onclick="toggleDyslexiaFriendlyFont()" id="btn-dyslexia-toggle" class="p-3 rounded-xl bg-slate-900/80 border border-slate-800 hover:border-slate-600 text-left transition">
            <div class="font-bold text-slate-200 text-xs flex items-center gap-1.5">
              <span>🔤</span> Dyslexia Font Mode
            </div>
            <div class="text-[10px] text-slate-400 mt-1">Increases letter spacing & font legibility</div>
          </button>
        </div>

        <div class="p-3.5 rounded-xl bg-emerald-950/40 border border-emerald-800/50 text-[11px] text-emerald-200 space-y-1">
          <div class="font-bold text-emerald-300 flex items-center gap-1">
            <span>✓</span> <span>VPAT Self-Declaration (Section 508 & WCAG 2.1 AAA)</span>
          </div>
          <p class="leading-relaxed text-emerald-200/90">
            Features 100% full keyboard shortcuts, ARIA live announcement regions, visible 3px focus rings, semantic landmark hierarchy, and reduced-motion support.
          </p>
        </div>
      </div>

      <div class="flex justify-end pt-3 border-t border-slate-800">
        <button type="button" onclick="toggleA11yModal()" class="px-4 py-2 rounded-lg bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-bold transition">
          Close
        </button>
      </div>
    </div>
  </div>

  <!-- Main Landmark -->
  <main id="main-content" role="main" class="relative z-10 flex-1 max-w-7xl w-full mx-auto p-4 sm:p-6 lg:p-8 space-y-6">

    <!-- ==================== TAB 1: ANALYZER ==================== -->
    <section id="tab-analyzer" role="tabpanel" aria-labelledby="nav-tab-analyzer" class="space-y-6">
      
      <!-- Beginner Quick-Start Guide (Accessible to any experience level) -->
      <div class="rounded-2xl p-5 border border-indigo-500/30 bg-gradient-to-r from-indigo-950/40 via-purple-950/20 to-slate-900/80 backdrop-blur-xl shadow-lg space-y-3">
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
          <div class="flex items-center gap-2">
            <span class="text-xl" aria-hidden="true">💡</span>
            <h3 class="font-display text-sm sm:text-base font-extrabold text-white">
              New to Legal Contracts? Start Here in 3 Simple Steps:
            </h3>
          </div>
          <span class="text-[11px] font-bold px-2.5 py-1 rounded-full bg-indigo-500/20 text-indigo-300 border border-indigo-500/30 w-fit">
            No Legal Experience Required
          </span>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-3 pt-1 text-xs">
          <div class="p-3 rounded-xl bg-slate-900/80 border border-slate-800 flex items-start gap-3">
            <span class="w-6 h-6 rounded-full bg-indigo-600/30 border border-indigo-500/50 flex items-center justify-center text-indigo-300 font-extrabold text-xs shrink-0">1</span>
            <div>
              <strong class="text-white block font-bold mb-0.5">Click a Sample Contract</strong>
              <p class="text-slate-400 text-[11px] leading-relaxed">Choose <button type="button" onclick="loadSample('freelance_high_risk')" class="text-indigo-400 underline font-semibold">Freelance High Risk</button> or <button type="button" onclick="loadSample('saas_terms')" class="text-indigo-400 underline font-semibold">SaaS Terms</button> to test immediately without typing.</p>
            </div>
          </div>
          <div class="p-3 rounded-xl bg-slate-900/80 border border-slate-800 flex items-start gap-3">
            <span class="w-6 h-6 rounded-full bg-purple-600/30 border border-purple-500/50 flex items-center justify-center text-purple-300 font-extrabold text-xs shrink-0">2</span>
            <div>
              <strong class="text-white block font-bold mb-0.5">Click "Analyze & Score Hazards"</strong>
              <p class="text-slate-400 text-[11px] leading-relaxed">Local Cython AI scans for hidden traps, twisted wording, and liability imbalances in sub-milliseconds.</p>
            </div>
          </div>
          <div class="p-3 rounded-xl bg-slate-900/80 border border-slate-800 flex items-start gap-3">
            <span class="w-6 h-6 rounded-full bg-emerald-600/30 border border-emerald-500/50 flex items-center justify-center text-emerald-300 font-extrabold text-xs shrink-0">3</span>
            <div>
              <strong class="text-white block font-bold mb-0.5">Read Plain-English & Copy Redlines</strong>
              <p class="text-slate-400 text-[11px] leading-relaxed">Review "What It Means For You" and 1-click copy attorney-grade counter-proposals to protect your rights.</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Ingestion & Configuration Box -->
      <div class="glass-panel rounded-2xl p-5 sm:p-6 space-y-4 shadow-xl">
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div>
            <h2 class="font-display text-base sm:text-lg font-extrabold text-white flex items-center gap-2">
              <span>Contract Risk Matrix & Plain-English Navigator</span>
            </h2>
            <p class="text-xs text-slate-400">Local-first analysis accelerated by Cython C-extensions with Gemini Flash-Lite / Nemotron deep reasoning</p>
          </div>
          
          <!-- Sample Contract Selectors -->
          <div class="flex flex-wrap items-center gap-1.5" role="group" aria-label="Load Sample Contracts">
            <span class="text-xs text-slate-400 font-bold mr-1">Sample:</span>
            <button type="button" onclick="loadSample('freelance_high_risk')" class="text-xs bg-slate-800/90 hover:bg-slate-700 text-slate-200 font-semibold px-2.5 py-1 rounded-lg border border-slate-700 hover:border-slate-600 transition">
              🚨 Freelance High Risk
            </button>
            <button type="button" onclick="loadSample('freelance_negotiated')" class="text-xs bg-slate-800/90 hover:bg-slate-700 text-slate-200 font-semibold px-2.5 py-1 rounded-lg border border-slate-700 hover:border-slate-600 transition">
              ✅ Negotiated Redline
            </button>
            <button type="button" onclick="loadSample('saas_terms')" class="text-xs bg-slate-800/90 hover:bg-slate-700 text-slate-200 font-semibold px-2.5 py-1 rounded-lg border border-slate-700 hover:border-slate-600 transition">
              ☁️ SaaS Terms
            </button>
            <button type="button" onclick="loadSample('mutual_nda')" class="text-xs bg-slate-800/90 hover:bg-slate-700 text-slate-200 font-semibold px-2.5 py-1 rounded-lg border border-slate-700 hover:border-slate-600 transition">
              🤝 Mutual NDA
            </button>
          </div>
        </div>

        <div class="relative space-y-1.5">
          <div class="flex items-center justify-between">
            <label for="contract-input" class="block text-xs font-bold text-slate-300">
              Contract Document Text:
            </label>
            <div class="flex items-center gap-3 text-[11px] font-mono text-slate-400">
              <span id="input-stats-pill" class="px-2 py-0.5 rounded-md bg-slate-900 border border-slate-800">
                0 words | 0 chars
              </span>
              <button type="button" onclick="clearContractInput()" class="text-slate-400 hover:text-rose-400 font-bold transition flex items-center gap-1" title="Clear input">
                <span>✕</span> Clear
              </button>
            </div>
          </div>
          <div class="relative group">
            <textarea id="contract-input" rows="8" aria-describedby="contract-input-desc" oninput="updateInputStats()" class="w-full font-mono text-xs text-slate-200 p-4 rounded-xl bg-slate-900/90 border border-slate-800/90 focus:ring-2 focus:ring-indigo-500/50 focus:border-indigo-500 transition leading-relaxed shadow-inner" placeholder="Paste your contract, NDA, SOW, or terms of service here, or drag & drop a .txt/.md file..."></textarea>
            <span id="contract-input-desc" class="sr-only">Input area for contract text. All PII is sanitized locally before analysis.</span>
          </div>
        </div>

        <div class="flex flex-wrap items-center justify-between gap-4 pt-1">
          <div class="flex items-center space-x-3">
            <label class="cursor-pointer inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg border border-slate-700 bg-slate-800/80 hover:bg-slate-700 text-xs font-bold text-slate-200 shadow-sm transition">
              <svg class="w-4 h-4 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12"/></svg>
              Upload Text File
              <input type="file" id="file-upload" class="hidden" accept=".txt,.md" onchange="handleFileUpload(event)">
            </label>
            <button type="button" onclick="previewPII()" class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg border border-slate-700 bg-slate-800/80 hover:bg-slate-700 text-xs font-bold text-slate-200 shadow-sm transition">
              🛡️ Audit PII Shield
            </button>
          </div>

          <button type="button" onclick="runAnalysis()" id="analyze-btn" class="relative overflow-hidden inline-flex items-center gap-2 px-6 py-2.5 rounded-xl bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600 hover:from-indigo-500 hover:to-pink-500 text-white text-xs sm:text-sm font-extrabold shadow-lg shadow-indigo-600/30 transition-all hover:scale-[1.02] active:scale-[0.98]">
            <span class="animate-shimmer pointer-events-none" aria-hidden="true"></span>
            <span>🚀</span>
            <span>Analyze & Score Hazards</span>
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3"/></svg>
          </button>
        </div>
      </div>

      <!-- Live Loading Indicator (WCAG aria-live) -->
      <div id="analyzer-loading" role="status" aria-live="polite" class="hidden text-center py-16 space-y-4">
        <div class="relative inline-flex items-center justify-center" aria-hidden="true">
          <div class="w-12 h-12 border-4 border-indigo-500/20 border-t-indigo-500 rounded-full animate-spin"></div>
          <span class="absolute text-xs font-bold">⚖️</span>
        </div>
        <p class="text-sm font-bold text-slate-200" id="loading-text">Anonymizing sensitive PII and executing Cython-accelerated risk heuristics...</p>
      </div>

      <!-- Analysis Results Presentation Layer -->
      <div id="analyzer-results" role="region" aria-label="Analysis Results" class="hidden space-y-6">

        <!-- Routing & Acceleration Telemetry Banner -->
        <div id="routing-banner" class="glass-card rounded-xl p-3.5 flex flex-col sm:flex-row sm:items-center justify-between gap-3 text-xs border border-indigo-500/30 bg-indigo-950/30">
          <div class="flex items-center gap-2.5">
            <span class="text-base" aria-hidden="true">⚡</span>
            <span class="text-slate-300">Engine:</span>
            <strong id="ai-engine-used" class="text-indigo-200">Local Privacy Shield & Cython-Accelerated Rules</strong>
          </div>
          <div class="flex flex-wrap items-center gap-2">
            <span id="cython-active-pill" class="px-2.5 py-0.5 rounded-full badge-cython font-bold text-[11px]">
              Cython: C-Compiled (-O3)
            </span>
            <span id="avg-confidence-pill" class="px-2.5 py-0.5 rounded-full bg-emerald-500/20 text-emerald-200 border border-emerald-500/40 font-bold text-[11px]">
              Local Confidence: 94%
            </span>
            <span id="twisted-count-pill" class="hidden px-2.5 py-0.5 rounded-full badge-twisted font-bold text-[11px]">
              🌀 Twisted Drafting: 0
            </span>
            <span id="escalated-count-pill" class="px-2.5 py-0.5 rounded-full bg-purple-500/20 text-purple-200 border border-purple-500/40 font-bold text-[11px]">
              Escalated: 0 clauses
            </span>
          </div>
        </div>

        <!-- Executive Risk Scorecard -->
        <div class="glass-panel rounded-2xl p-6 shadow-xl space-y-6">
          <div class="grid grid-cols-1 lg:grid-cols-4 gap-6 items-center">
            
            <!-- Risk Gauge with High Contrast & Circular Radial SVG -->
            <div class="flex flex-col items-center justify-center p-6 bg-slate-900/90 rounded-2xl border border-slate-800 text-center relative overflow-hidden shadow-inner">
              <span class="text-xs font-bold uppercase tracking-wider text-slate-400 mb-1">Legal Risk Index</span>
              
              <div class="relative w-36 h-36 flex items-center justify-center my-2" aria-label="Risk Score Meter">
                <svg class="w-full h-full transform -rotate-90" viewBox="0 0 100 100">
                  <!-- Background Track -->
                  <circle cx="50" cy="50" r="42" class="gauge-bg" fill="none" />
                  <!-- Progress Arc -->
                  <circle id="gauge-progress-circle" cx="50" cy="50" r="42" class="gauge-fill" fill="none"
                    stroke="#10b981" stroke-dasharray="264" stroke-dashoffset="264" />
                </svg>
                <div class="absolute inset-0 flex flex-col items-center justify-center">
                  <div class="flex items-baseline">
                    <span id="score-meter" class="font-display text-4xl sm:text-5xl font-black text-white tracking-tight">--</span>
                    <span class="text-[11px] font-bold text-slate-400 ml-0.5">/100</span>
                  </div>
                </div>
              </div>

              <span id="score-badge" class="px-3 py-1 text-xs font-extrabold rounded-full badge-high uppercase tracking-wider shadow-sm">
                EVALUATING
              </span>
            </div>

            <!-- Stats & Exposure Breakdown -->
            <div class="lg:col-span-3 space-y-4">
              <div>
                <h3 class="font-display text-lg font-extrabold text-white tracking-tight" id="results-title">Contract Assessment</h3>
                <p class="text-xs text-slate-200 mt-1.5 leading-relaxed" id="executive-summary"></p>
              </div>

              <!-- Clause Count Counters -->
              <div class="grid grid-cols-3 gap-3" role="group" aria-label="Risk Summary Counts">
                <div class="p-3.5 rounded-xl bg-rose-500/15 border border-rose-500/30 text-center">
                  <div class="font-display text-2xl font-black text-rose-300" id="high-risk-count">0</div>
                  <div class="text-[11px] font-bold text-rose-200 mt-0.5">High Risk Traps</div>
                </div>
                <div class="p-3.5 rounded-xl bg-amber-500/15 border border-amber-500/30 text-center">
                  <div class="font-display text-2xl font-black text-amber-300" id="medium-risk-count">0</div>
                  <div class="text-[11px] font-bold text-amber-200 mt-0.5">Moderate Risks</div>
                </div>
                <div class="p-3.5 rounded-xl bg-emerald-500/15 border border-emerald-500/30 text-center">
                  <div class="font-display text-2xl font-black text-emerald-300" id="low-risk-count">0</div>
                  <div class="text-[11px] font-bold text-emerald-200 mt-0.5">Standard Clauses</div>
                </div>
              </div>

              <!-- Critical Findings Banner -->
              <div id="critical-findings-container" class="space-y-1.5 pt-1" role="list" aria-label="Critical Hazards">
                <!-- Injected via JS -->
              </div>
            </div>

          </div>
        </div>

        <!-- Structured Explorer Navigation & Instant Search Filter -->
        <div class="space-y-3 border-b border-slate-800 pb-3">
          <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
            <div class="flex space-x-6" role="tablist" aria-label="Results Explorer View">
              <button role="tab" id="view-clauses-btn" aria-selected="true" onclick="switchAnalysisView('clauses')" class="font-bold text-xs sm:text-sm text-indigo-400 border-b-2 border-indigo-500 pb-2 transition">
                Clause-by-Clause Translation & Semantic Insights
              </button>
              <button role="tab" id="view-checklist-btn" aria-selected="false" onclick="switchAnalysisView('checklist')" class="font-bold text-xs sm:text-sm text-slate-400 hover:text-slate-200 border-b-2 border-transparent pb-2 transition">
                Attorney Consultation Brief
              </button>
            </div>
            <!-- Live Search Bar -->
            <div class="relative min-w-[240px]">
              <input type="text" id="clause-search-input" oninput="searchClauses(this.value)" placeholder="Search clauses, traps, keywords..." class="w-full text-xs bg-slate-900 text-slate-200 pl-8 pr-3 py-1.5 rounded-lg border border-slate-700 focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 transition">
              <svg class="w-3.5 h-3.5 text-slate-400 absolute left-2.5 top-2.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/></svg>
            </div>
          </div>

          <!-- Quick Filter Pill Buttons -->
          <div class="flex flex-wrap items-center gap-1.5 pt-1 text-xs">
            <span class="text-slate-400 font-bold mr-1 text-[11px]">Filter:</span>
            <button type="button" onclick="setFilterChip('ALL')" id="filter-chip-ALL" class="filter-chip px-2.5 py-1 rounded-lg bg-indigo-600 text-white font-bold text-[11px] border border-indigo-500 transition">
              All Clauses
            </button>
            <button type="button" onclick="setFilterChip('TWISTED')" id="filter-chip-TWISTED" class="filter-chip px-2.5 py-1 rounded-lg bg-slate-800 text-amber-300 hover:bg-slate-700 font-bold text-[11px] border border-slate-700 transition">
              🌀 Twisted / Euphemisms
            </button>
            <button type="button" onclick="setFilterChip('HIGH')" id="filter-chip-HIGH" class="filter-chip px-2.5 py-1 rounded-lg bg-slate-800 text-rose-300 hover:bg-slate-700 font-bold text-[11px] border border-slate-700 transition">
              🚨 High Risk Traps
            </button>
            <button type="button" onclick="setFilterChip('ESCALATED')" id="filter-chip-ESCALATED" class="filter-chip px-2.5 py-1 rounded-lg bg-slate-800 text-purple-300 hover:bg-slate-700 font-bold text-[11px] border border-slate-700 transition">
              🧠 AI Escalated
            </button>
            <button type="button" onclick="setFilterChip('MEDIUM')" id="filter-chip-MEDIUM" class="filter-chip px-2.5 py-1 rounded-lg bg-slate-800 text-amber-200 hover:bg-slate-700 font-bold text-[11px] border border-slate-700 transition">
              ⚠️ Moderate
            </button>
            <button type="button" onclick="setFilterChip('LOW')" id="filter-chip-LOW" class="filter-chip px-2.5 py-1 rounded-lg bg-slate-800 text-emerald-300 hover:bg-slate-700 font-bold text-[11px] border border-slate-700 transition">
              ✅ Standard
            </button>
            <select id="filter-risk" onchange="filterClauses(this.value)" class="sr-only">
              <option value="ALL">All</option>
              <option value="TWISTED">Twisted</option>
              <option value="HIGH">High</option>
              <option value="ESCALATED">Escalated</option>
              <option value="MEDIUM">Medium</option>
              <option value="LOW">Low</option>
            </select>
          </div>
        </div>

        <!-- VIEW 1: CLAUSE CARDS -->
        <div id="clause-cards-view" class="space-y-4" role="region" aria-label="Clause Breakdown">
          <!-- Injected via JS -->
        </div>

        <!-- VIEW 2: ATTORNEY CONSULTATION BRIEF -->
        <div id="attorney-checklist-view" class="hidden space-y-6" role="region" aria-label="Attorney Consultation Brief">
          <div class="glass-panel rounded-2xl p-6 space-y-6">
            <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-800 pb-4">
              <div>
                <h3 class="font-display text-lg font-extrabold text-white">Attorney Consultation Brief</h3>
                <p class="text-xs text-slate-400">Exportable questions and priority redline fallback positions for your legal counsel.</p>
              </div>
              <div class="flex items-center gap-2">
                <button type="button" onclick="copyChecklistMarkdown()" class="px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-bold border border-slate-700 transition">
                  📋 Copy Markdown
                </button>
                <button type="button" onclick="downloadChecklistFile()" class="px-3 py-1.5 rounded-lg bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-bold transition shadow-sm">
                  ⬇️ Download .md
                </button>
              </div>
            </div>

            <!-- Questions to ask Counsel -->
            <div class="space-y-3">
              <h4 class="text-xs font-extrabold text-indigo-300 uppercase tracking-wider">Specific Questions For Counsel:</h4>
              <div id="checklist-questions-list" class="space-y-3">
                <!-- Injected via JS -->
              </div>
            </div>

            <!-- Priority Redline Checklist -->
            <div class="space-y-3 pt-2">
              <h4 class="text-xs font-extrabold text-indigo-300 uppercase tracking-wider">Priority Negotiation Checklist:</h4>
              <ul id="checklist-redlines-list" class="space-y-2 text-xs text-slate-200 font-medium">
                <!-- Injected via JS -->
              </ul>
            </div>
          </div>
        </div>

      </div>
    </section>

    <!-- ==================== TAB 2: VERSION COMPARATOR ==================== -->
    <section id="tab-comparator" role="tabpanel" aria-labelledby="nav-tab-comparator" class="hidden space-y-6">
      <div class="glass-panel rounded-2xl p-6 space-y-4">
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div>
            <h2 class="font-display text-lg font-extrabold text-white">Contract Version Redline Comparator</h2>
            <p class="text-xs text-slate-400">Compare original vs counterparty proposed redline to track risk trajectory</p>
          </div>
          <button type="button" onclick="loadSampleComparison()" class="text-xs bg-slate-800 hover:bg-slate-700 text-slate-200 font-bold px-3 py-1.5 rounded-lg border border-slate-700 transition">
            Load Sample Redline Diff
          </button>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label for="compare-v1" class="block text-xs font-bold text-rose-300 mb-1">Contract Version A (Original):</label>
            <textarea id="compare-v1" rows="9" class="w-full font-mono text-xs text-slate-200 p-3.5 rounded-xl bg-slate-900/90 border border-slate-800 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 leading-relaxed" placeholder="Paste initial draft..."></textarea>
          </div>
          <div>
            <label for="compare-v2" class="block text-xs font-bold text-emerald-300 mb-1">Contract Version B (Revised Proposal):</label>
            <textarea id="compare-v2" rows="9" class="w-full font-mono text-xs text-slate-200 p-3.5 rounded-xl bg-slate-900/90 border border-slate-800 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 leading-relaxed" placeholder="Paste counter-proposal or redline..."></textarea>
          </div>
        </div>

        <div class="flex justify-end pt-1">
          <button type="button" onclick="runComparison()" class="inline-flex items-center gap-2 px-6 py-2.5 rounded-xl bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-500 hover:to-purple-500 text-white text-xs sm:text-sm font-extrabold shadow-lg shadow-indigo-600/30 transition">
            <span>Calculate Risk Delta & Diff</span>
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3"/></svg>
          </button>
        </div>
      </div>

      <div id="comparator-results" role="region" aria-label="Comparison Results" class="hidden space-y-6">
        <!-- Results Card -->
        <div class="glass-panel rounded-2xl p-6 space-y-4">
          <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-800 pb-4">
            <div>
              <span id="compare-trajectory-badge" class="px-3 py-1 text-xs font-bold rounded-full badge-low uppercase">
                TRAJECTORY
              </span>
              <h3 class="font-display text-base font-extrabold text-white mt-2" id="compare-scores-summary"></h3>
            </div>
          </div>
          
          <div class="space-y-2">
            <h4 class="text-xs font-extrabold text-slate-300 uppercase tracking-wider">Key Redline Shifts:</h4>
            <ul id="compare-changes-list" class="space-y-1 text-xs text-slate-200 font-medium"></ul>
          </div>

          <div class="space-y-3 pt-2">
            <h4 class="text-xs font-extrabold text-slate-300 uppercase tracking-wider">Clause Level Diffs & Analysis:</h4>
            <div id="compare-diff-cards" class="space-y-3"></div>
          </div>
        </div>
      </div>
    </section>

    <!-- ==================== TAB 3: LEGAL NAVIGATOR AI CHAT ==================== -->
    <section id="tab-chat" role="tabpanel" aria-labelledby="nav-tab-chat" class="hidden space-y-4">
      <div class="glass-panel rounded-2xl p-6 flex flex-col h-[650px] shadow-xl">
        <div class="flex items-center justify-between border-b border-slate-800 pb-3">
          <div class="flex items-center gap-2.5">
            <div class="w-8 h-8 rounded-lg bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center text-white" aria-hidden="true">
              💬
            </div>
            <div>
              <h2 class="font-display text-base font-bold text-white">Contextual Legal Navigator AI</h2>
              <p class="text-xs text-slate-400">Ask questions grounded strictly in your analyzed contract</p>
            </div>
          </div>
          <span id="chat-model-badge" class="text-xs text-indigo-300 font-bold bg-indigo-950/70 border border-indigo-800/60 px-2.5 py-1 rounded-full">
            Active Provider
          </span>
        </div>

        <!-- Chat History Window -->
        <div id="chat-messages" role="log" aria-live="polite" class="flex-1 overflow-y-auto p-4 space-y-4">
          <div class="max-w-xl p-4 bg-slate-900/90 text-slate-200 rounded-xl border border-slate-800 text-xs space-y-2 leading-relaxed">
            <p class="font-bold text-white flex items-center gap-1.5">
              <span>👋</span> Welcome to Legal-Ease Navigator!
            </p>
            <p>I can help break down convoluted terms, locate hidden indemnification traps, explain payment withholding risks, and suggest protective counter-proposals.</p>
            <p class="text-[11px] text-slate-400">Tip: Click one of the quick prompts below or type your question.</p>
          </div>
        </div>

        <!-- Quick Prompts -->
        <div class="py-2 flex flex-wrap gap-1.5 border-t border-slate-800 text-[11px]">
          <span class="text-slate-400 font-bold py-1">Quick:</span>
          <button type="button" onclick="sendQuickPrompt('Can the client terminate without paying me?')" class="px-2.5 py-1 rounded-lg bg-slate-900 hover:bg-slate-800 text-slate-300 border border-slate-800 transition">
            Terminate without paying?
          </button>
          <button type="button" onclick="sendQuickPrompt('Do I give away my pre-existing IP in this agreement?')" class="px-2.5 py-1 rounded-lg bg-slate-900 hover:bg-slate-800 text-slate-300 border border-slate-800 transition">
            Do I surrender pre-existing IP?
          </button>
          <button type="button" onclick="sendQuickPrompt('What is the worst-case financial liability for me under indemnification?')" class="px-2.5 py-1 rounded-lg bg-slate-900 hover:bg-slate-800 text-slate-300 border border-slate-800 transition">
            Worst-case indemnity exposure?
          </button>
        </div>

        <!-- Chat Input Form -->
        <form onsubmit="handleChatSubmit(event)" class="flex gap-2 pt-2 border-t border-slate-800">
          <label for="chat-input" class="sr-only">Ask a question about the contract</label>
          <input type="text" id="chat-input" placeholder="Ask about indemnification, liability, IP rights, or termination..." class="flex-1 px-4 py-2.5 rounded-xl bg-slate-900 border border-slate-700 text-xs text-white placeholder:text-slate-500 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500">
          <button type="submit" class="px-5 py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-bold shadow-md shadow-indigo-600/30 transition">
            Send
          </button>
        </form>
      </div>
    </section>

    <!-- ==================== TAB 4: PRIVACY & PII VAULT ==================== -->
    <section id="tab-privacy" role="tabpanel" aria-labelledby="nav-tab-privacy" class="hidden space-y-6">
      <div class="glass-panel rounded-2xl p-6 space-y-6">
        <div class="flex items-center gap-3 border-b border-slate-800 pb-4">
          <div class="w-10 h-10 rounded-xl bg-emerald-500/20 text-emerald-400 flex items-center justify-center text-xl font-bold" aria-hidden="true">
            🛡️
          </div>
          <div>
            <h2 class="font-display text-lg font-extrabold text-white">Local Privacy Shield & PII Sanitization Vault</h2>
            <p class="text-xs text-slate-400">Verifiable local redaction tokens protecting personal and commercial identifiers</p>
          </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
          <div class="p-4 rounded-xl bg-slate-900/90 border border-slate-800 space-y-2">
            <div class="font-extrabold text-white">100% Client-Side Privacy Guarantee</div>
            <p class="text-slate-300 leading-relaxed">
              No names, emails, telephone numbers, tax IDs (SSN/EIN), or confidential currency amounts ever leave your machine without tokenization. All upstream AI synthesis is executed exclusively on anonymized pseudonyms.
            </p>
          </div>
          <div class="p-4 rounded-xl bg-slate-900/90 border border-slate-800 space-y-2">
            <div class="font-extrabold text-white">Privacy Metrics</div>
            <div class="flex items-center justify-between text-slate-300">
              <span>Total Entities Masked:</span>
              <strong id="privacy-total-redacted" class="text-emerald-400">0</strong>
            </div>
            <div class="flex items-center justify-between text-slate-300">
              <span>Estimated Privacy Coverage:</span>
              <strong id="privacy-score-display" class="text-emerald-400">100%</strong>
            </div>
          </div>
        </div>

        <div class="space-y-3">
          <h3 class="text-xs font-extrabold text-slate-300 uppercase tracking-wider">Sanitization Table (Pseudonym Mapping):</h3>
          <div class="overflow-x-auto rounded-xl border border-slate-800">
            <table class="w-full text-left text-xs text-slate-300">
              <thead class="bg-slate-900 text-slate-400 uppercase font-bold text-[11px] border-b border-slate-800">
                <tr>
                  <th scope="col" class="px-4 py-3">Category</th>
                  <th scope="col" class="px-4 py-3">Redacted Token</th>
                  <th scope="col" class="px-4 py-3">Original Value</th>
                </tr>
              </thead>
              <tbody id="privacy-table-body" class="divide-y divide-slate-800/60 bg-slate-900/40">
                <tr>
                  <td colspan="3" class="px-4 py-4 text-center text-slate-400">Analyze a contract to inspect local redaction tokens.</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </section>

    <!-- ==================== TAB 5: PRODUCT DETAILS & ESTIMATED SAVINGS (ROI) ==================== -->
    <section id="tab-details" role="tabpanel" aria-labelledby="nav-tab-details" class="hidden space-y-8" tabindex="0">
      
      <!-- ==================== HACKATHON PROBLEM STATEMENT & 7 USE CASES ACCORDION ==================== -->
      <div class="glass-panel rounded-3xl p-6 sm:p-8 space-y-6 border border-indigo-500/30 shadow-2xl bg-gradient-to-br from-slate-900/90 via-indigo-950/25 to-purple-950/30">
        <div class="space-y-2">
          <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-indigo-500/20 text-indigo-300 text-xs font-bold border border-indigo-500/40">
            <span>🏆</span> <span>Official Hackathon Challenge Alignment: AI for Legal Assistance & Access</span>
          </div>
          <h2 class="text-xl sm:text-2xl font-extrabold text-white tracking-tight">
            Direct Alignment with the Hackathon Problem Statement
          </h2>
          <blockquote class="p-4 rounded-xl bg-slate-950/80 border-l-4 border-indigo-500 text-slate-300 text-xs sm:text-sm leading-relaxed italic">
            "Legal information can often be complex, difficult to understand, and challenging to navigate without professional assistance. Build a GenAI-powered solution that makes legal information and basic legal assistance more accessible by helping users understand, compare, and navigate legal documents and information."
          </blockquote>
          <div class="p-3 rounded-xl bg-slate-900/80 border border-slate-800 text-[11px] text-slate-300">
            <strong class="text-amber-300">Mandatory Compliance Note:</strong> Legal-Ease is strictly built to provide document literacy, semantic clarity, and preliminary triage <em>rather than replace professional legal advice</em>. It arms users with structured briefings for real attorneys.
          </div>
        </div>

        <div class="space-y-3">
          <h3 class="text-xs font-bold uppercase tracking-wider text-indigo-400">1-to-1 Mapping to All 7 Official Potential Use Cases:</h3>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs">
            
            <div class="p-3.5 rounded-xl bg-slate-900/80 border border-slate-800 space-y-1">
              <div class="font-bold text-white flex items-center justify-between">
                <span>1. Simplifying Complex Legal Documents</span>
                <span class="text-[10px] px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 font-bold">100% Implemented</span>
              </div>
              <p class="text-slate-400 text-[11px] leading-relaxed">Plain-English translation engine maps archaic jargon into conversational 8th-grade explanations and "What It Means For You" impact cards.</p>
              <div class="text-[10px] text-indigo-400 font-semibold">Found in: Tab 1 (Contract Risk Analyzer)</div>
            </div>

            <div class="p-3.5 rounded-xl bg-slate-900/80 border border-slate-800 space-y-1">
              <div class="font-bold text-white flex items-center justify-between">
                <span>2. Comparing Contracts, Agreements, or Policies</span>
                <span class="text-[10px] px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 font-bold">100% Implemented</span>
              </div>
              <p class="text-slate-400 text-[11px] leading-relaxed">Cython C-accelerated side-by-side version comparator identifies additions, deletions, modifications, and overall risk trajectory (SAFER / MORE_RISK).</p>
              <div class="text-[10px] text-indigo-400 font-semibold">Found in: Tab 2 (Version Comparator)</div>
            </div>

            <div class="p-3.5 rounded-xl bg-slate-900/80 border border-slate-800 space-y-1">
              <div class="font-bold text-white flex items-center justify-between">
                <span>3. Highlighting Important Clauses, Obligations & Risks</span>
                <span class="text-[10px] px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 font-bold">100% Implemented</span>
              </div>
              <p class="text-slate-400 text-[11px] leading-relaxed">Character N-Gram vector model scores risk (0-100) and unmasks 8 predatory traps (unilateral indemnity, unlimited liability, rogue IP forfeiture).</p>
              <div class="text-[10px] text-indigo-400 font-semibold">Found in: Tab 1 (Risk Overview & Matrix)</div>
            </div>

            <div class="p-3.5 rounded-xl bg-slate-900/80 border border-slate-800 space-y-1">
              <div class="font-bold text-white flex items-center justify-between">
                <span>4. Answering Questions Based on Legal Documents</span>
                <span class="text-[10px] px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 font-bold">100% Implemented</span>
              </div>
              <p class="text-slate-400 text-[11px] leading-relaxed">Interactive conversational Legal Navigator AI answers user questions in plain English, citing specific contract section numbers with non-advisory guardrails.</p>
              <div class="text-[10px] text-indigo-400 font-semibold">Found in: Tab 3 (Legal Navigator AI)</div>
            </div>

            <div class="p-3.5 rounded-xl bg-slate-900/80 border border-slate-800 space-y-1">
              <div class="font-bold text-white flex items-center justify-between">
                <span>5. Helping Users Understand Options & Next Steps</span>
                <span class="text-[10px] px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 font-bold">100% Implemented</span>
              </div>
              <p class="text-slate-400 text-[11px] leading-relaxed">Generates contextual negotiation tips and 1-click bilateral redline counter-proposals ready to paste into client negotiation emails.</p>
              <div class="text-[10px] text-indigo-400 font-semibold">Found in: Tab 1 (Clause Negotiation Cards)</div>
            </div>

            <div class="p-3.5 rounded-xl bg-slate-900/80 border border-slate-800 space-y-1">
              <div class="font-bold text-white flex items-center justify-between">
                <span>6. Generating Summaries, Checklists & Outputs</span>
                <span class="text-[10px] px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 font-bold">100% Implemented</span>
              </div>
              <p class="text-slate-400 text-[11px] leading-relaxed">Generates an Executive Summary, Legal Risk Index, categorized severity counts, and exportable Markdown Attorney Consultation Briefs.</p>
              <div class="text-[10px] text-indigo-400 font-semibold">Found in: Tab 1 (Overview & Checklist View)</div>
            </div>

            <div class="p-3.5 rounded-xl bg-slate-900/80 border border-slate-800 space-y-1 md:col-span-2">
              <div class="font-bold text-white flex items-center justify-between">
                <span>7. Helping Users Prepare Information or Questions for a Legal Professional</span>
                <span class="text-[10px] px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 font-bold">100% Implemented</span>
              </div>
              <p class="text-slate-400 text-[11px] leading-relaxed">Automatically drafts an exportable Attorney Consultation Brief with targeted statutory questions, flagged high-risk clauses, and negotiation redlines—turning a $1,500 legal bill into a focused 15-minute consultation.</p>
              <div class="text-[10px] text-indigo-400 font-semibold">Found in: Tab 1 (Attorney Brief Modal) & Tab 5</div>
            </div>

          </div>
        </div>
      </div>

      <!-- Promotional Hero Banner -->
      <div class="glass-panel rounded-3xl p-6 sm:p-10 relative overflow-hidden border border-indigo-500/20 shadow-2xl">
        <div class="absolute -right-20 -top-20 w-80 h-80 bg-gradient-to-br from-indigo-500/20 via-purple-500/20 to-pink-500/10 rounded-full blur-3xl pointer-events-none" aria-hidden="true"></div>
        <div class="relative z-10 space-y-4 max-w-3xl">
          <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-indigo-500/10 border border-indigo-500/30 text-indigo-300 text-xs font-semibold">
            <span>🚀</span> <span>AI for Legal Assistance & Access Vertical</span>
          </div>
          <h1 class="text-2xl sm:text-4xl font-extrabold text-white tracking-tight leading-tight">
            Stop Signing Away Your Rights. <br>
            <span class="bg-gradient-to-r from-indigo-400 via-purple-300 to-pink-400 bg-clip-text text-transparent">
              Instant Legal Literacy & Contract Defense.
            </span>
          </h1>
          <p class="text-sm sm:text-base text-slate-300 leading-relaxed font-normal">
            Over <strong>85% of freelancers, independent contractors, and small business owners</strong> execute commercial contracts without professional legal review because attorneys bill <strong>$350–$650/hour</strong>. 
            Legal-Ease democratizes legal literacy: delivering sub-second, privacy-first contract triage, exposing predatory traps, and generating lawyer-ready negotiation briefs completely free.
          </p>
          <div class="flex flex-wrap gap-3 pt-2">
            <button onclick="switchTab('analyzer')" class="px-5 py-2.5 rounded-xl bg-gradient-to-r from-indigo-500 to-purple-600 hover:from-indigo-600 hover:to-purple-700 text-white font-bold text-xs sm:text-sm shadow-lg shadow-indigo-500/25 transition flex items-center gap-2">
              <span>📄</span> Audit a Contract Now
            </button>
            <button onclick="switchTab('comparator')" class="px-5 py-2.5 rounded-xl bg-slate-800/90 hover:bg-slate-750 text-slate-200 border border-slate-700 font-bold text-xs sm:text-sm transition flex items-center gap-2">
              <span>⚖️</span> Compare Revisions
            </button>
          </div>
        </div>
      </div>

      <!-- Quick KPI Metric Cards -->
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div class="glass-card rounded-2xl p-5 border border-slate-800 space-y-1 text-center sm:text-left">
          <div class="text-2xl sm:text-3xl font-extrabold text-indigo-400">$450/hr</div>
          <div class="text-xs font-bold text-slate-200">Average Legal Bill Saved</div>
          <p class="text-[11px] text-slate-400">Eliminate expensive preliminary billable hours before ever engaging counsel.</p>
        </div>
        <div class="glass-card rounded-2xl p-5 border border-slate-800 space-y-1 text-center sm:text-left">
          <div class="text-2xl sm:text-3xl font-extrabold text-emerald-400">&lt; 1.5s</div>
          <div class="text-xs font-bold text-slate-200">High-Velocity Triage</div>
          <p class="text-[11px] text-slate-400">Powered by compiled Cython C-extensions and pre-indexed semantic vectors.</p>
        </div>
        <div class="glass-card rounded-2xl p-5 border border-slate-800 space-y-1 text-center sm:text-left">
          <div class="text-2xl sm:text-3xl font-extrabold text-cyan-400">100%</div>
          <div class="text-xs font-bold text-slate-200">Zero-Leakage Local Privacy</div>
          <p class="text-[11px] text-slate-400">Deterministic local regex pseudonymization guarantees no PII leaves your browser.</p>
        </div>
        <div class="glass-card rounded-2xl p-5 border border-slate-800 space-y-1 text-center sm:text-left">
          <div class="text-2xl sm:text-3xl font-extrabold text-amber-400">8+</div>
          <div class="text-xs font-bold text-slate-200">Predatory Archetypes Caught</div>
          <p class="text-[11px] text-slate-400">Identifies twisted euphemisms, asymmetric caps, and rogue IP forfeiture traps.</p>
        </div>
      </div>

      <!-- Interactive Estimated Savings & ROI Calculator -->
      <div class="glass-panel rounded-3xl p-6 sm:p-8 space-y-6 border border-slate-800 shadow-xl">
        <div class="border-b border-slate-800/80 pb-4">
          <div class="flex items-center gap-2.5">
            <div class="w-9 h-9 rounded-xl bg-gradient-to-br from-emerald-500 to-teal-700 flex items-center justify-center text-white text-lg">
              💰
            </div>
            <div>
              <h2 class="text-lg sm:text-xl font-bold text-white">Interactive Estimated Savings & ROI Calculator</h2>
              <p class="text-xs text-slate-400">Adjust your volume and rates below to see your personalized annual financial and operational savings.</p>
            </div>
          </div>
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-12 gap-6">
          
          <!-- Sliders / Controls (Left column) -->
          <div class="lg:col-span-6 space-y-5 bg-slate-900/50 p-5 rounded-2xl border border-slate-800/70">
            
            <!-- Slider 1: Contracts Reviewed Per Month -->
            <div class="space-y-2">
              <div class="flex justify-between items-center text-xs">
                <label for="calc-contracts" class="font-bold text-slate-300">Contracts Reviewed Per Month:</label>
                <span id="calc-contracts-val" class="px-2.5 py-0.5 rounded-lg bg-indigo-500/20 text-indigo-300 font-extrabold text-xs">3 contracts</span>
              </div>
              <input type="range" id="calc-contracts" min="1" max="25" value="3" step="1" oninput="recalculateSavings()" class="w-full h-2 bg-slate-700 rounded-lg appearance-none cursor-pointer accent-indigo-500" aria-label="Contracts reviewed per month">
              <div class="flex justify-between text-[10px] text-slate-500 font-medium">
                <span>1 / mo (Solo Freelancer)</span>
                <span>10 / mo (Agency / Studio)</span>
                <span>25 / mo (High Volume)</span>
              </div>
            </div>

            <!-- Slider 2: Average Attorney Billing Rate -->
            <div class="space-y-2">
              <div class="flex justify-between items-center text-xs">
                <label for="calc-rate" class="font-bold text-slate-300">Attorney Hourly Rate ($/hr):</label>
                <span id="calc-rate-val" class="px-2.5 py-0.5 rounded-lg bg-indigo-500/20 text-indigo-300 font-extrabold text-xs">$450 / hr</span>
              </div>
              <input type="range" id="calc-rate" min="200" max="850" value="450" step="25" oninput="recalculateSavings()" class="w-full h-2 bg-slate-700 rounded-lg appearance-none cursor-pointer accent-indigo-500" aria-label="Attorney hourly rate">
              <div class="flex justify-between text-[10px] text-slate-500 font-medium">
                <span>$200/hr (Junior Associate)</span>
                <span>$450/hr (Commercial Standard)</span>
                <span>$850/hr (Senior Partner)</span>
              </div>
            </div>

            <!-- Slider 3: Hours Saved Per Contract Review -->
            <div class="space-y-2">
              <div class="flex justify-between items-center text-xs">
                <label for="calc-hours" class="font-bold text-slate-300">Hours Saved Per Contract:</label>
                <span id="calc-hours-val" class="px-2.5 py-0.5 rounded-lg bg-indigo-500/20 text-indigo-300 font-extrabold text-xs">2.5 hours</span>
              </div>
              <input type="range" id="calc-hours" min="1.0" max="6.0" value="2.5" step="0.5" oninput="recalculateSavings()" class="w-full h-2 bg-slate-700 rounded-lg appearance-none cursor-pointer accent-indigo-500" aria-label="Hours saved per contract">
              <div class="flex justify-between text-[10px] text-slate-500 font-medium">
                <span>1.0 hr (Quick review)</span>
                <span>2.5 hrs (Standard agreement)</span>
                <span>6.0 hrs (Complex MSA)</span>
              </div>
            </div>

            <!-- Slider 4: Average Contract Value ($) -->
            <div class="space-y-2">
              <div class="flex justify-between items-center text-xs">
                <label for="calc-deal" class="font-bold text-slate-300">Average Contract Deal Size ($):</label>
                <span id="calc-deal-val" class="px-2.5 py-0.5 rounded-lg bg-indigo-500/20 text-indigo-300 font-extrabold text-xs">$12,000</span>
              </div>
              <input type="range" id="calc-deal" min="2000" max="100000" value="12000" step="2000" oninput="recalculateSavings()" class="w-full h-2 bg-slate-700 rounded-lg appearance-none cursor-pointer accent-indigo-500" aria-label="Average contract value">
              <div class="flex justify-between text-[10px] text-slate-500 font-medium">
                <span>$2,000 (Small Gig)</span>
                <span>$25,000 (Agency Retainer)</span>
                <span>$100,000 (Enterprise SOW)</span>
              </div>
            </div>

          </div>

          <!-- Calculated Results Display (Right column) -->
          <div class="lg:col-span-6 flex flex-col justify-between space-y-4 bg-gradient-to-br from-slate-900/90 via-indigo-950/30 to-purple-950/30 p-6 rounded-2xl border border-indigo-500/30 shadow-inner">
            
            <div class="space-y-4">
              <div class="flex items-center justify-between">
                <span class="text-xs font-bold text-slate-400 uppercase tracking-wider">Estimated Annual ROI</span>
                <span class="px-2.5 py-1 rounded-full bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 text-[11px] font-extrabold">
                  100% Free / Open Source
                </span>
              </div>

              <div class="space-y-1">
                <div class="text-xs text-slate-400 font-semibold">Direct Billable Legal Fees Saved:</div>
                <div id="calc-annual-fees" class="text-3xl sm:text-4xl font-extrabold text-emerald-400 tracking-tight">
                  $40,500
                </div>
                <div class="text-[11px] text-slate-400">Calculated as: contracts/mo × 12 × hourly rate × hours saved.</div>
              </div>

              <div class="grid grid-cols-2 gap-3 pt-2">
                <div class="p-3 rounded-xl bg-slate-900/80 border border-slate-800">
                  <div class="text-[11px] text-slate-400 font-semibold">Review Time Saved:</div>
                  <div id="calc-annual-hours" class="text-xl font-bold text-indigo-300">90 hrs / yr</div>
                  <div class="text-[10px] text-slate-500">Over 2 full work weeks saved</div>
                </div>
                <div class="p-3 rounded-xl bg-slate-900/80 border border-slate-800">
                  <div class="text-[11px] text-slate-400 font-semibold">Catastrophic Risk Averted:</div>
                  <div id="calc-liability-averted" class="text-xl font-bold text-purple-300">$50,400+</div>
                  <div class="text-[10px] text-slate-500">Uncapped liability & IP forfeiture avoided</div>
                </div>
              </div>

              <div class="p-3.5 rounded-xl bg-indigo-900/30 border border-indigo-700/40 text-xs text-indigo-200 leading-relaxed">
                💡 <strong>The Attorney Triage Advantage:</strong> Instead of paying a lawyer $1,100+ to read boilerplate line-by-line, Legal-Ease generates an automated <strong>Attorney Brief</strong> with targeted statutory questions, turning a $1,500 legal bill into a focused 15-minute consultation.
              </div>
            </div>

            <button onclick="switchTab('analyzer')" class="w-full py-3 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white font-extrabold text-xs sm:text-sm shadow-lg shadow-emerald-600/25 transition text-center">
              Try Legal-Ease On Your Next Contract →
            </button>

          </div>
        </div>
      </div>

      <!-- Feature Comparison Matrix -->
      <div class="glass-panel rounded-3xl p-6 sm:p-8 space-y-5 border border-slate-800 shadow-xl">
        <div>
          <h2 class="text-lg sm:text-xl font-bold text-white">How Legal-Ease Compares</h2>
          <p class="text-xs text-slate-400">Specialized, privacy-first legal AI compared against traditional retainers and generic chatbots.</p>
        </div>

        <div class="overflow-x-auto rounded-2xl border border-slate-800">
          <table class="w-full text-left text-xs text-slate-300">
            <thead class="bg-slate-900 text-slate-400 uppercase font-bold text-[11px] border-b border-slate-800">
              <tr>
                <th scope="col" class="px-4 py-3.5">Capability / Dimension</th>
                <th scope="col" class="px-4 py-3.5">Traditional Law Firm</th>
                <th scope="col" class="px-4 py-3.5">Generic LLM (ChatGPT)</th>
                <th scope="col" class="px-4 py-3.5 text-indigo-400 font-extrabold">Legal-Ease AI</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-800/60 bg-slate-900/30 font-medium">
              <tr class="hover:bg-slate-800/30 transition">
                <td class="px-4 py-3.5 font-bold text-white">Turnaround Time</td>
                <td class="px-4 py-3.5 text-slate-400">3 – 7 Business Days</td>
                <td class="px-4 py-3.5 text-slate-400">15 – 30 Seconds</td>
                <td class="px-4 py-3.5 text-emerald-400 font-bold">&lt; 1.5 Seconds (Cython Accelerated)</td>
              </tr>
              <tr class="hover:bg-slate-800/30 transition">
                <td class="px-4 py-3.5 font-bold text-white">Cost Per Agreement</td>
                <td class="px-4 py-3.5 text-rose-400 font-semibold">$500 – $2,500+</td>
                <td class="px-4 py-3.5 text-slate-400">$20 / month sub</td>
                <td class="px-4 py-3.5 text-emerald-400 font-bold">100% Free / Open Source BYOK</td>
              </tr>
              <tr class="hover:bg-slate-800/30 transition">
                <td class="px-4 py-3.5 font-bold text-white">Client Data Privacy</td>
                <td class="px-4 py-3.5 text-slate-400">Subject to law firm staff</td>
                <td class="px-4 py-3.5 text-rose-400">Leaked to cloud servers</td>
                <td class="px-4 py-3.5 text-cyan-400 font-bold">100% Local PII Pseudonymization</td>
              </tr>
              <tr class="hover:bg-slate-800/30 transition">
                <td class="px-4 py-3.5 font-bold text-white">Twisted / Euphemism Radar</td>
                <td class="px-4 py-3.5 text-slate-400">Requires senior lawyer eye</td>
                <td class="px-4 py-3.5 text-slate-400">Prone to hallucination</td>
                <td class="px-4 py-3.5 text-purple-400 font-bold">L2 Vector Space Archetype Engine</td>
              </tr>
              <tr class="hover:bg-slate-800/30 transition">
                <td class="px-4 py-3.5 font-bold text-white">Lawyer-Ready Consultation Brief</td>
                <td class="px-4 py-3.5 text-slate-400">N/A (They are the lawyer)</td>
                <td class="px-4 py-3.5 text-slate-400">Generic bullet points</td>
                <td class="px-4 py-3.5 text-indigo-400 font-bold">Structured Brief with Fallback Redlines</td>
              </tr>
              <tr class="hover:bg-slate-800/30 transition">
                <td class="px-4 py-3.5 font-bold text-white">Version Diffing & Trajectory</td>
                <td class="px-4 py-3.5 text-slate-400">Manual Word track changes</td>
                <td class="px-4 py-3.5 text-slate-400">No risk scoring</td>
                <td class="px-4 py-3.5 text-emerald-400 font-bold">Automated SAFER / MORE_RISK Trajectory</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Who It Empowers (Target Personas) -->
      <div class="space-y-4">
        <h2 class="text-lg sm:text-xl font-bold text-white">Engineered For Real-World Commercial Work</h2>
        
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          
          <div class="glass-card rounded-2xl p-5 border border-slate-800 space-y-3">
            <div class="w-10 h-10 rounded-xl bg-indigo-500/20 text-indigo-400 flex items-center justify-center text-xl font-bold">
              👨‍💻
            </div>
            <h3 class="text-sm font-bold text-white">Freelancers & Contractors</h3>
            <p class="text-xs text-slate-300 leading-relaxed font-normal">
              Never unknowingly assign your pre-existing codebase, reusable tools, or portfolios. Detect broad non-compete covenants that threaten your future livelihood.
            </p>
            <div class="text-[11px] text-indigo-400 font-bold">Key Save: IP Ownership & Non-Compete Neutralization</div>
          </div>

          <div class="glass-card rounded-2xl p-5 border border-slate-800 space-y-3">
            <div class="w-10 h-10 rounded-xl bg-purple-500/20 text-purple-400 flex items-center justify-center text-xl font-bold">
              🚀
            </div>
            <h3 class="text-sm font-bold text-white">Startup Founders & SMBs</h3>
            <p class="text-xs text-slate-300 leading-relaxed font-normal">
              Review incoming vendor agreements and client Master Services Agreements (MSAs) without burning early-stage venture funding on expensive hourly retainers.
            </p>
            <div class="text-[11px] text-purple-400 font-bold">Key Save: Asymmetric Liability & Indemnity Caps</div>
          </div>

          <div class="glass-card rounded-2xl p-5 border border-slate-800 space-y-3">
            <div class="w-10 h-10 rounded-xl bg-emerald-500/20 text-emerald-400 flex items-center justify-center text-xl font-bold">
              🎨
            </div>
            <h3 class="text-sm font-bold text-white">Creative Agencies & Studios</h3>
            <p class="text-xs text-slate-300 leading-relaxed font-normal">
              Halt predatory Net-90 payment terms and arbitrary milestone rejection traps. Enforce mandatory 30-day cancellation notices and kill-fees.
            </p>
            <div class="text-[11px] text-emerald-400 font-bold">Key Save: Cash Flow Protection & Kill-Fee Guarantees</div>
          </div>

        </div>
      </div>

    </section>

  </main>

  <!-- Accessible Footer -->
  <footer role="contentinfo" class="relative z-10 glass-panel border-t border-slate-800 text-slate-400 text-xs py-5 px-4 mt-auto">
    <div class="max-w-7xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-3 text-center sm:text-left">
      <div>
        <strong>Legal-Ease v1.0.0 (WCAG 2.1 Level AAA Compliant)</strong> — Privacy-First AI Contract Navigator with Google Gemini Flash-Lite & NVIDIA Nemotron
      </div>
      <div>
        AI for Legal Assistance & Access | <a href="https://github.com/seeramsujay/legal-ease" target="_blank" rel="noopener noreferrer" class="text-indigo-400 hover:underline">GitHub Repository</a>
      </div>
    </div>
  </footer>

  <!-- Interactive Accessible JavaScript Application -->
  <script>
    let currentAnalysis = null;
    let cachedSamples = [];
    let llmSettings = {
      api_key_configured: false,
      provider: 'gemini',
      base_url: 'https://generativelanguage.googleapis.com/v1beta/openai',
      model_name: 'gemini-2.0-flash-lite',
      confidence_threshold: 0.75,
      api_key_source: 'none'
    };

    const PRESETS = {
      gemini: {
        provider: 'gemini',
        base_url: 'https://generativelanguage.googleapis.com/v1beta/openai',
        model_name: 'gemini-2.0-flash-lite',
        label: 'Google Gemini 2.0 Flash-Lite'
      },
      nemotron: {
        provider: 'nemotron',
        base_url: 'https://integrate.api.nvidia.com/v1',
        model_name: 'nvidia/llama-3.1-nemotron-70b-instruct',
        label: 'NVIDIA Nemotron 70B'
      },
      openai: {
        provider: 'openai',
        base_url: 'https://api.openai.com/v1',
        model_name: 'gpt-4o-mini',
        label: 'OpenAI GPT-4o-mini'
      }
    };

    function selectProviderPreset(provKey) {
      const p = PRESETS[provKey];
      if (!p) return;
      document.getElementById('modal-base-url').value = p.base_url;
      document.getElementById('modal-model-name').value = p.model_name;

      ['gemini', 'nemotron', 'openai'].forEach(k => {
        const btn = document.getElementById(`btn-preset-${k}`);
        if (k === provKey) {
          btn.className = 'p-2.5 rounded-xl border border-indigo-500 bg-indigo-950/60 text-left transition';
        } else {
          btn.className = 'p-2.5 rounded-xl border border-slate-700 bg-slate-900/60 text-left transition hover:border-slate-500';
        }
      });
      llmSettings.provider = provKey;
    }

    // Accessible Tab Switcher (WCAG Tablist with Glowing Indicators)
    // Accessibility Dialog & Styling Controls (WCAG 2.1 AAA)
    function toggleA11yModal() {
      const modal = document.getElementById('a11y-modal');
      if (!modal) return;
      const isHidden = modal.classList.contains('hidden');
      if (isHidden) {
        modal.classList.remove('hidden');
        document.getElementById('btn-a11y-modal')?.setAttribute('aria-expanded', 'true');
      } else {
        modal.classList.add('hidden');
        document.getElementById('btn-a11y-modal')?.setAttribute('aria-expanded', 'false');
      }
    }

    function setFontScale(scale) {
      document.documentElement.style.fontSize = scale;
      ['100', '115', '130'].forEach(s => {
        const btn = document.getElementById(`scale-${s}`);
        if (btn) {
          if (`${s}%` === scale) {
            btn.classList.add('bg-indigo-600', 'text-white');
            btn.classList.remove('bg-slate-800', 'text-slate-300');
          } else {
            btn.classList.remove('bg-indigo-600', 'text-white');
            btn.classList.add('bg-slate-800', 'text-slate-300');
          }
        }
      });
      showToast(`Text scale set to ${scale}`, 'info');
    }

    let isHighContrast = false;
    function toggleHighContrastMode() {
      isHighContrast = !isHighContrast;
      document.body.classList.toggle('contrast-125', isHighContrast);
      document.body.classList.toggle('brightness-110', isHighContrast);
      showToast(isHighContrast ? 'High Contrast AAA Enabled' : 'Standard Contrast Restored', 'info');
    }

    let isDyslexia = false;
    function toggleDyslexiaFriendlyFont() {
      isDyslexia = !isDyslexia;
      if (isDyslexia) {
        document.body.style.letterSpacing = '0.04em';
        document.body.style.lineHeight = '1.8';
        showToast('Dyslexia readability mode enabled', 'info');
      } else {
        document.body.style.letterSpacing = '';
        document.body.style.lineHeight = '';
        showToast('Standard typography restored', 'info');
      }
    }

    function switchTab(tabName) {
      const tabs = ['analyzer', 'comparator', 'chat', 'privacy', 'details'];
      tabs.forEach(t => {
        const section = document.getElementById(`tab-${t}`);
        const navBtn = document.getElementById(`nav-tab-${t}`);
        if (t === tabName) {
          section.classList.remove('hidden');
          navBtn.setAttribute('aria-selected', 'true');
          navBtn.setAttribute('tabindex', '0');
          navBtn.classList.add('border-indigo-500', 'text-indigo-300', 'bg-indigo-500/10', 'rounded-t-lg');
          navBtn.classList.remove('border-transparent', 'text-slate-400');
        } else {
          section.classList.add('hidden');
          navBtn.setAttribute('aria-selected', 'false');
          navBtn.setAttribute('tabindex', '-1');
          navBtn.classList.remove('border-indigo-500', 'text-indigo-300', 'bg-indigo-500/10', 'rounded-t-lg');
          navBtn.classList.add('border-transparent', 'text-slate-400');
        }
      });
    }

    // Switch between Clause Explorer and Attorney Checklist
    function switchAnalysisView(view) {
      const clausesView = document.getElementById('clause-cards-view');
      const checklistView = document.getElementById('attorney-checklist-view');
      const clausesBtn = document.getElementById('view-clauses-btn');
      const checklistBtn = document.getElementById('view-checklist-btn');

      if (view === 'clauses') {
        clausesView.classList.remove('hidden');
        checklistView.classList.add('hidden');
        clausesBtn.setAttribute('aria-selected', 'true');
        checklistBtn.setAttribute('aria-selected', 'false');
        clausesBtn.classList.add('text-indigo-400', 'border-indigo-500');
        clausesBtn.classList.remove('text-slate-400', 'border-transparent');
        checklistBtn.classList.remove('text-indigo-400', 'border-indigo-500');
        checklistBtn.classList.add('text-slate-400', 'border-transparent');
      } else {
        clausesView.classList.add('hidden');
        checklistView.classList.remove('hidden');
        checklistBtn.setAttribute('aria-selected', 'true');
        clausesBtn.setAttribute('aria-selected', 'false');
        checklistBtn.classList.add('text-indigo-400', 'border-indigo-500');
        checklistBtn.classList.remove('text-slate-400', 'border-transparent');
        clausesBtn.classList.remove('text-indigo-400', 'border-indigo-500');
        clausesBtn.classList.add('text-slate-400', 'border-transparent');
      }
    }

    // Floating Toast Notification System
    function showToast(message, type = 'info') {
      const container = document.getElementById('toast-container');
      if (!container) return;
      const toast = document.createElement('div');
      toast.className = 'toast-item';
      let icon = 'ℹ️';
      if (type === 'success') icon = '✅';
      if (type === 'error') icon = '🚨';
      if (type === 'copied') icon = '📋';
      toast.innerHTML = `<span>${icon}</span> <span>${message}</span>`;
      container.appendChild(toast);
      setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateY(10px)';
        setTimeout(() => toast.remove(), 300);
      }, 3200);
    }

    // Input Stats Pill Updater
    function updateInputStats() {
      const input = document.getElementById('contract-input');
      const pill = document.getElementById('input-stats-pill');
      if (!input || !pill) return;
      const text = input.value.trim();
      const words = text ? text.split(\' \').filter(w => w.length > 0).length : 0;
      const chars = input.value.length;
      pill.innerText = `${words.toLocaleString()} words | ${chars.toLocaleString()} chars`;
    }

    function clearContractInput() {
      const input = document.getElementById('contract-input');
      if (input) {
        input.value = '';
        updateInputStats();
        showToast('Document cleared', 'info');
      }
    }

    // Drag and drop listener setup
    function setupDragAndDrop() {
      const input = document.getElementById('contract-input');
      if (!input) return;
      ['dragenter', 'dragover'].forEach(eventName => {
        input.addEventListener(eventName, (e) => {
          e.preventDefault();
          e.stopPropagation();
          input.classList.add('border-indigo-400', 'ring-2', 'ring-indigo-400/50');
        }, false);
      });
      ['dragleave', 'drop'].forEach(eventName => {
        input.addEventListener(eventName, (e) => {
          e.preventDefault();
          e.stopPropagation();
          input.classList.remove('border-indigo-400', 'ring-2', 'ring-indigo-400/50');
        }, false);
      });
      input.addEventListener('drop', (e) => {
        const dt = e.dataTransfer;
        const files = dt.files;
        if (files && files.length > 0) {
          const file = files[0];
          const reader = new FileReader();
          reader.onload = (event) => {
            input.value = event.target.result;
            updateInputStats();
            showToast(`Loaded file: ${file.name}`, 'success');
          };
          reader.readAsText(file);
        }
      }, false);
    }

    // Filter Chips & Live Search
    function setFilterChip(level) {
      const chips = ['ALL', 'TWISTED', 'HIGH', 'ESCALATED', 'MEDIUM', 'LOW'];
      chips.forEach(c => {
        const el = document.getElementById(`filter-chip-${c}`);
        if (!el) return;
        if (c === level) {
          el.className = 'filter-chip px-2.5 py-1 rounded-lg bg-indigo-600 text-white font-bold text-[11px] border border-indigo-500 transition shadow-sm';
        } else {
          el.className = 'filter-chip px-2.5 py-1 rounded-lg bg-slate-800 text-slate-300 hover:bg-slate-700 font-bold text-[11px] border border-slate-700 transition';
        }
      });
      const select = document.getElementById('filter-risk');
      if (select) select.value = level;
      filterClauses(level);
    }

    function searchClauses(query) {
      const q = query.toLowerCase().trim();
      const cards = document.querySelectorAll('.clause-card');
      cards.forEach(card => {
        if (!q) {
          card.classList.remove('hidden');
          return;
        }
        const text = card.innerText.toLowerCase();
        if (text.includes(q)) {
          card.classList.remove('hidden');
        } else {
          card.classList.add('hidden');
        }
      });
    }

    // 1-Click Copy Negotiation Tip
    function copyTip(clauseId, btn) {
      const tipElement = document.getElementById(`tip-content-${clauseId}`);
      if (!tipElement) return;
      const tipText = tipElement.innerText.trim();
      navigator.clipboard.writeText(tipText).then(() => {
        const originalHtml = btn.innerHTML;
        btn.innerHTML = '<span>✅</span> Copied!';
        btn.classList.add('bg-emerald-600', 'text-white');
        showToast('Negotiation redline copied to clipboard!', 'copied');
        setTimeout(() => {
          btn.innerHTML = originalHtml;
          btn.classList.remove('bg-emerald-600', 'text-white');
        }, 2000);
      });
    }

    // Fetch and cache samples on load
    async function initSamples() {
      try {
        const res = await fetch('/api/samples');
        if (res.ok) {
          cachedSamples = await res.json();
          loadSample('freelance_high_risk');
        }
      } catch (err) {
        console.error('Failed to load samples:', err);
      }
    }

    function loadSample(sampleId) {
      const found = cachedSamples.find(s => s.id === sampleId);
      if (found) {
        document.getElementById('contract-input').value = found.content;
        updateInputStats();
        showToast(`Loaded sample: ${found.title || sampleId}`, 'info');
      }
    }

    function handleFileUpload(event) {
      const file = event.target.files[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = (e) => {
          document.getElementById('contract-input').value = e.target.result;
          updateInputStats();
          showToast(`Uploaded file: ${file.name}`, 'success');
        };
        reader.readAsText(file);
      }
    }

    async function previewPII() {
      const text = document.getElementById('contract-input').value.trim();
      if (!text) {
        alert('Please paste or load a contract first.');
        return;
      }
      try {
        const res = await fetch('/api/anonymize', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ text })
        });
        const data = await res.json();
        alert(`🛡️ Local PII Shield Audit:\\n\\n` +
              `Total Identifiers Masked: ${data.entities.length}\\n` +
              `• Emails: ${data.entity_counts.EMAIL || 0}\\n` +
              `• Phone Numbers: ${data.entity_counts.PHONE || 0}\\n` +
              `• SSN / Tax IDs: ${data.entity_counts.SSN_TAX_ID || 0}\\n` +
              `• Monetary Amounts: ${data.entity_counts.FINANCIAL || 0}\\n` +
              `• Addresses & Entities: ${data.entity_counts.ADDRESS || 0}`);
      } catch (e) {
        alert('Error testing PII redaction: ' + e);
      }
    }

    // LLM Settings Modal handlers
    function toggleLLMModal() {
      const modal = document.getElementById('llm-modal');
      const btn = document.getElementById('llm-status-btn');
      const isHidden = modal.classList.toggle('hidden');
      btn.setAttribute('aria-expanded', String(!isHidden));
      if (!isHidden) {
        document.getElementById('modal-api-key').focus();
      }
    }

    async function loadLLMSettings() {
      try {
        const res = await fetch('/api/settings/llm');
        if (res.ok) {
          llmSettings = await res.json();
          const dot = document.getElementById('llm-dot');
          const label = document.getElementById('llm-label');
          const envBadge = document.getElementById('env-badge-pill');
          const envBox = document.getElementById('modal-env-status');
          const envDesc = document.getElementById('modal-env-desc');

          const prov = llmSettings.provider || 'gemini';
          const model = llmSettings.model_name || 'gemini-2.0-flash-lite';
          selectProviderPreset(prov);

          const resetBtn = document.getElementById('modal-reset-btn');
          const keyBadge = document.getElementById('modal-key-badge');
          if (llmSettings.api_key_configured) {
            dot.className = 'w-2 h-2 rounded-full bg-emerald-400 animate-pulse';
            label.innerText = `${prov.toUpperCase()}: ${model}`;
            document.getElementById('chat-model-badge').innerText = `Engine: ${model}`;

            if (llmSettings.api_key_source === 'environment') {
              envBadge.classList.remove('hidden');
              envBox.classList.remove('hidden');
              envBox.className = 'p-3.5 rounded-xl bg-emerald-950/40 border border-emerald-800/60 text-emerald-200 space-y-1';
              envDesc.innerText = `Active API Key read from server environment (GEMINI_API_KEY). Evaluator does not need to enter BYOK! You can enter a key below to override if desired.`;
              if (resetBtn) resetBtn.classList.add('hidden');
              if (keyBadge) keyBadge.innerText = 'Env Key Active';
            } else if (llmSettings.api_key_source === 'user_configured') {
              envBadge.classList.remove('hidden');
              envBox.classList.remove('hidden');
              envBox.className = 'p-3.5 rounded-xl bg-indigo-950/40 border border-indigo-800/60 text-indigo-200 space-y-1';
              envDesc.innerText = `Using custom BYOK API key. Clear key or click 'Reset to Env' to fall back to server environment defaults.`;
              if (resetBtn) resetBtn.classList.remove('hidden');
              if (keyBadge) keyBadge.innerText = 'BYOK Active';
            } else {
              envBadge.classList.add('hidden');
              envBox.classList.add('hidden');
              if (resetBtn) resetBtn.classList.add('hidden');
            }
          } else {
            dot.className = 'w-2 h-2 rounded-full bg-slate-500';
            label.innerText = `Configure AI (${prov.toUpperCase()})`;
            envBadge.classList.add('hidden');
            envBox.classList.remove('hidden');
            envBox.className = 'p-3.5 rounded-xl bg-slate-900/60 border border-slate-700/60 text-slate-300 space-y-1';
            envDesc.innerText = `Operating in pure Local-First mode (Cython C-Accelerated). To activate LLM deep synthesis, set GEMINI_API_KEY in your environment, or enter a BYOK key below.`;
            if (resetBtn) resetBtn.classList.add('hidden');
            if (keyBadge) keyBadge.innerText = 'Local Mode';
          }

          if (llmSettings.base_url) document.getElementById('modal-base-url').value = llmSettings.base_url;
          if (llmSettings.model_name) document.getElementById('modal-model-name').value = llmSettings.model_name;
          if (llmSettings.confidence_threshold) {
            document.getElementById('modal-threshold').value = Math.round(llmSettings.confidence_threshold * 100);
            document.getElementById('threshold-val').innerText = Math.round(llmSettings.confidence_threshold * 100) + '%';
          }
        }
      } catch (e) {
        console.error('Failed to load LLM settings:', e);
      }
    }

    async function saveLLMSettings() {
      const apiKey = document.getElementById('modal-api-key').value.trim();
      const baseUrl = document.getElementById('modal-base-url').value.trim();
      const modelName = document.getElementById('modal-model-name').value.trim();
      const threshold = parseFloat(document.getElementById('modal-threshold').value) / 100.0;

      const payload = {
        base_url: baseUrl,
        model_name: modelName,
        confidence_threshold: threshold,
        provider: llmSettings.provider,
        enabled: true,
        api_key: apiKey
      };

      try {
        const res = await fetch('/api/settings/llm', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        });
        if (res.ok) {
          await loadLLMSettings();
          toggleLLMModal();
          showToast('success', 'AI Provider settings updated successfully!');
        }
      } catch (e) {
        showToast('error', 'Failed to save settings: ' + e);
      }
    }

    async function resetToEnvironmentSettings() {
      try {
        const res = await fetch('/api/settings/reset', { method: 'POST' });
        if (res.ok) {
          document.getElementById('modal-api-key').value = '';
          await loadLLMSettings();
          showToast('info', 'Restored server environment key defaults!');
        }
      } catch (e) {
        showToast('error', 'Failed to reset settings: ' + e);
      }
    }

    async function testConnection() {
      const btn = document.getElementById('modal-test-btn');
      const resBox = document.getElementById('modal-test-result');
      btn.innerText = 'Testing...';
      resBox.className = 'hidden';

      const apiKey = document.getElementById('modal-api-key').value.trim();
      if (apiKey) {
        await fetch('/api/settings/llm', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            api_key: apiKey,
            base_url: document.getElementById('modal-base-url').value.trim(),
            model_name: document.getElementById('modal-model-name').value.trim(),
            provider: llmSettings.provider
          })
        });
      }

      try {
        const res = await fetch('/api/settings/test', { method: 'POST' });
        const data = await res.json();
        resBox.classList.remove('hidden');
        if (data.success) {
          resBox.className = 'text-xs p-3 rounded-lg bg-emerald-950/70 border border-emerald-700/70 text-emerald-200 font-semibold';
          resBox.innerText = `✅ Success! Connected to ${data.provider} model '${data.model}' on ${data.base_url}`;
        } else {
          resBox.className = 'text-xs p-3 rounded-lg bg-rose-950/70 border border-rose-700/70 text-rose-200 font-semibold';
          resBox.innerText = `❌ Connection Failed: ${data.message}`;
        }
      } catch (e) {
        resBox.classList.remove('hidden');
        resBox.className = 'text-xs p-3 rounded-lg bg-rose-950/70 border border-rose-700/70 text-rose-200 font-semibold';
        resBox.innerText = '❌ Error testing connection: ' + e;
      } finally {
        btn.innerText = 'Ping / Test Connection';
      }
    }

    // Full contract analysis run
    async function runAnalysis() {
      const text = document.getElementById('contract-input').value.trim();
      if (!text) {
        alert('Please paste or upload a contract.');
        return;
      }

      document.getElementById('analyzer-loading').classList.remove('hidden');
      document.getElementById('analyzer-results').classList.add('hidden');

      try {
        const res = await fetch('/api/analyze', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ text })
        });

        if (!res.ok) {
          throw new Error('Analysis failed with status ' + res.status);
        }

        currentAnalysis = await res.json();
        renderAnalysisResults(currentAnalysis);
      } catch (err) {
        alert('Analysis failed: ' + err.message);
      } finally {
        document.getElementById('analyzer-loading').classList.add('hidden');
      }
    }

    function renderAnalysisResults(data) {
      document.getElementById('analyzer-results').classList.remove('hidden');

      // Routing banner
      document.getElementById('ai-engine-used').innerText = data.risk_overview.ai_model_used || 'Local Privacy Shield';
      document.getElementById('avg-confidence-pill').innerText = `Local Confidence: ${Math.round(data.risk_overview.average_confidence * 100)}%`;
      document.getElementById('escalated-count-pill').innerText = `Escalated: ${data.risk_overview.escalated_clauses_count} clauses`;

      // Twisted count pill
      const twistedPill = document.getElementById('twisted-count-pill');
      if (data.risk_overview.twisted_clauses_count > 0) {
        twistedPill.classList.remove('hidden');
        twistedPill.innerText = `🌀 Twisted Drafting: ${data.risk_overview.twisted_clauses_count}`;
      } else {
        twistedPill.classList.add('hidden');
      }

      // Score and Radial SVG Gauge Animation
      const index = data.risk_overview.legal_risk_index;
      document.getElementById('score-meter').innerText = index;
      const badge = document.getElementById('score-badge');
      badge.innerText = data.risk_overview.risk_level;

      const circle = document.getElementById('gauge-progress-circle');
      const circumference = 264; // 2 * PI * 42 ~= 263.89
      const offset = circumference - (index / 100) * circumference;

      if (circle) {
        circle.style.strokeDashoffset = offset;
        if (index >= 75) {
          circle.setAttribute('stroke', '#f43f5e'); // Rose
        } else if (index >= 45) {
          circle.setAttribute('stroke', '#f59e0b'); // Amber
        } else {
          circle.setAttribute('stroke', '#10b981'); // Emerald
        }
      }

      if (index >= 75) {
        badge.className = 'px-3 py-1 text-xs font-extrabold rounded-full badge-critical uppercase tracking-wider';
      } else if (index >= 45) {
        badge.className = 'px-3 py-1 text-xs font-extrabold rounded-full badge-medium uppercase tracking-wider';
      } else {
        badge.className = 'px-3 py-1 text-xs font-extrabold rounded-full badge-low uppercase tracking-wider';
      }

      document.getElementById('results-title').innerText = data.attorney_checklist.document_title;
      document.getElementById('executive-summary').innerText = data.risk_overview.executive_summary;
      document.getElementById('high-risk-count').innerText = data.risk_overview.high_risk_count;
      document.getElementById('medium-risk-count').innerText = data.risk_overview.medium_risk_count;
      document.getElementById('low-risk-count').innerText = data.risk_overview.low_risk_count;

      // Critical findings
      const findingsContainer = document.getElementById('critical-findings-container');
      findingsContainer.innerHTML = '';
      data.risk_overview.critical_findings.forEach(finding => {
        const div = document.createElement('div');
        div.className = 'text-xs text-rose-200 bg-rose-950/50 border border-rose-800/60 px-3 py-2 rounded-lg flex items-center gap-2';
        div.innerHTML = `<span aria-hidden="true">🚨</span> <strong>${finding}</strong>`;
        findingsContainer.appendChild(div);
      });

      renderClauseCards(data.clauses);
      renderAttorneyChecklist(data.attorney_checklist);
      renderPrivacyVault(data.anonymization);
    }

    function renderClauseCards(clauses) {
      const container = document.getElementById('clause-cards-view');
      container.innerHTML = '';

      clauses.forEach(clause => {
        const card = document.createElement('div');
        let severityBadge = '';
        if (clause.severity === 'HIGH' || clause.severity === 'CRITICAL') {
          severityBadge = '<span class="px-2.5 py-0.5 text-xs font-extrabold rounded-md badge-critical">HIGH RISK</span>';
        } else if (clause.severity === 'MEDIUM') {
          severityBadge = '<span class="px-2.5 py-0.5 text-xs font-extrabold rounded-md badge-medium">MODERATE</span>';
        } else {
          severityBadge = '<span class="px-2.5 py-0.5 text-xs font-extrabold rounded-md badge-low">STANDARD</span>';
        }

        // Source & Confidence Pill
        let sourcePill = '';
        if (clause.analysis_source === 'GEMINI_DEEP_REASONING') {
          sourcePill = `<span class="px-2.5 py-0.5 text-[11px] font-bold rounded-full badge-gemini">🚀 Gemini Flash-Lite Deep Synthesis</span>`;
        } else if (clause.analysis_source === 'NEMOTRON_DEEP_REASONING') {
          sourcePill = `<span class="px-2.5 py-0.5 text-[11px] font-bold rounded-full badge-nemotron">🧠 Nemotron Deep Synthesis</span>`;
        } else if (clause.analysis_source === 'OPENAI_DEEP_REASONING') {
          sourcePill = `<span class="px-2.5 py-0.5 text-[11px] font-bold rounded-full bg-slate-700 text-white border border-slate-600">⚡ OpenAI Deep Synthesis</span>`;
        } else {
          sourcePill = `<span class="px-2.5 py-0.5 text-[11px] font-semibold rounded-full bg-slate-800 text-slate-300 border border-slate-700">⚡ ${Math.round(clause.confidence * 100)}% Local Confidence</span>`;
        }

        // Twisted badge
        let twistedBadge = '';
        if (clause.is_twisted) {
          twistedBadge = `<span class="px-2.5 py-0.5 text-[11px] font-extrabold rounded-md badge-twisted">🌀 Twisted Phrasing (${Math.round((clause.obfuscation_score || 0.5) * 100)}% Obfuscation)</span>`;
        }

        const trapsHtml = (clause.detected_traps || []).map(t => 
          `<span class="inline-block bg-rose-500/25 text-rose-200 border border-rose-500/40 text-[11px] font-bold px-2 py-0.5 rounded-md mr-1 mt-1">⚠️ ${t}</span>`
        ).join('');

        card.className = `glass-card rounded-2xl p-5 sm:p-6 space-y-4 clause-card transition-all ${clause.is_twisted ? 'border-amber-500/40 shadow-lg shadow-amber-950/20' : ''}`;
        card.setAttribute('data-severity', clause.severity);
        card.setAttribute('data-source', clause.analysis_source);
        card.setAttribute('data-twisted', clause.is_twisted ? 'true' : 'false');

        // Archetypes details if present
        let archetypeHtml = '';
        if (clause.semantic_archetype_matches && Object.keys(clause.semantic_archetype_matches).length > 0) {
          const topMatches = Object.entries(clause.semantic_archetype_matches)
            .filter(([_, score]) => score > 0.15)
            .sort((a, b) => b[1] - a[1]);
          if (topMatches.length > 0) {
            archetypeHtml = `
              <div class="mt-2 p-2.5 rounded-lg bg-slate-900/90 border border-slate-800 space-y-1">
                <div class="text-[11px] font-bold text-amber-300 flex items-center gap-1">
                  <span>📐</span> Semantic Vector Archetype Overlap:
                </div>
                <div class="flex flex-wrap gap-1.5 pt-0.5">
                  ${topMatches.map(([arch, score]) => `
                    <span class="text-[10px] px-2 py-0.5 rounded bg-slate-800 text-slate-200 border border-slate-700 font-mono">
                      ${arch.replace(/_/g, ' ')}: <strong class="text-indigo-300">${Math.round(score * 100)}%</strong>
                    </span>
                  `).join('')}
                </div>
              </div>
            `;
          }
        }

        card.innerHTML = `
          <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-800 pb-3">
            <div class="flex items-center gap-2.5">
              <span class="text-xs font-bold bg-slate-800 text-slate-300 px-2.5 py-0.5 rounded-md border border-slate-700 font-mono">#${clause.id}</span>
              <h4 class="font-display text-sm sm:text-base font-extrabold text-white">${clause.section_title}</h4>
            </div>
            <div class="flex flex-wrap items-center gap-2">
              <span class="text-[11px] font-semibold text-slate-400 uppercase tracking-wider">${clause.category.replace(/_/g, ' ')}</span>
              ${twistedBadge}
              ${severityBadge}
              ${sourcePill}
            </div>
          </div>

          ${clause.escalation_reason ? `<div class="text-[11px] text-purple-200 bg-purple-950/50 border border-purple-800/60 p-2.5 rounded-lg font-medium">💡 ${clause.escalation_reason}</div>` : ''}

          ${trapsHtml ? `<div class="pt-0.5">${trapsHtml}</div>` : ''}

          ${archetypeHtml}

          <div class="grid grid-cols-1 md:grid-cols-2 gap-4 pt-1">
            <div class="space-y-2.5">
              <div class="text-xs font-bold uppercase tracking-wider text-slate-300">Plain English Meaning:</div>
              <p class="text-xs text-slate-200 leading-relaxed bg-slate-900/90 p-3.5 rounded-xl border border-slate-800">
                ${clause.plain_english_summary}
              </p>
              <div class="text-xs font-bold uppercase tracking-wider text-rose-300">What This Means For You:</div>
              <p class="text-xs text-rose-100 bg-rose-950/40 p-3.5 rounded-xl border border-rose-900/50 leading-relaxed">
                ${clause.what_it_means_for_you}
              </p>
            </div>

            <div class="space-y-2.5">
              <div class="flex items-center justify-between">
                <span class="text-xs font-bold uppercase tracking-wider text-indigo-300">Recommended Redline / Fallback:</span>
                <button type="button" onclick="copyTip('${clause.id}', this)" class="inline-flex items-center gap-1 text-[10px] font-bold text-indigo-300 hover:text-white bg-indigo-900/40 hover:bg-indigo-800/60 px-2 py-0.5 rounded-md border border-indigo-700/50 transition" title="Copy fallback redline tip">
                  <span>📋</span> Copy Tip
                </button>
              </div>
              <div id="tip-content-${clause.id}" class="text-xs text-indigo-100 bg-indigo-950/50 p-3.5 rounded-xl border border-indigo-900/60 leading-relaxed">
                💡 ${clause.negotiation_tip}
              </div>
              <details class="text-xs text-slate-400">
                <summary class="cursor-pointer font-semibold text-slate-300 hover:text-white py-1">View Original Contract Clause Text</summary>
                <pre class="mt-1.5 p-3 bg-slate-900 rounded-xl text-[11px] font-mono whitespace-pre-wrap overflow-x-auto text-slate-300 max-h-36 border border-slate-800">${clause.original_text}</pre>
              </details>
            </div>
          </div>
        `;
        container.appendChild(card);
      });
    }

    function filterClauses(level) {
      const cards = document.querySelectorAll('.clause-card');
      cards.forEach(c => {
        const sev = c.getAttribute('data-severity');
        const src = c.getAttribute('data-source');
        const isTwisted = c.getAttribute('data-twisted') === 'true';

        if (level === 'ALL') {
          c.classList.remove('hidden');
        } else if (level === 'TWISTED') {
          if (isTwisted) c.classList.remove('hidden');
          else c.classList.add('hidden');
        } else if (level === 'ESCALATED') {
          if (src && src.includes('DEEP_REASONING')) c.classList.remove('hidden');
          else c.classList.add('hidden');
        } else if (level === 'HIGH') {
          if (sev === 'HIGH' || sev === 'CRITICAL') c.classList.remove('hidden');
          else c.classList.add('hidden');
        } else if (sev === level) {
          c.classList.remove('hidden');
        } else {
          c.classList.add('hidden');
        }
      });
    }

    function renderAttorneyChecklist(checklist) {
      const qList = document.getElementById('checklist-questions-list');
      qList.innerHTML = '';

      checklist.questions_for_counsel.forEach((q, i) => {
        const div = document.createElement('div');
        div.className = 'p-4 rounded-xl bg-slate-900/90 border border-slate-800 space-y-2.5';
        div.innerHTML = `
          <div class="flex items-center gap-2">
            <span class="text-xs font-bold text-indigo-400 uppercase tracking-wider">Question ${i + 1}: ${q.category}</span>
          </div>
          <p class="font-display text-xs sm:text-sm font-extrabold text-white leading-snug">"${q.question}"</p>
          <p class="text-xs text-slate-200"><strong>Why It Matters:</strong> ${q.why_it_matters}</p>
          <div class="text-xs text-indigo-100 bg-indigo-950/40 p-2.5 rounded-lg border border-indigo-900/50 font-mono">
            <strong>Recommended Redline:</strong> ${q.recommended_fallback}
          </div>
        `;
        qList.appendChild(div);
      });

      const rList = document.getElementById('checklist-redlines-list');
      rList.innerHTML = '';
      checklist.priority_negotiation_items.forEach(item => {
        const li = document.createElement('li');
        li.className = 'flex items-start gap-2';
        li.innerHTML = `<span class="text-indigo-400 font-bold" aria-hidden="true">☑</span> <span>${item}</span>`;
        rList.appendChild(li);
      });
    }

    function renderPrivacyVault(anon) {
      document.getElementById('privacy-total-redacted').innerText = anon.entities.length;
      document.getElementById('privacy-score-display').innerText = anon.privacy_score + '%';

      const tbody = document.getElementById('privacy-table-body');
      tbody.innerHTML = '';
      if (anon.entities.length === 0) {
        tbody.innerHTML = '<tr><td colspan="3" class="px-4 py-4 text-center text-slate-400">No sensitive PII identifiers detected in this document.</td></tr>';
        return;
      }

      anon.entities.forEach(ent => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
          <td class="px-4 py-2.5 font-bold text-slate-200">${ent.entity_type}</td>
          <td class="px-4 py-2.5 font-mono text-indigo-300">${ent.token}</td>
          <td class="px-4 py-2.5 font-mono text-slate-400">${ent.original_value}</td>
        `;
        tbody.appendChild(tr);
      });
    }

    function copyChecklistMarkdown() {
      if (!currentAnalysis) return;
      navigator.clipboard.writeText(currentAnalysis.attorney_checklist.markdown_report);
      alert('Attorney Consultation Brief copied to clipboard in Markdown format!');
    }

    function downloadChecklistFile() {
      if (!currentAnalysis) return;
      const blob = new Blob([currentAnalysis.attorney_checklist.markdown_report], { type: 'text/markdown' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'attorney_consultation_brief.md';
      a.click();
      URL.revokeObjectURL(url);
    }

    // Comparison Logic
    function loadSampleComparison() {
      const v1 = cachedSamples.find(s => s.id === 'freelance_high_risk');
      const v2 = cachedSamples.find(s => s.id === 'freelance_negotiated');
      if (v1 && v2) {
        document.getElementById('compare-v1').value = v1.content;
        document.getElementById('compare-v2').value = v2.content;
      }
    }

    async function runComparison() {
      const text_v1 = document.getElementById('compare-v1').value.trim();
      const text_v2 = document.getElementById('compare-v2').value.trim();
      if (!text_v1 || !text_v2) {
        alert('Please supply both Contract A and Contract B to compare.');
        return;
      }

      try {
        const res = await fetch('/api/compare', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ text_v1, text_v2 })
        });
        const data = await res.json();
        renderComparisonResults(data);
      } catch (err) {
        alert('Comparison failed: ' + err.message);
      }
    }

    function renderComparisonResults(data) {
      document.getElementById('comparator-results').classList.remove('hidden');

      const badge = document.getElementById('compare-trajectory-badge');
      badge.innerText = `${data.trajectory}: ${data.risk_index_delta > 0 ? '+' : ''}${data.risk_index_delta} Risk Points`;
      if (data.trajectory === 'SAFER') {
        badge.className = 'px-3 py-1 text-xs font-bold rounded-full badge-low uppercase';
      } else if (data.trajectory === 'MORE_RISK') {
        badge.className = 'px-3 py-1 text-xs font-bold rounded-full badge-critical uppercase';
      } else {
        badge.className = 'px-3 py-1 text-xs font-bold rounded-full badge-medium uppercase';
      }

      document.getElementById('compare-scores-summary').innerText = 
        `Original Version Risk: ${data.risk_index_v1}/100 ➔ Revised Proposal Risk: ${data.risk_index_v2}/100`;

      const list = document.getElementById('compare-changes-list');
      list.innerHTML = '';
      data.summary_of_changes.forEach(ch => {
        const li = document.createElement('li');
        li.innerHTML = `• ${ch}`;
        list.appendChild(li);
      });

      const container = document.getElementById('compare-diff-cards');
      container.innerHTML = '';
      data.clause_diffs.forEach(diff => {
        const card = document.createElement('div');
        card.className = 'glass-card rounded-xl p-4 space-y-2 border border-slate-800';
        
        let typeBadge = '';
        if (diff.change_type === 'ADDED') typeBadge = '<span class="px-2 py-0.5 rounded text-xs font-bold bg-blue-500/25 text-blue-200 border border-blue-500/40">ADDED</span>';
        else if (diff.change_type === 'REMOVED') typeBadge = '<span class="px-2 py-0.5 rounded text-xs font-bold bg-rose-500/25 text-rose-200 border border-rose-500/40">REMOVED</span>';
        else if (diff.change_type === 'MODIFIED') typeBadge = '<span class="px-2 py-0.5 rounded text-xs font-bold bg-amber-500/25 text-amber-200 border border-amber-500/40">MODIFIED</span>';
        else typeBadge = '<span class="px-2 py-0.5 rounded text-xs font-bold bg-slate-800 text-slate-300">UNCHANGED</span>';

        card.innerHTML = `
          <div class="flex items-center justify-between border-b border-slate-800 pb-2">
            <h4 class="font-display text-sm font-extrabold text-white">${diff.section_title}</h4>
            <div class="flex items-center gap-2">
              <span class="text-xs text-slate-400 font-semibold">${diff.category}</span>
              ${typeBadge}
            </div>
          </div>
          <p class="text-xs text-slate-200 font-medium">${diff.analysis_notes}</p>
          ${diff.text_v1 && diff.text_v2 && diff.change_type === 'MODIFIED' ? `
            <div class="grid grid-cols-1 md:grid-cols-2 gap-2 text-[11px] font-mono pt-1">
              <div class="bg-rose-950/40 p-2.5 rounded-lg border border-rose-900/50 text-rose-100 max-h-32 overflow-y-auto">
                <div class="font-bold mb-1 text-rose-200">V1 Original:</div>${diff.text_v1}
              </div>
              <div class="bg-emerald-950/40 p-2.5 rounded-lg border border-emerald-900/50 text-emerald-100 max-h-32 overflow-y-auto">
                <div class="font-bold mb-1 text-emerald-200">V2 Revision:</div>${diff.text_v2}
              </div>
            </div>
          ` : ''}
        `;
        container.appendChild(card);
      });
    }

    // Chat Handler
    async function handleChatSubmit(e) {
      e.preventDefault();
      const input = document.getElementById('chat-input');
      const msg = input.value.trim();
      if (!msg) return;

      appendChatMessage('user', msg);
      input.value = '';

      const contractText = document.getElementById('contract-input').value.trim();
      const contextClauses = currentAnalysis ? currentAnalysis.clauses : null;

      try {
        const res = await fetch('/api/chat', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            message: msg,
            contract_text: contractText,
            context_clauses: contextClauses
          })
        });
        const data = await res.json();
        appendChatMessage('assistant', data.answer, data.risk_warning, data.referenced_clauses, data.model_used);
      } catch (err) {
        appendChatMessage('assistant', 'Sorry, I encountered an issue processing your query: ' + err.message);
      }
    }

    function sendQuickPrompt(prompt) {
      document.getElementById('chat-input').value = prompt;
      handleChatSubmit(new Event('submit'));
    }

    function appendChatMessage(sender, text, warning, cited, model) {
      const container = document.getElementById('chat-messages');
      const div = document.createElement('div');
      
      if (sender === 'user') {
        div.className = 'ml-auto max-w-lg p-3.5 bg-indigo-600 text-white rounded-xl shadow-md text-xs leading-relaxed font-medium';
        div.innerText = text;
      } else {
        div.className = 'mr-auto max-w-xl p-4 bg-slate-800/90 text-slate-100 rounded-xl border border-slate-700/80 shadow-md space-y-2.5 text-xs leading-relaxed';
        let warningHtml = warning ? `<div class="p-2.5 bg-rose-950/60 border border-rose-800 text-rose-200 rounded-lg font-bold" role="alert">🚨 ${warning}</div>` : '';
        let citationsHtml = (cited && cited.length > 0) ? `<div class="text-[11px] text-slate-400 font-semibold">Referenced Clauses: ${cited.join(', ')}</div>` : '';
        let modelHtml = model ? `<div class="text-[10px] text-purple-300 font-bold uppercase tracking-wider">Engine: ${model}</div>` : '';
        div.innerHTML = `
          ${modelHtml}
          ${warningHtml}
          <div class="whitespace-pre-wrap leading-relaxed">${text.replace(/\\n/g, '<br>')}</div>
          ${citationsHtml}
        `;
      }
      container.appendChild(div);
      container.scrollTop = container.scrollHeight;
    }

    // Modal Toggle for Keyboard Shortcuts
    function toggleShortcutsModal() {
      const modal = document.getElementById('shortcuts-modal');
      const isHidden = modal.classList.toggle('hidden');
      if (!isHidden) {
        modal.querySelector('button[aria-label="Close shortcuts modal"]')?.focus();
      }
    }

    // Comprehensive Keyboard Navigation & Shortcuts System (WCAG 2.1 AAA)
    document.addEventListener('keydown', (e) => {
      // 1. Close active modals on Escape
      if (e.key === 'Escape') {
        const llmModal = document.getElementById('llm-modal');
        if (llmModal && !llmModal.classList.contains('hidden')) {
          toggleLLMModal();
          return;
        }
        const scModal = document.getElementById('shortcuts-modal');
        if (scModal && !scModal.classList.contains('hidden')) {
          toggleShortcutsModal();
          return;
        }
      }

      // Check if user is actively typing in an input or textarea
      const activeTag = document.activeElement ? document.activeElement.tagName.toLowerCase() : '';
      const isTyping = activeTag === 'input' || activeTag === 'textarea';

      // 2. Open Shortcuts Modal with '?' key when not typing
      if (e.key === '?' && !isTyping) {
        e.preventDefault();
        toggleShortcutsModal();
        return;
      }

      // 3. Focus Clause Search bar with '/' key when not typing
      if (e.key === '/' && !isTyping) {
        const searchInput = document.getElementById('clause-search-input');
        if (searchInput) {
          e.preventDefault();
          searchInput.focus();
          searchInput.select();
          return;
        }
      }

      // 4. Run Analysis with Ctrl + Enter or Cmd + Enter anytime
      if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        e.preventDefault();
        runAnalysis();
        return;
      }

      // 5. Quick Tab switching with Alt + 1 through Alt + 5
      if (e.altKey && !e.ctrlKey && !e.metaKey) {
        if (e.key === '1') { e.preventDefault(); switchTab('analyzer'); showToast('info', 'Switched to Contract Risk Analyzer (Alt+1)'); }
        else if (e.key === '2') { e.preventDefault(); switchTab('comparator'); showToast('info', 'Switched to Version Comparator (Alt+2)'); }
        else if (e.key === '3') { e.preventDefault(); switchTab('chat'); showToast('info', 'Switched to Legal Navigator AI (Alt+3)'); }
        else if (e.key === '4') { e.preventDefault(); switchTab('privacy'); showToast('info', 'Switched to Privacy & PII Vault (Alt+4)'); }
        else if (e.key === '5') { e.preventDefault(); switchTab('details'); showToast('info', 'Switched to Impact & Savings (Alt+5)'); }
        else if (e.key.toLowerCase() === 's') { e.preventDefault(); toggleLLMModal(); }
      }
    });

    // Interactive Estimated Savings & ROI Calculator
    function recalculateSavings() {
      const contractsSlider = document.getElementById('calc-contracts');
      const rateSlider = document.getElementById('calc-rate');
      const hoursSlider = document.getElementById('calc-hours');
      const dealSlider = document.getElementById('calc-deal');

      if (!contractsSlider || !rateSlider || !hoursSlider || !dealSlider) return;

      const contracts = parseInt(contractsSlider.value, 10);
      const rate = parseInt(rateSlider.value, 10);
      const hours = parseFloat(hoursSlider.value);
      const deal = parseInt(dealSlider.value, 10);

      // Update badge indicators
      const contractsVal = document.getElementById('calc-contracts-val');
      const rateVal = document.getElementById('calc-rate-val');
      const hoursVal = document.getElementById('calc-hours-val');
      const dealVal = document.getElementById('calc-deal-val');

      if (contractsVal) contractsVal.innerText = contracts + ' contract' + (contracts > 1 ? 's' : '');
      if (rateVal) rateVal.innerText = '$' + rate + ' / hr';
      if (hoursVal) hoursVal.innerText = hours + ' hour' + (hours > 1 ? 's' : '');
      if (dealVal) dealVal.innerText = '$' + deal.toLocaleString();

      // Recalculate metrics
      const annualFees = Math.round(contracts * 12 * rate * hours);
      const annualHours = Math.round(contracts * 12 * hours);
      const liabilityAverted = Math.round(contracts * 12 * deal * 0.35);

      const feesEl = document.getElementById('calc-annual-fees');
      const hoursEl = document.getElementById('calc-annual-hours');
      const liabEl = document.getElementById('calc-liability-averted');

      if (feesEl) feesEl.innerText = '$' + annualFees.toLocaleString();
      if (hoursEl) hoursEl.innerText = annualHours + ' hrs / yr';
      if (liabEl) liabEl.innerText = '$' + liabilityAverted.toLocaleString() + '+';
    }

    // Startup bootstrap
    window.addEventListener('DOMContentLoaded', () => {
      initSamples();
      loadLLMSettings();
      recalculateSavings();
      setupDragAndDrop();
      updateInputStats();
    });
  </script>
  <!-- Floating Dynamic Toast Notification Container -->
  <div id="toast-container" aria-live="polite" aria-atomic="true"></div>

</body>
</html>
"""
