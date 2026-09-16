"""
Web UI dashboard template and component builder for Legal-Ease.
Sleek, modern, extremely accessible (WCAG 2.1 AAA/AA compliant),
with Cython hardware acceleration indicators, Nemotron LLM escalation management,
and structured multi-mode contract risk intelligence.
"""

def get_dashboard_html() -> str:
    """Return the complete, self-contained, accessible dashboard HTML."""
    return """<!DOCTYPE html>
<html lang="en" class="h-full bg-slate-950 text-slate-100 antialiased selection:bg-indigo-500 selection:text-white">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="Legal-Ease: Privacy-First AI Legal Navigator & Contract Risk Analyzer powered by local heuristics, Cython C-acceleration, and NVIDIA Nemotron.">
  <title>Legal-Ease | Privacy-First Legal AI Navigator</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {
      darkMode: 'class',
      theme: {
        extend: {
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
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');
    
    body {
      font-family: 'Plus Jakarta Sans', system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }
    code, pre, .font-mono {
      font-family: 'JetBrains Mono', ui-monospace, SFMono-Regular, monospace;
    }

    /* Glassmorphic panels with accessible contrast */
    .glass-panel {
      background: rgba(15, 23, 42, 0.82);
      backdrop-filter: blur(16px);
      -webkit-backdrop-filter: blur(16px);
      border: 1px solid rgba(255, 255, 255, 0.09);
    }
    .glass-card {
      background: rgba(30, 41, 59, 0.65);
      backdrop-filter: blur(12px);
      border: 1px solid rgba(255, 255, 255, 0.08);
    }

    /* WCAG AAA High Contrast Badges (Color + Text + Border) */
    .badge-critical {
      background: rgba(225, 29, 72, 0.2);
      color: #ffe4e6;
      border: 1px solid #f43f5e;
    }
    .badge-high {
      background: rgba(239, 68, 68, 0.2);
      color: #fef2f2;
      border: 1px solid #ef4444;
    }
    .badge-medium {
      background: rgba(245, 158, 11, 0.2);
      color: #fef3c7;
      border: 1px solid #f59e0b;
    }
    .badge-low {
      background: rgba(16, 185, 129, 0.2);
      color: #ecfdf5;
      border: 1px solid #10b981;
    }
    .badge-nemotron {
      background: rgba(139, 92, 246, 0.25);
      color: #f5f3ff;
      border: 1px solid #a855f7;
    }
    .badge-cython {
      background: rgba(6, 182, 212, 0.2);
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
    <div class="absolute -top-40 left-1/4 w-96 h-96 bg-indigo-600/15 rounded-full blur-3xl"></div>
    <div class="absolute top-1/3 -right-20 w-96 h-96 bg-purple-600/15 rounded-full blur-3xl"></div>
    <div class="absolute -bottom-40 left-1/3 w-96 h-96 bg-cyan-600/10 rounded-full blur-3xl"></div>
  </div>

  <!-- Mandatory Legal Disclaimer Banner -->
  <aside role="note" aria-label="Legal Non-Advisory Notice" class="relative z-20 bg-slate-900/95 border-b border-slate-800 text-slate-300 text-xs py-2 px-4 text-center font-medium backdrop-blur">
    ⚖️ <strong>Non-Advisory Tool:</strong> Legal-Ease provides educational contract literacy and negotiation issue-spotting. It does not provide legal advice or substitute for a licensed attorney.
  </aside>

  <!-- Header -->
  <header role="banner" class="relative z-20 glass-panel border-b border-slate-800/80 sticky top-0 shadow-lg">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex items-center justify-between h-16">
      
      <!-- Brand & Telemetry Badges -->
      <div class="flex items-center space-x-3.5">
        <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-indigo-500 via-indigo-600 to-purple-600 flex items-center justify-center text-white shadow-lg shadow-indigo-500/25 ring-1 ring-white/20 text-lg font-bold" aria-hidden="true">
          ⚖️
        </div>
        <div>
          <div class="flex items-center gap-2">
            <span class="text-lg font-extrabold tracking-tight text-white">
              Legal-Ease
            </span>
            <!-- Acceleration Badge -->
            <span id="header-cython-badge" class="hidden sm:inline-flex items-center gap-1 text-[10px] uppercase font-bold tracking-wider px-2 py-0.5 rounded-full badge-cython">
              ⚡ Cython Binary Active
            </span>
          </div>
          <p class="text-[11px] text-slate-400">Local-First AI Contract Navigator & Risk Engine</p>
        </div>
      </div>

      <!-- Controls & Engine Status -->
      <div class="flex items-center space-x-3">
        
        <!-- PII Status Pill -->
        <span class="hidden md:inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-emerald-500/15 text-emerald-300 border border-emerald-500/30">
          <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" aria-hidden="true"></span>
          100% Local PII Shield
        </span>

        <!-- AI / Nemotron Model Settings Button -->
        <button onclick="toggleLLMModal()" id="llm-status-btn" aria-haspopup="dialog" aria-expanded="false" class="inline-flex items-center gap-2 px-3 py-1.5 rounded-lg text-xs font-bold bg-slate-800/90 hover:bg-slate-750 text-slate-200 border border-slate-700 shadow-sm transition">
          <span id="nemotron-dot" class="w-2 h-2 rounded-full bg-slate-500" aria-hidden="true"></span>
          <span id="nemotron-label">Nemotron / OpenAI AI</span>
          <svg class="w-3.5 h-3.5 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/></svg>
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
    </nav>
  </header>

  <!-- ==================== ACCESSIBLE NEMOTRON SETTINGS MODAL ==================== -->
  <div id="llm-modal" role="dialog" aria-modal="true" aria-labelledby="modal-title" class="hidden fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/75 backdrop-blur-sm">
    <div class="glass-panel w-full max-w-xl rounded-2xl p-6 space-y-5 border border-slate-700 shadow-2xl">
      
      <div class="flex items-center justify-between border-b border-slate-800 pb-3">
        <div class="flex items-center gap-2.5">
          <div class="w-8 h-8 rounded-lg bg-gradient-to-br from-purple-500 to-indigo-600 flex items-center justify-center text-white text-base" aria-hidden="true">
            🧠
          </div>
          <div>
            <h2 id="modal-title" class="text-base font-bold text-white">NVIDIA Nemotron & LLM Configuration</h2>
            <p class="text-xs text-slate-400">OpenAI-Compatible endpoint for confidence-based deep legal reasoning</p>
          </div>
        </div>
        <button onclick="toggleLLMModal()" aria-label="Close modal dialog" class="text-slate-400 hover:text-white p-1 rounded-lg">✕</button>
      </div>

      <div class="space-y-4 text-xs">
        
        <!-- Architecture Explanation Banner -->
        <div class="p-3.5 rounded-xl bg-indigo-950/50 border border-indigo-800/50 text-indigo-200 space-y-1 leading-relaxed">
          <strong class="text-white">⚡ Local-First Routing Architecture:</strong> Contracts are analyzed locally with 100% PII redaction. If local heuristic confidence is high (&ge; 75%), analysis completes in sub-milliseconds with 0 external network calls. If confidence is low, only the anonymized clause is escalated to Nemotron!
        </div>

        <!-- API Key Input -->
        <div>
          <label class="block font-bold text-slate-300 mb-1" for="modal-api-key">API Key (Nemotron / OpenAI / OpenRouter)</label>
          <input type="password" id="modal-api-key" placeholder="nvapi-... or sk-..." class="w-full px-3 py-2 rounded-lg bg-slate-900 border border-slate-700 text-white placeholder:text-slate-500 focus:border-indigo-500">
        </div>

        <!-- Base URL with Presets -->
        <div>
          <div class="flex items-center justify-between mb-1">
            <label class="font-bold text-slate-300" for="modal-base-url">Base URL</label>
            <div class="space-x-1" role="group" aria-label="Preset URLs">
              <button type="button" onclick="setBaseUrlPreset('https://integrate.api.nvidia.com/v1', 'nvidia/llama-3.1-nemotron-70b-instruct')" class="text-[11px] text-purple-400 hover:underline font-semibold">NVIDIA Nemotron</button>
              <span class="text-slate-600" aria-hidden="true">•</span>
              <button type="button" onclick="setBaseUrlPreset('https://openrouter.ai/api/v1', 'nvidia/llama-3.1-nemotron-70b-instruct')" class="text-[11px] text-indigo-400 hover:underline font-semibold">OpenRouter</button>
              <span class="text-slate-600" aria-hidden="true">•</span>
              <button type="button" onclick="setBaseUrlPreset('http://localhost:11434/v1', 'nemotron-mini')" class="text-[11px] text-cyan-400 hover:underline font-semibold">Local vLLM/Ollama</button>
            </div>
          </div>
          <input type="text" id="modal-base-url" value="https://integrate.api.nvidia.com/v1" class="w-full px-3 py-2 rounded-lg bg-slate-900 border border-slate-700 text-white font-mono text-[11px] focus:border-indigo-500">
        </div>

        <!-- Model Identifier -->
        <div>
          <label class="block font-bold text-slate-300 mb-1" for="modal-model-name">Model Name</label>
          <input type="text" id="modal-model-name" value="nvidia/llama-3.1-nemotron-70b-instruct" class="w-full px-3 py-2 rounded-lg bg-slate-900 border border-slate-700 text-white font-mono text-[11px] focus:border-indigo-500">
        </div>

        <!-- Confidence Threshold Slider -->
        <div>
          <div class="flex items-center justify-between mb-1">
            <label class="font-bold text-slate-300" for="modal-threshold">Escalation Confidence Threshold</label>
            <span id="threshold-val" class="font-extrabold text-indigo-400">75%</span>
          </div>
          <input type="range" id="modal-threshold" min="50" max="95" value="75" aria-valuemin="50" aria-valuemax="95" aria-valuenow="75" oninput="document.getElementById('threshold-val').innerText = this.value + '%'" class="w-full accent-indigo-500">
          <p class="text-[11px] text-slate-400 mt-1">Clauses with local confidence below this threshold escalate to Nemotron for deep synthesis.</p>
        </div>

      </div>

      <!-- Modal Footer -->
      <div class="flex items-center justify-between pt-3 border-t border-slate-800">
        <button type="button" onclick="testConnection()" id="modal-test-btn" class="px-3.5 py-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-bold border border-slate-700 transition flex items-center gap-1.5">
          <span>Ping / Test Connection</span>
        </button>
        <div class="flex items-center gap-2">
          <button type="button" onclick="toggleLLMModal()" class="px-3 py-2 rounded-lg text-slate-400 hover:text-white text-xs font-semibold">Cancel</button>
          <button type="button" onclick="saveLLMSettings()" id="modal-save-btn" class="px-4 py-2 rounded-lg bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-bold shadow-md shadow-indigo-600/30 transition">
            Save & Enable Nemotron
          </button>
        </div>
      </div>
      <div id="modal-test-result" role="status" aria-live="polite" class="hidden text-xs p-3 rounded-lg"></div>
    </div>
  </div>

  <!-- Main Landmark -->
  <main id="main-content" role="main" class="relative z-10 flex-1 max-w-7xl w-full mx-auto p-4 sm:p-6 lg:p-8 space-y-6">

    <!-- ==================== TAB 1: ANALYZER ==================== -->
    <section id="tab-analyzer" role="tabpanel" aria-labelledby="nav-tab-analyzer" class="space-y-6">
      
      <!-- Ingestion & Configuration Box -->
      <div class="glass-panel rounded-2xl p-5 sm:p-6 space-y-4 shadow-xl">
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div>
            <h2 class="text-base sm:text-lg font-extrabold text-white flex items-center gap-2">
              <span>Contract Risk Matrix & Plain-English Navigator</span>
            </h2>
            <p class="text-xs text-slate-400">Local-first analysis accelerated by Cython C-extensions with Nemotron deep reasoning</p>
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

        <div class="relative">
          <label for="contract-input" class="block text-xs font-bold text-slate-300 mb-1">Contract Document Text:</label>
          <textarea id="contract-input" rows="8" aria-describedby="contract-input-desc" class="w-full font-mono text-xs text-slate-200 p-3.5 rounded-xl bg-slate-900/90 border border-slate-800 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition leading-relaxed" placeholder="Paste your contract, NDA, SOW, or terms of service here..."></textarea>
          <span id="contract-input-desc" class="sr-only">Input area for contract text. All PII is sanitized locally before analysis.</span>
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

          <button type="button" onclick="runAnalysis()" id="analyze-btn" class="inline-flex items-center gap-2 px-6 py-2.5 rounded-xl bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-500 hover:to-purple-500 text-white text-xs sm:text-sm font-extrabold shadow-lg shadow-indigo-600/30 transition-all hover:scale-[1.01] active:scale-[0.99]">
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
            <span id="escalated-count-pill" class="px-2.5 py-0.5 rounded-full bg-purple-500/20 text-purple-200 border border-purple-500/40 font-bold text-[11px]">
              Escalated: 0 clauses
            </span>
          </div>
        </div>

        <!-- Executive Risk Scorecard -->
        <div class="glass-panel rounded-2xl p-6 shadow-xl space-y-6">
          <div class="grid grid-cols-1 lg:grid-cols-4 gap-6 items-center">
            
            <!-- Risk Gauge with High Contrast -->
            <div class="flex flex-col items-center justify-center p-6 bg-slate-900/90 rounded-2xl border border-slate-800 text-center relative overflow-hidden">
              <span class="text-xs font-bold uppercase tracking-wider text-slate-400">Legal Risk Index</span>
              <div class="relative flex items-center justify-center my-3" aria-label="Risk Score">
                <span id="score-meter" class="text-6xl font-black text-white tracking-tight">--</span>
                <span class="text-xs font-bold text-slate-400 ml-1">/100</span>
              </div>
              <span id="score-badge" class="px-3 py-1 text-xs font-extrabold rounded-full badge-high uppercase tracking-wider">
                EVALUATING
              </span>
            </div>

            <!-- Stats & Exposure Breakdown -->
            <div class="lg:col-span-3 space-y-4">
              <div>
                <h3 class="text-lg font-extrabold text-white tracking-tight" id="results-title">Contract Assessment</h3>
                <p class="text-xs text-slate-200 mt-1.5 leading-relaxed" id="executive-summary"></p>
              </div>

              <!-- Clause Count Counters -->
              <div class="grid grid-cols-3 gap-3" role="group" aria-label="Risk Summary Counts">
                <div class="p-3.5 rounded-xl bg-rose-500/15 border border-rose-500/30 text-center">
                  <div class="text-2xl font-black text-rose-300" id="high-risk-count">0</div>
                  <div class="text-[11px] font-bold text-rose-200 mt-0.5">High Risk Traps</div>
                </div>
                <div class="p-3.5 rounded-xl bg-amber-500/15 border border-amber-500/30 text-center">
                  <div class="text-2xl font-black text-amber-300" id="medium-risk-count">0</div>
                  <div class="text-[11px] font-bold text-amber-200 mt-0.5">Moderate Risks</div>
                </div>
                <div class="p-3.5 rounded-xl bg-emerald-500/15 border border-emerald-500/30 text-center">
                  <div class="text-2xl font-black text-emerald-300" id="low-risk-count">0</div>
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

        <!-- Structured Explorer Navigation -->
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-800 pb-3">
          <div class="flex space-x-6" role="tablist" aria-label="Results Explorer View">
            <button role="tab" id="view-clauses-btn" aria-selected="true" onclick="switchAnalysisView('clauses')" class="font-bold text-xs sm:text-sm text-indigo-400 border-b-2 border-indigo-500 pb-2 transition">
              Clause-by-Clause Translation & Risks
            </button>
            <button role="tab" id="view-checklist-btn" aria-selected="false" onclick="switchAnalysisView('checklist')" class="font-bold text-xs sm:text-sm text-slate-400 hover:text-slate-200 border-b-2 border-transparent pb-2 transition">
              Attorney Consultation Brief
            </button>
          </div>
          <div class="flex items-center space-x-2 text-xs">
            <label for="filter-risk" class="text-slate-300 font-bold">Filter Clauses:</label>
            <select id="filter-risk" onchange="filterClauses(this.value)" class="text-xs rounded-lg border-slate-700 py-1.5 px-3 bg-slate-900 text-slate-200 font-semibold focus:border-indigo-500">
              <option value="ALL">All Clauses</option>
              <option value="HIGH">🚨 High Risk Traps Only</option>
              <option value="ESCALATED">🧠 Nemotron Escalated Only</option>
              <option value="MEDIUM">⚠️ Moderate Only</option>
              <option value="LOW">✅ Standard Only</option>
            </select>
          </div>
        </div>

        <!-- Clause Cards Container -->
        <div id="clause-cards-view" class="space-y-4" role="region" aria-label="Clause Cards">
          <!-- Dynamically populated -->
        </div>

        <!-- Attorney Consultation Checklist View -->
        <div id="attorney-checklist-view" class="hidden glass-panel rounded-2xl p-6 space-y-6 shadow-xl" role="region" aria-label="Attorney Consultation Brief">
          <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-800 pb-4">
            <div>
              <h3 class="text-base sm:text-lg font-extrabold text-white">Attorney Consultation Brief</h3>
              <p class="text-xs text-slate-400">Structured briefing memo with prioritized legal questions and counter-proposal redlines.</p>
            </div>
            <div class="flex items-center gap-2">
              <button type="button" onclick="copyChecklistMarkdown()" class="text-xs bg-slate-800 hover:bg-slate-700 text-slate-200 font-bold px-3 py-1.5 rounded-lg border border-slate-700 transition inline-flex items-center gap-1.5">
                📋 Copy Markdown
              </button>
              <button type="button" onclick="downloadChecklistFile()" class="text-xs bg-indigo-600 hover:bg-indigo-500 text-white font-bold px-3 py-1.5 rounded-lg transition inline-flex items-center gap-1.5 shadow-md shadow-indigo-600/20">
                ⬇️ Export Brief (.md)
              </button>
            </div>
          </div>

          <div id="checklist-questions-list" class="space-y-4">
            <!-- Populated by JS -->
          </div>

          <div>
            <h4 class="text-sm font-bold text-white mb-2.5">Priority Counter-Proposal Checklist (Redlines)</h4>
            <ul id="checklist-redlines-list" class="space-y-2 text-xs text-slate-200">
              <!-- Redline items populated by JS -->
            </ul>
          </div>
        </div>

      </div>
    </section>

    <!-- ==================== TAB 2: COMPARATOR ==================== -->
    <section id="tab-comparator" role="tabpanel" aria-labelledby="nav-tab-comparator" class="hidden space-y-6">
      <div class="glass-panel rounded-2xl p-5 sm:p-6 space-y-4 shadow-xl">
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div>
            <h2 class="text-base sm:text-lg font-extrabold text-white">Side-by-Side Contract Comparator</h2>
            <p class="text-xs text-slate-400">Accelerated by native Cython Jaccard token alignment for instant diff tracking</p>
          </div>
          <button type="button" onclick="loadSampleComparison()" class="text-xs bg-indigo-950/70 hover:bg-indigo-900/70 text-indigo-300 font-bold px-3.5 py-1.5 rounded-lg border border-indigo-700/50 transition">
            ⚡ 1-Click Load: Original vs. Negotiated Draft
          </button>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label for="compare-v1" class="block text-xs font-bold text-slate-300 mb-1">Contract A (Original / Standard Draft):</label>
            <textarea id="compare-v1" rows="7" class="w-full font-mono text-xs text-slate-200 p-3 rounded-xl bg-slate-900 border border-slate-800 focus:ring-2 focus:ring-indigo-500" placeholder="Paste base agreement..."></textarea>
          </div>
          <div>
            <label for="compare-v2" class="block text-xs font-bold text-slate-300 mb-1">Contract B (Counter-Proposal / Revised Draft):</label>
            <textarea id="compare-v2" rows="7" class="w-full font-mono text-xs text-slate-200 p-3 rounded-xl bg-slate-900 border border-slate-800 focus:ring-2 focus:ring-indigo-500" placeholder="Paste revised agreement..."></textarea>
          </div>
        </div>

        <div class="flex justify-end">
          <button type="button" onclick="runComparison()" class="inline-flex items-center gap-2 px-6 py-2.5 rounded-xl bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-500 hover:to-purple-500 text-white text-xs sm:text-sm font-extrabold shadow-lg shadow-indigo-600/30 transition">
            Compare Versions & Liability Shift
          </button>
        </div>
      </div>

      <!-- Comparison Results -->
      <div id="comparator-results" role="region" aria-label="Comparison Results" class="hidden space-y-6">
        <div class="glass-panel rounded-2xl p-6 shadow-xl space-y-4">
          <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-800 pb-4">
            <div>
              <span id="compare-trajectory-badge" class="px-3 py-1 text-xs font-extrabold rounded-full badge-low uppercase">
                ANALYZING
              </span>
              <h3 class="text-base font-bold text-white mt-2">Overall Liability Trajectory</h3>
              <p class="text-xs text-slate-300" id="compare-scores-summary"></p>
            </div>
          </div>

          <div>
            <h4 class="text-xs font-bold uppercase tracking-wider text-slate-400 mb-2">Summary of Key Changes:</h4>
            <ul id="compare-changes-list" class="space-y-1.5 text-xs text-slate-300"></ul>
          </div>
        </div>

        <div id="compare-diff-cards" class="space-y-4">
          <!-- Diff cards populated by JS -->
        </div>
      </div>
    </section>

    <!-- ==================== TAB 3: CHAT ==================== -->
    <section id="tab-chat" role="tabpanel" aria-labelledby="nav-tab-chat" class="hidden space-y-6">
      <div class="glass-panel rounded-2xl p-5 sm:p-6 space-y-4 shadow-xl">
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
          <div>
            <h2 class="text-base sm:text-lg font-extrabold text-white">Legal Navigator Assistant</h2>
            <p class="text-xs text-slate-400">Context-grounded assistant with mandatory non-advisory guardrails and clause citations</p>
          </div>
          <span id="chat-model-badge" class="text-xs font-bold px-3 py-1 rounded-full bg-slate-800 text-slate-300 border border-slate-700">
            Engine: Local Grounded Rules
          </span>
        </div>

        <!-- Quick Question Chips -->
        <div class="flex flex-wrap gap-2 pt-1" role="group" aria-label="Suggested Prompts">
          <button type="button" onclick="sendQuickPrompt('Can the client terminate without paying me for completed work?')" class="text-xs bg-slate-800/80 hover:bg-slate-700 text-slate-200 px-3 py-1.5 rounded-lg border border-slate-700 transition font-semibold">
            ❓ Can they cancel without paying?
          </button>
          <button type="button" onclick="sendQuickPrompt('Who owns the code and tools I create under this agreement?')" class="text-xs bg-slate-800/80 hover:bg-slate-700 text-slate-200 px-3 py-1.5 rounded-lg border border-slate-700 transition font-semibold">
            💡 Who owns the IP?
          </button>
          <button type="button" onclick="sendQuickPrompt('What is my maximum financial liability if something goes wrong?')" class="text-xs bg-slate-800/80 hover:bg-slate-700 text-slate-200 px-3 py-1.5 rounded-lg border border-slate-700 transition font-semibold">
            🛡️ What is my maximum liability?
          </button>
          <button type="button" onclick="sendQuickPrompt('Is there a binding arbitration clause or class action waiver?')" class="text-xs bg-slate-800/80 hover:bg-slate-700 text-slate-200 px-3 py-1.5 rounded-lg border border-slate-700 transition font-semibold">
            ⚖️ Is there an arbitration clause?
          </button>
        </div>

        <!-- Accessible Chat Log Window -->
        <div id="chat-messages" role="log" aria-live="polite" aria-label="Conversation Log" class="h-96 overflow-y-auto p-4 bg-slate-900/90 rounded-xl border border-slate-800 space-y-4 text-xs">
          <div class="p-3.5 bg-slate-800/80 rounded-xl border border-slate-700/60 max-w-xl text-slate-200 shadow-md">
            <p class="leading-relaxed">
              👋 Greetings! I am your <strong>Legal-Ease Navigator</strong>. Ask me any question regarding the active contract text. If you configured a Nemotron API key, questions can leverage deep neural synthesis!
            </p>
          </div>
        </div>

        <!-- Chat Input Form -->
        <form onsubmit="handleChatSubmit(event)" class="flex gap-2">
          <label for="chat-input" class="sr-only">Ask a question about your contract</label>
          <input type="text" id="chat-input" class="flex-1 text-xs rounded-xl border border-slate-700 bg-slate-900 p-3 text-white placeholder:text-slate-500 focus:border-indigo-500" placeholder="Ask a question (e.g., 'What happens if deliverables are delayed?')...">
          <button type="submit" class="px-5 py-3 bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-500 hover:to-purple-500 text-white text-xs font-bold rounded-xl shadow-md transition">
            Send Query
          </button>
        </form>
      </div>
    </section>

    <!-- ==================== TAB 4: PRIVACY VAULT ==================== -->
    <section id="tab-privacy" role="tabpanel" aria-labelledby="nav-tab-privacy" class="hidden space-y-6">
      <div class="glass-panel rounded-2xl p-6 space-y-6 shadow-xl">
        <div>
          <h2 class="text-base sm:text-lg font-extrabold text-white">🛡️ Zero-Knowledge Local PII Shield Audit</h2>
          <p class="text-xs text-slate-400">
            Sensitive personal & business identifiers (names, SSNs, bank accounts, emails, fees) are permanently masked before any external processing.
          </p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-4 text-center">
          <div class="p-5 bg-slate-900/80 rounded-xl border border-slate-800">
            <span class="text-3xl font-black text-indigo-400" id="privacy-total-redacted">0</span>
            <div class="text-xs font-bold text-slate-400 mt-1">Sensitive Entities Masked</div>
          </div>
          <div class="p-5 bg-slate-900/80 rounded-xl border border-slate-800">
            <span class="text-3xl font-black text-emerald-400" id="privacy-score-display">100%</span>
            <div class="text-xs font-bold text-slate-400 mt-1">Local Privacy Score</div>
          </div>
          <div class="p-5 bg-slate-900/80 rounded-xl border border-slate-800">
            <span class="text-3xl font-black text-purple-400">Client Sandbox</span>
            <div class="text-xs font-bold text-slate-400 mt-1">Local In-Memory Pseudonymization</div>
          </div>
        </div>

        <div>
          <h3 class="text-sm font-bold text-white mb-2.5">Redacted Entities Audit Log</h3>
          <div class="overflow-x-auto border border-slate-800 rounded-xl">
            <table class="min-w-full divide-y divide-slate-800 text-xs text-left" aria-label="PII Redaction Audit Table">
              <thead class="bg-slate-900 text-slate-300 font-bold uppercase tracking-wider">
                <tr>
                  <th scope="col" class="px-4 py-3">Entity Type</th>
                  <th scope="col" class="px-4 py-3">Assigned Token</th>
                  <th scope="col" class="px-4 py-3">Original Sensitive Value</th>
                </tr>
              </thead>
              <tbody id="privacy-table-body" class="divide-y divide-slate-800/60 text-slate-300">
                <tr>
                  <td colspan="3" class="px-4 py-6 text-center text-slate-500">
                    No active analysis yet. Load a contract in the Analyzer tab to view the live audit vault.
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </section>

  </main>

  <!-- Footer Landmark -->
  <footer role="contentinfo" class="relative z-10 glass-panel border-t border-slate-800 py-4 text-center text-xs text-slate-400">
    <div class="max-w-7xl mx-auto px-4 flex flex-col sm:flex-row items-center justify-between gap-2">
      <div>
        <strong>Legal-Ease</strong> — Built strictly with <code class="text-indigo-400 font-mono">uv</code> and <code class="text-indigo-400 font-mono">pnpm</code>. Repository size: &lt; 1 MB.
      </div>
      <div>
        Hackathon Vertical: <strong>AI for Legal Assistance & Access</strong> (Local Shield + Cython + Nemotron)
      </div>
    </div>
  </footer>

  <!-- Interactive Accessible JavaScript Application -->
  <script>
    let currentAnalysis = null;
    let cachedSamples = [];
    let llmSettings = {
      api_key_configured: false,
      base_url: 'https://integrate.api.nvidia.com/v1',
      model_name: 'nvidia/llama-3.1-nemotron-70b-instruct',
      confidence_threshold: 0.75
    };

    // Accessible Tab Switcher (WCAG Tablist)
    function switchTab(tabName) {
      const tabs = ['analyzer', 'comparator', 'chat', 'privacy'];
      tabs.forEach(t => {
        const section = document.getElementById(`tab-${t}`);
        const navBtn = document.getElementById(`nav-tab-${t}`);
        if (t === tabName) {
          section.classList.remove('hidden');
          navBtn.setAttribute('aria-selected', 'true');
          navBtn.setAttribute('tabindex', '0');
          navBtn.classList.add('border-indigo-500', 'text-indigo-400');
          navBtn.classList.remove('border-transparent', 'text-slate-400');
        } else {
          section.classList.add('hidden');
          navBtn.setAttribute('aria-selected', 'false');
          navBtn.setAttribute('tabindex', '-1');
          navBtn.classList.remove('border-indigo-500', 'text-indigo-400');
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
      }
    }

    function handleFileUpload(event) {
      const file = event.target.files[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = (e) => {
          document.getElementById('contract-input').value = e.target.result;
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

    // Nemotron Settings Modal handlers
    function toggleLLMModal() {
      const modal = document.getElementById('llm-modal');
      const btn = document.getElementById('llm-status-btn');
      const isHidden = modal.classList.toggle('hidden');
      btn.setAttribute('aria-expanded', String(!isHidden));
      if (!isHidden) {
        document.getElementById('modal-api-key').focus();
      }
    }

    function setBaseUrlPreset(url, model) {
      document.getElementById('modal-base-url').value = url;
      document.getElementById('modal-model-name').value = model;
    }

    async function loadLLMSettings() {
      try {
        const res = await fetch('/api/settings/llm');
        if (res.ok) {
          llmSettings = await res.json();
          const dot = document.getElementById('nemotron-dot');
          const label = document.getElementById('nemotron-label');
          if (llmSettings.api_key_configured) {
            dot.className = 'w-2 h-2 rounded-full bg-purple-400 animate-pulse';
            label.innerText = 'Nemotron Active';
            document.getElementById('chat-model-badge').innerText = `Engine: ${llmSettings.model_name}`;
          } else {
            dot.className = 'w-2 h-2 rounded-full bg-slate-500';
            label.innerText = 'Configure Nemotron';
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
        enabled: true
      };
      if (apiKey) payload.api_key = apiKey;

      try {
        const res = await fetch('/api/settings/llm', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        });
        if (res.ok) {
          await loadLLMSettings();
          toggleLLMModal();
          alert('Nemotron configuration saved successfully!');
        }
      } catch (e) {
        alert('Failed to save settings: ' + e);
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
            model_name: document.getElementById('modal-model-name').value.trim()
          })
        });
      }

      try {
        const res = await fetch('/api/settings/test', { method: 'POST' });
        const data = await res.json();
        resBox.classList.remove('hidden');
        if (data.success) {
          resBox.className = 'text-xs p-3 rounded-lg bg-emerald-950/70 border border-emerald-700/70 text-emerald-200 font-semibold';
          resBox.innerText = `✅ Success! Connected to model '${data.model}' on ${data.base_url}`;
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

      // Score and Level
      const index = data.risk_overview.legal_risk_index;
      document.getElementById('score-meter').innerText = index;
      const badge = document.getElementById('score-badge');
      badge.innerText = data.risk_overview.risk_level;
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
        if (clause.analysis_source === 'NEMOTRON_DEEP_REASONING') {
          sourcePill = `<span class="px-2.5 py-0.5 text-[11px] font-bold rounded-full badge-nemotron">🧠 Nemotron Deep Synthesis</span>`;
        } else {
          sourcePill = `<span class="px-2.5 py-0.5 text-[11px] font-semibold rounded-full bg-slate-800 text-slate-300 border border-slate-700">⚡ ${Math.round(clause.confidence * 100)}% Local Confidence</span>`;
        }

        const trapsHtml = clause.detected_traps.map(t => 
          `<span class="inline-block bg-rose-500/25 text-rose-200 border border-rose-500/40 text-[11px] font-bold px-2 py-0.5 rounded-md mr-1 mt-1">⚠️ ${t}</span>`
        ).join('');

        card.className = `glass-card rounded-2xl p-5 sm:p-6 space-y-4 clause-card transition-all ${clause.analysis_source === 'NEMOTRON_DEEP_REASONING' ? 'border-purple-500/40 shadow-lg shadow-purple-950/20' : ''}`;
        card.setAttribute('data-severity', clause.severity);
        card.setAttribute('data-source', clause.analysis_source);

        card.innerHTML = `
          <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-800 pb-3">
            <div class="flex items-center gap-2.5">
              <span class="text-xs font-bold bg-slate-800 text-slate-300 px-2.5 py-0.5 rounded-md border border-slate-700">#${clause.id}</span>
              <h4 class="text-sm sm:text-base font-extrabold text-white">${clause.section_title}</h4>
            </div>
            <div class="flex items-center gap-2">
              <span class="text-[11px] font-semibold text-slate-400 uppercase tracking-wider">${clause.category.replace('_', ' ')}</span>
              ${severityBadge}
              ${sourcePill}
            </div>
          </div>

          ${clause.escalation_reason ? `<div class="text-[11px] text-purple-200 bg-purple-950/50 border border-purple-800/60 p-2.5 rounded-lg font-medium">💡 ${clause.escalation_reason}</div>` : ''}

          ${trapsHtml ? `<div class="pt-0.5">${trapsHtml}</div>` : ''}

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
              <div class="text-xs font-bold uppercase tracking-wider text-indigo-300">Recommended Redline / Fallback:</div>
              <div class="text-xs text-indigo-100 bg-indigo-950/50 p-3.5 rounded-xl border border-indigo-900/60 leading-relaxed">
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
        if (level === 'ALL') {
          c.classList.remove('hidden');
        } else if (level === 'ESCALATED') {
          if (src === 'NEMOTRON_DEEP_REASONING') c.classList.remove('hidden');
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
          <p class="text-xs sm:text-sm font-extrabold text-white leading-snug">"${q.question}"</p>
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
            <h4 class="text-sm font-extrabold text-white">${diff.section_title}</h4>
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

    // Keyboard navigation for W3C tabs (ArrowLeft, ArrowRight)
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') {
        const modal = document.getElementById('llm-modal');
        if (!modal.classList.contains('hidden')) {
          toggleLLMModal();
        }
      }
    });

    // Startup bootstrap
    window.addEventListener('DOMContentLoaded', () => {
      initSamples();
      loadLLMSettings();
    });
  </script>
</body>
</html>
"""
