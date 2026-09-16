"""
Web UI dashboard template and component builder for Legal-Ease.
Self-contained, accessible, and fast Single Page Application.
"""

def get_dashboard_html() -> str:
    """Return the complete, self-contained dashboard HTML."""
    return """<!DOCTYPE html>
<html lang="en" class="h-full bg-slate-50 text-slate-900">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
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
              500: '#6366f1',
              600: '#4f46e5',
              700: '#4338ca',
              900: '#312e81',
            }
          }
        }
      }
    }
  </script>
  <style>
    .tab-active {
      border-bottom-color: #4f46e5;
      color: #4f46e5;
      font-weight: 600;
    }
    .badge-high {
      background-color: #fee2e2;
      color: #991b1b;
      border: 1px solid #fca5a5;
    }
    .badge-medium {
      background-color: #fef3c7;
      color: #92400e;
      border: 1px solid #fcd34d;
    }
    .badge-low {
      background-color: #d1fae5;
      color: #065f46;
      border: 1px solid #6ee7b7;
    }
    /* Accessible focus ring */
    button:focus-visible, a:focus-visible, input:focus-visible, textarea:focus-visible {
      outline: 2px solid #4f46e5;
      outline-offset: 2px;
    }
  </style>
</head>
<body class="h-full flex flex-col font-sans antialiased">

  <!-- Top Disclaimer Notice Bar -->
  <aside aria-label="Legal Disclaimer" class="bg-amber-100 border-b border-amber-200 text-amber-900 text-xs py-1.5 px-4 text-center font-medium">
    ⚖️ <strong>Informational Tool Only:</strong> Legal-Ease assists with document literacy and negotiation prep. It does not provide legal advice or create an attorney-client relationship. Always consult a licensed attorney.
  </aside>

  <!-- Navigation Header -->
  <header class="bg-white border-b border-slate-200 sticky top-0 z-30 shadow-sm">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex items-center justify-between h-16">
      <div class="flex items-center space-x-3">
        <div class="w-10 h-10 rounded-lg bg-brand-600 flex items-center justify-center text-white font-bold text-xl shadow-md">
          ⚖️
        </div>
        <div>
          <h1 class="text-xl font-bold tracking-tight text-slate-900 flex items-center gap-2">
            Legal-Ease
            <span class="text-xs bg-indigo-100 text-indigo-800 font-semibold px-2 py-0.5 rounded-full">Privacy-First AI</span>
          </h1>
          <p class="text-xs text-slate-500">Legal Document Literacy & Contract Risk Navigator</p>
        </div>
      </div>

      <div class="flex items-center space-x-4 text-xs">
        <span class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full font-medium bg-emerald-50 text-emerald-700 border border-emerald-200">
          <span class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
          100% Local PII Redacted
        </span>
        <a href="https://github.com/seeramsujay/legal-ease" target="_blank" rel="noopener noreferrer" class="hidden sm:inline-flex items-center gap-1 px-3 py-1.5 rounded-md bg-slate-100 hover:bg-slate-200 text-slate-700 font-medium transition">
          <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24"><path fill-rule="evenodd" clip-rule="evenodd" d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.53 1.032 1.53 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z"/></svg>
          GitHub Repo
        </a>
      </div>
    </div>

    <!-- Main Navigation Tabs -->
    <nav class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex space-x-8 border-t border-slate-200 overflow-x-auto" aria-label="Main Navigation">
      <button id="nav-tab-analyzer" onclick="switchTab('analyzer')" class="py-3 px-1 border-b-2 font-medium text-sm border-brand-600 text-brand-600 flex items-center gap-2 whitespace-nowrap">
        📄 Contract Risk Analyzer
      </button>
      <button id="nav-tab-comparator" onclick="switchTab('comparator')" class="py-3 px-1 border-b-2 font-medium text-sm border-transparent text-slate-500 hover:text-slate-700 hover:border-slate-300 flex items-center gap-2 whitespace-nowrap">
        ⚖️ Version Comparator
      </button>
      <button id="nav-tab-chat" onclick="switchTab('chat')" class="py-3 px-1 border-b-2 font-medium text-sm border-transparent text-slate-500 hover:text-slate-700 hover:border-slate-300 flex items-center gap-2 whitespace-nowrap">
        💬 Legal Navigator AI
      </button>
      <button id="nav-tab-privacy" onclick="switchTab('privacy')" class="py-3 px-1 border-b-2 font-medium text-sm border-transparent text-slate-500 hover:text-slate-700 hover:border-slate-300 flex items-center gap-2 whitespace-nowrap">
        🛡️ Privacy & PII Vault
      </button>
    </nav>
  </header>

  <!-- Main Container -->
  <main class="flex-1 max-w-7xl w-full mx-auto p-4 sm:p-6 lg:p-8 space-y-6">

    <!-- ==================== TAB 1: ANALYZER ==================== -->
    <section id="tab-analyzer" class="space-y-6" aria-labelledby="nav-tab-analyzer">
      <!-- Input Panel -->
      <div class="bg-white rounded-xl shadow-sm border border-slate-200 p-5 space-y-4">
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div>
            <h2 class="text-lg font-semibold text-slate-900">Upload or Paste Legal Agreement</h2>
            <p class="text-xs text-slate-500">All sensitive identifiers are anonymized locally before analysis.</p>
          </div>
          <div class="flex flex-wrap items-center gap-2">
            <span class="text-xs text-slate-500 font-medium">Quick Samples:</span>
            <button onclick="loadSample('freelance_high_risk')" class="text-xs bg-slate-100 hover:bg-slate-200 text-slate-800 font-medium px-2.5 py-1 rounded transition">
              🚨 Freelance (High Risk)
            </button>
            <button onclick="loadSample('freelance_negotiated')" class="text-xs bg-slate-100 hover:bg-slate-200 text-slate-800 font-medium px-2.5 py-1 rounded transition">
              ✅ Negotiated (Low Risk)
            </button>
            <button onclick="loadSample('saas_terms')" class="text-xs bg-slate-100 hover:bg-slate-200 text-slate-800 font-medium px-2.5 py-1 rounded transition">
              ☁️ SaaS ToS
            </button>
            <button onclick="loadSample('mutual_nda')" class="text-xs bg-slate-100 hover:bg-slate-200 text-slate-800 font-medium px-2.5 py-1 rounded transition">
              🤝 Mutual NDA
            </button>
          </div>
        </div>

        <div class="relative">
          <label for="contract-input" class="sr-only">Contract Text</label>
          <textarea id="contract-input" rows="8" class="w-full font-mono text-xs text-slate-800 p-3 rounded-lg border border-slate-300 focus:ring-2 focus:ring-brand-500 focus:border-brand-500" placeholder="Paste your contract, agreement, NDA, or terms of service here..."></textarea>
        </div>

        <div class="flex flex-wrap items-center justify-between gap-4 pt-1">
          <div class="flex items-center space-x-3">
            <label class="cursor-pointer inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg border border-slate-300 bg-white hover:bg-slate-50 text-xs font-medium text-slate-700 shadow-sm">
              <svg class="w-4 h-4 text-slate-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12"/></svg>
              Upload .txt / .md
              <input type="file" id="file-upload" class="hidden" accept=".txt,.md" onchange="handleFileUpload(event)">
            </label>
            <button type="button" onclick="previewPII()" class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg border border-slate-300 bg-white hover:bg-slate-50 text-xs font-medium text-slate-700 shadow-sm">
              🛡️ Preview PII Masking
            </button>
          </div>

          <button type="button" onclick="runAnalysis()" id="analyze-btn" class="inline-flex items-center gap-2 px-5 py-2 rounded-lg bg-brand-600 hover:bg-brand-700 text-white text-sm font-semibold shadow-sm transition">
            <span>Analyze Contract & Score Risks</span>
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3"/></svg>
          </button>
        </div>
      </div>

      <!-- Loading State -->
      <div id="analyzer-loading" class="hidden text-center py-12 space-y-3">
        <div class="inline-block w-8 h-8 border-4 border-brand-500 border-t-transparent rounded-full animate-spin"></div>
        <p class="text-sm font-medium text-slate-600">Redacting PII and evaluating risk exposure matrix...</p>
      </div>

      <!-- Results Container -->
      <div id="analyzer-results" class="hidden space-y-6">

        <!-- Executive Risk Scorecard -->
        <div class="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
          <div class="grid grid-cols-1 md:grid-cols-4 gap-6 items-center">
            
            <!-- Risk Gauge / Meter -->
            <div class="flex flex-col items-center justify-center p-4 bg-slate-50 rounded-xl border border-slate-100 text-center">
              <span class="text-xs font-semibold uppercase tracking-wider text-slate-500">Legal Risk Index</span>
              <div class="relative flex items-center justify-center my-2">
                <span id="score-meter" class="text-5xl font-extrabold text-slate-900">--</span>
                <span class="text-xs font-semibold text-slate-400 ml-1">/100</span>
              </div>
              <span id="score-badge" class="px-3 py-1 text-xs font-bold rounded-full badge-high uppercase tracking-wide">
                EVALUATING
              </span>
            </div>

            <!-- Stats & Exposure Breakdown -->
            <div class="md:col-span-3 space-y-4">
              <div>
                <h3 class="text-base font-bold text-slate-900" id="results-title">Contract Assessment</h3>
                <p class="text-xs text-slate-600 mt-1 leading-relaxed" id="executive-summary"></p>
              </div>

              <!-- Clause Count Counters -->
              <div class="grid grid-cols-3 gap-3">
                <div class="p-3 rounded-lg bg-rose-50 border border-rose-200 text-rose-900 text-center">
                  <div class="text-xl font-bold" id="high-risk-count">0</div>
                  <div class="text-xs font-medium">High Risk Traps</div>
                </div>
                <div class="p-3 rounded-lg bg-amber-50 border border-amber-200 text-amber-900 text-center">
                  <div class="text-xl font-bold" id="medium-risk-count">0</div>
                  <div class="text-xs font-medium">Moderate Risks</div>
                </div>
                <div class="p-3 rounded-lg bg-emerald-50 border border-emerald-200 text-emerald-900 text-center">
                  <div class="text-xl font-bold" id="low-risk-count">0</div>
                  <div class="text-xs font-medium">Standard Clauses</div>
                </div>
              </div>

              <!-- Critical Findings Banner -->
              <div id="critical-findings-container" class="space-y-1.5 pt-1">
                <!-- Injected via JS -->
              </div>
            </div>

          </div>
        </div>

        <!-- Section Navigation: Clause Breakdown vs Attorney Checklist -->
        <div class="flex items-center justify-between border-b border-slate-200 pb-2">
          <div class="flex space-x-4">
            <button onclick="switchAnalysisView('clauses')" id="view-clauses-btn" class="font-semibold text-sm text-brand-600 border-b-2 border-brand-600 pb-2">
              Clause-by-Clause Translation & Risks
            </button>
            <button onclick="switchAnalysisView('checklist')" id="view-checklist-btn" class="font-medium text-sm text-slate-500 hover:text-slate-800 border-b-2 border-transparent pb-2">
              Attorney Briefing Checklist
            </button>
          </div>
          <div class="flex items-center space-x-2 text-xs">
            <label for="filter-risk" class="text-slate-500 font-medium">Filter:</label>
            <select id="filter-risk" onchange="filterClauses(this.value)" class="text-xs rounded border-slate-300 py-1 px-2 bg-white text-slate-800">
              <option value="ALL">All Clauses</option>
              <option value="HIGH">High Risk Only</option>
              <option value="MEDIUM">Moderate Only</option>
              <option value="LOW">Standard Only</option>
            </select>
          </div>
        </div>

        <!-- Clause Cards Container -->
        <div id="clause-cards-view" class="space-y-4">
          <!-- Dynamically filled with clauses -->
        </div>

        <!-- Attorney Checklist View (Hidden by default) -->
        <div id="attorney-checklist-view" class="hidden bg-white rounded-xl shadow-sm border border-slate-200 p-6 space-y-6">
          <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-200 pb-4">
            <div>
              <h3 class="text-lg font-bold text-slate-900">Attorney Consultation Brief</h3>
              <p class="text-xs text-slate-500">Categorized briefing points and prioritized negotiation questions for legal counsel.</p>
            </div>
            <div class="flex items-center gap-2">
              <button onclick="copyChecklistMarkdown()" class="text-xs bg-slate-100 hover:bg-slate-200 text-slate-800 font-medium px-3 py-1.5 rounded-lg transition inline-flex items-center gap-1">
                📋 Copy Markdown
              </button>
              <button onclick="downloadChecklistFile()" class="text-xs bg-brand-600 hover:bg-brand-700 text-white font-medium px-3 py-1.5 rounded-lg transition inline-flex items-center gap-1">
                ⬇️ Export Brief (.md)
              </button>
            </div>
          </div>

          <div id="checklist-questions-list" class="space-y-4">
            <!-- Questions populated by JS -->
          </div>

          <div>
            <h4 class="text-sm font-bold text-slate-900 mb-2">Priority Counter-Proposal Checklist (Redlines)</h4>
            <ul id="checklist-redlines-list" class="space-y-2 text-xs text-slate-700">
              <!-- Redline items populated by JS -->
            </ul>
          </div>
        </div>

      </div>
    </section>

    <!-- ==================== TAB 2: COMPARATOR ==================== -->
    <section id="tab-comparator" class="hidden space-y-6" aria-labelledby="nav-tab-comparator">
      <div class="bg-white rounded-xl shadow-sm border border-slate-200 p-5 space-y-4">
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div>
            <h2 class="text-lg font-semibold text-slate-900">Side-by-Side Contract Comparison</h2>
            <p class="text-xs text-slate-500">Identify modified obligations, newly inserted liabilities, and deleted protections.</p>
          </div>
          <button onclick="loadSampleComparison()" class="text-xs bg-indigo-50 hover:bg-indigo-100 text-indigo-700 font-semibold px-3 py-1.5 rounded-lg border border-indigo-200 transition">
            ⚡ 1-Click Load: Original vs. Negotiated Draft
          </button>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label for="compare-v1" class="block text-xs font-bold text-slate-700 mb-1">Contract A (Original / Standard)</label>
            <textarea id="compare-v1" rows="7" class="w-full font-mono text-xs text-slate-800 p-3 rounded-lg border border-slate-300 focus:ring-2 focus:ring-brand-500" placeholder="Paste original agreement..."></textarea>
          </div>
          <div>
            <label for="compare-v2" class="block text-xs font-bold text-slate-700 mb-1">Contract B (Counter-Proposal / Revised)</label>
            <textarea id="compare-v2" rows="7" class="w-full font-mono text-xs text-slate-800 p-3 rounded-lg border border-slate-300 focus:ring-2 focus:ring-brand-500" placeholder="Paste revised draft..."></textarea>
          </div>
        </div>

        <div class="flex justify-end">
          <button onclick="runComparison()" class="inline-flex items-center gap-2 px-5 py-2 rounded-lg bg-brand-600 hover:bg-brand-700 text-white text-sm font-semibold shadow-sm transition">
            Compare Versions & Liability Shift
          </button>
        </div>
      </div>

      <!-- Comparison Results -->
      <div id="comparator-results" class="hidden space-y-6">
        <div class="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
          <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-200 pb-4">
            <div>
              <span id="compare-trajectory-badge" class="px-3 py-1 text-xs font-bold rounded-full badge-low uppercase">
                ANALYZING
              </span>
              <h3 class="text-base font-bold text-slate-900 mt-2">Overall Liability Shift</h3>
              <p class="text-xs text-slate-500" id="compare-scores-summary"></p>
            </div>
          </div>

          <div class="mt-4">
            <h4 class="text-xs font-bold uppercase tracking-wider text-slate-500 mb-2">Summary of Key Changes:</h4>
            <ul id="compare-changes-list" class="space-y-1.5 text-xs text-slate-700"></ul>
          </div>
        </div>

        <div id="compare-diff-cards" class="space-y-4">
          <!-- Populated by JS -->
        </div>
      </div>
    </section>

    <!-- ==================== TAB 3: CHAT ==================== -->
    <section id="tab-chat" class="hidden space-y-6" aria-labelledby="nav-tab-chat">
      <div class="bg-white rounded-xl shadow-sm border border-slate-200 p-5 space-y-4">
        <div>
          <h2 class="text-lg font-semibold text-slate-900">Legal Navigator Q&A Assistant</h2>
          <p class="text-xs text-slate-500">Ask questions grounded strictly in your loaded contract clauses.</p>
        </div>

        <!-- Quick Question Chips -->
        <div class="flex flex-wrap gap-2 pt-1">
          <button onclick="sendQuickPrompt('Can the client terminate without paying me for completed work?')" class="text-xs bg-slate-100 hover:bg-slate-200 text-slate-800 px-2.5 py-1 rounded-full transition">
            ❓ Can they cancel without paying?
          </button>
          <button onclick="sendQuickPrompt('Who owns the code and tools I create under this agreement?')" class="text-xs bg-slate-100 hover:bg-slate-200 text-slate-800 px-2.5 py-1 rounded-full transition">
            💡 Who owns the IP?
          </button>
          <button onclick="sendQuickPrompt('What is my maximum financial liability if something goes wrong?')" class="text-xs bg-slate-100 hover:bg-slate-200 text-slate-800 px-2.5 py-1 rounded-full transition">
            🛡️ What is my maximum liability?
          </button>
          <button onclick="sendQuickPrompt('Is there a binding arbitration clause or class action waiver?')" class="text-xs bg-slate-100 hover:bg-slate-200 text-slate-800 px-2.5 py-1 rounded-full transition">
            ⚖️ Is there an arbitration clause?
          </button>
        </div>

        <!-- Chat Log Window -->
        <div id="chat-messages" class="h-96 overflow-y-auto p-4 bg-slate-50 rounded-lg border border-slate-200 space-y-4 text-sm">
          <div class="p-3 bg-white rounded-lg border border-slate-200 max-w-xl shadow-xs">
            <p class="text-xs text-slate-700 leading-relaxed">
              Hello! I am your <strong>Legal-Ease Navigator</strong>. Ask me any question about the clauses in your agreement. I will explain the real-world consequences and point out specific risk traps.
            </p>
          </div>
        </div>

        <!-- Chat Input Form -->
        <form onsubmit="handleChatSubmit(event)" class="flex gap-2">
          <input type="text" id="chat-input" class="flex-1 text-xs rounded-lg border border-slate-300 p-2.5 focus:ring-2 focus:ring-brand-500" placeholder="Type your contract question here (e.g., 'What are the payment terms?')...">
          <button type="submit" class="px-4 py-2 bg-brand-600 hover:bg-brand-700 text-white text-xs font-semibold rounded-lg shadow-sm transition">
            Ask Assistant
          </button>
        </form>
      </div>
    </section>

    <!-- ==================== TAB 4: PRIVACY VAULT ==================== -->
    <section id="tab-privacy" class="hidden space-y-6" aria-labelledby="nav-tab-privacy">
      <div class="bg-white rounded-xl shadow-sm border border-slate-200 p-6 space-y-4">
        <div>
          <h2 class="text-lg font-semibold text-slate-900">🛡️ Local PII Redaction & Zero-Knowledge Architecture</h2>
          <p class="text-xs text-slate-500">
            Legal-Ease guarantees that personal identities, financial numbers, SSNs, and corporate addresses are never exposed during linguistic analysis.
          </p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-4 text-center">
          <div class="p-4 bg-slate-50 rounded-lg border border-slate-200">
            <span class="text-2xl font-bold text-indigo-600" id="privacy-total-redacted">0</span>
            <div class="text-xs font-medium text-slate-600 mt-1">Sensitive Entities Masked</div>
          </div>
          <div class="p-4 bg-slate-50 rounded-lg border border-slate-200">
            <span class="text-2xl font-bold text-emerald-600" id="privacy-score-display">100%</span>
            <div class="text-xs font-medium text-slate-600 mt-1">Local Privacy Score</div>
          </div>
          <div class="p-4 bg-slate-50 rounded-lg border border-slate-200">
            <span class="text-2xl font-bold text-slate-800">Local Only</span>
            <div class="text-xs font-medium text-slate-600 mt-1">Client Sandbox Processing</div>
          </div>
        </div>

        <div class="mt-4">
          <h3 class="text-sm font-bold text-slate-900 mb-2">Redacted Entities Audit Vault</h3>
          <div class="overflow-x-auto border border-slate-200 rounded-lg">
            <table class="min-w-full divide-y divide-slate-200 text-xs text-left">
              <thead class="bg-slate-50 text-slate-600 font-semibold uppercase">
                <tr>
                  <th class="px-4 py-2.5">Entity Type</th>
                  <th class="px-4 py-2.5">Assigned Token</th>
                  <th class="px-4 py-2.5">Original Sensitive Value</th>
                </tr>
              </thead>
              <tbody id="privacy-table-body" class="divide-y divide-slate-200 text-slate-700">
                <tr>
                  <td colspan="3" class="px-4 py-6 text-center text-slate-400">
                    No active analysis yet. Load a contract in the Analyzer tab to view the audit log.
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </section>

  </main>

  <!-- Footer -->
  <footer class="bg-white border-t border-slate-200 py-4 text-center text-xs text-slate-500">
    <div class="max-w-7xl mx-auto px-4 flex flex-col sm:flex-row items-center justify-between gap-2">
      <div>
        <strong>Legal-Ease</strong> — Built with <code class="bg-slate-100 px-1 py-0.5 rounded text-indigo-700 font-mono">uv</code> and <code class="bg-slate-100 px-1 py-0.5 rounded text-indigo-700 font-mono">pnpm</code>. Repository size: &lt;10 MB.
      </div>
      <div>
        Hackathon Vertical: <strong>AI for Legal Assistance & Access</strong>
      </div>
    </div>
  </footer>

  <!-- Interactive JavaScript Application -->
  <script>
    let currentAnalysis = null;
    let cachedSamples = [];

    // Tab switcher
    function switchTab(tabName) {
      const tabs = ['analyzer', 'comparator', 'chat', 'privacy'];
      tabs.forEach(t => {
        const section = document.getElementById(`tab-${t}`);
        const navBtn = document.getElementById(`nav-tab-${t}`);
        if (t === tabName) {
          section.classList.remove('hidden');
          navBtn.classList.add('border-brand-600', 'text-brand-600');
          navBtn.classList.remove('border-transparent', 'text-slate-500');
        } else {
          section.classList.add('hidden');
          navBtn.classList.remove('border-brand-600', 'text-brand-600');
          navBtn.classList.add('border-transparent', 'text-slate-500');
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
        clausesBtn.classList.add('text-brand-600', 'border-brand-600');
        clausesBtn.classList.remove('text-slate-500', 'border-transparent');
        checklistBtn.classList.remove('text-brand-600', 'border-brand-600');
        checklistBtn.classList.add('text-slate-500', 'border-transparent');
      } else {
        clausesView.classList.add('hidden');
        checklistView.classList.remove('hidden');
        checklistBtn.classList.add('text-brand-600', 'border-brand-600');
        checklistBtn.classList.remove('text-slate-500', 'border-transparent');
        clausesBtn.classList.remove('text-brand-600', 'border-brand-600');
        clausesBtn.classList.add('text-slate-500', 'border-transparent');
      }
    }

    // Fetch and cache samples on load
    async function initSamples() {
      try {
        const res = await fetch('/api/samples');
        if (res.ok) {
          cachedSamples = await res.json();
          // Load default high-risk sample
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
        alert(`Shield Preview: ${data.entities.length} sensitive items identified.\n` + 
              `Emails: ${data.entity_counts.EMAIL || 0}, Phones: ${data.entity_counts.PHONE || 0}, ` +
              `SSN/EIN: ${data.entity_counts.SSN_TAX_ID || 0}, Amounts: ${data.entity_counts.FINANCIAL || 0}`);
      } catch (e) {
        alert('Error testing PII redaction: ' + e);
      }
    }

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

      // Score and Level
      const index = data.risk_overview.legal_risk_index;
      document.getElementById('score-meter').innerText = index;
      const badge = document.getElementById('score-badge');
      badge.innerText = data.risk_overview.risk_level;
      if (index >= 75) {
        badge.className = 'px-3 py-1 text-xs font-bold rounded-full badge-high uppercase tracking-wide';
      } else if (index >= 45) {
        badge.className = 'px-3 py-1 text-xs font-bold rounded-full badge-medium uppercase tracking-wide';
      } else {
        badge.className = 'px-3 py-1 text-xs font-bold rounded-full badge-low uppercase tracking-wide';
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
        div.className = 'text-xs text-rose-700 bg-rose-50 border border-rose-200 px-2.5 py-1 rounded flex items-center gap-1.5';
        div.innerHTML = `<span>🚨</span> <strong>${finding}</strong>`;
        findingsContainer.appendChild(div);
      });

      // Render Clauses
      renderClauseCards(data.clauses);

      // Render Checklist
      renderAttorneyChecklist(data.attorney_checklist);

      // Update Privacy Vault
      renderPrivacyVault(data.anonymization);
    }

    function renderClauseCards(clauses) {
      const container = document.getElementById('clause-cards-view');
      container.innerHTML = '';

      clauses.forEach(clause => {
        const card = document.createElement('div');
        let severityBadge = '';
        if (clause.severity === 'HIGH' || clause.severity === 'CRITICAL') {
          severityBadge = '<span class="px-2 py-0.5 text-xs font-bold rounded badge-high">HIGH RISK</span>';
        } else if (clause.severity === 'MEDIUM') {
          severityBadge = '<span class="px-2 py-0.5 text-xs font-bold rounded badge-medium">MODERATE</span>';
        } else {
          severityBadge = '<span class="px-2 py-0.5 text-xs font-bold rounded badge-low">STANDARD</span>';
        }

        const trapsHtml = clause.detected_traps.map(t => 
          `<span class="inline-block bg-rose-100 text-rose-800 text-[10px] font-semibold px-2 py-0.5 rounded mr-1">⚠️ ${t}</span>`
        ).join('');

        card.className = 'bg-white rounded-xl shadow-sm border border-slate-200 p-5 space-y-3 clause-card';
        card.setAttribute('data-severity', clause.severity);

        card.innerHTML = `
          <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-100 pb-3">
            <div class="flex items-center gap-2">
              <span class="text-xs font-bold bg-slate-100 text-slate-700 px-2 py-0.5 rounded">#${clause.id}</span>
              <h4 class="text-sm font-bold text-slate-900">${clause.section_title}</h4>
            </div>
            <div class="flex items-center gap-2">
              <span class="text-xs font-semibold text-slate-500 uppercase tracking-wider">${clause.category.replace('_', ' ')}</span>
              ${severityBadge}
            </div>
          </div>

          ${trapsHtml ? `<div class="pt-1">${trapsHtml}</div>` : ''}

          <div class="grid grid-cols-1 md:grid-cols-2 gap-4 pt-1">
            <div class="space-y-2">
              <div class="text-xs font-bold uppercase tracking-wider text-slate-500">In Plain English:</div>
              <p class="text-xs text-slate-800 leading-relaxed bg-slate-50 p-2.5 rounded border border-slate-200">
                ${clause.plain_english_summary}
              </p>
              <div class="text-xs font-bold uppercase tracking-wider text-rose-700">What This Means For You:</div>
              <p class="text-xs text-rose-900 bg-rose-50/50 p-2.5 rounded border border-rose-200 leading-relaxed">
                ${clause.what_it_means_for_you}
              </p>
            </div>

            <div class="space-y-2">
              <div class="text-xs font-bold uppercase tracking-wider text-indigo-700">Negotiation Redline Tip:</div>
              <div class="text-xs text-indigo-950 bg-indigo-50/70 p-2.5 rounded border border-indigo-200 leading-relaxed">
                💡 ${clause.negotiation_tip}
              </div>
              <details class="text-xs text-slate-600">
                <summary class="cursor-pointer font-medium text-slate-500 hover:text-slate-800 py-1">View Original Contract Clause Text</summary>
                <pre class="mt-1 p-2 bg-slate-100 rounded text-[11px] font-mono whitespace-pre-wrap overflow-x-auto text-slate-700 max-h-36">${clause.original_text}</pre>
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
        if (level === 'ALL' || sev === level || (level === 'HIGH' && sev === 'CRITICAL')) {
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
        div.className = 'p-4 rounded-lg bg-slate-50 border border-slate-200 space-y-2';
        div.innerHTML = `
          <div class="flex items-center gap-2">
            <span class="text-xs font-bold text-brand-600 uppercase tracking-wide">Question ${i + 1}: ${q.category}</span>
          </div>
          <p class="text-xs font-bold text-slate-900 leading-snug">"${q.question}"</p>
          <p class="text-xs text-slate-600"><strong>Why It Matters:</strong> ${q.why_it_matters}</p>
          <p class="text-xs text-indigo-800 bg-white p-2 rounded border border-indigo-100 font-mono">
            <strong>Recommended Redline:</strong> ${q.recommended_fallback}
          </p>
        `;
        qList.appendChild(div);
      });

      const rList = document.getElementById('checklist-redlines-list');
      rList.innerHTML = '';
      checklist.priority_negotiation_items.forEach(item => {
        const li = document.createElement('li');
        li.className = 'flex items-start gap-2';
        li.innerHTML = `<span class="text-indigo-600 font-bold">☑</span> <span>${item}</span>`;
        rList.appendChild(li);
      });
    }

    function renderPrivacyVault(anon) {
      document.getElementById('privacy-total-redacted').innerText = anon.entities.length;
      document.getElementById('privacy-score-display').innerText = anon.privacy_score + '%';

      const tbody = document.getElementById('privacy-table-body');
      tbody.innerHTML = '';
      if (anon.entities.length === 0) {
        tbody.innerHTML = '<tr><td colspan="3" class="px-4 py-4 text-center text-slate-400">No PII identifiers detected in this document.</td></tr>';
        return;
      }

      anon.entities.forEach(ent => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
          <td class="px-4 py-2 font-medium text-slate-800">${ent.entity_type}</td>
          <td class="px-4 py-2 font-mono text-indigo-600">${ent.token}</td>
          <td class="px-4 py-2 font-mono text-slate-500">${ent.original_value}</td>
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
        badge.className = 'px-3 py-1 text-xs font-bold rounded-full badge-high uppercase';
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
        card.className = 'bg-white rounded-xl shadow-sm border border-slate-200 p-4 space-y-2';
        
        let typeBadge = '';
        if (diff.change_type === 'ADDED') typeBadge = '<span class="px-2 py-0.5 rounded text-xs font-bold bg-blue-100 text-blue-800">ADDED</span>';
        else if (diff.change_type === 'REMOVED') typeBadge = '<span class="px-2 py-0.5 rounded text-xs font-bold bg-rose-100 text-rose-800">REMOVED</span>';
        else if (diff.change_type === 'MODIFIED') typeBadge = '<span class="px-2 py-0.5 rounded text-xs font-bold bg-amber-100 text-amber-800">MODIFIED</span>';
        else typeBadge = '<span class="px-2 py-0.5 rounded text-xs font-bold bg-slate-100 text-slate-700">UNCHANGED</span>';

        card.innerHTML = `
          <div class="flex items-center justify-between border-b border-slate-100 pb-2">
            <h4 class="text-sm font-bold text-slate-900">${diff.section_title}</h4>
            <div class="flex items-center gap-2">
              <span class="text-xs text-slate-500 font-medium">${diff.category}</span>
              ${typeBadge}
            </div>
          </div>
          <p class="text-xs text-slate-700 font-medium">${diff.analysis_notes}</p>
          ${diff.text_v1 && diff.text_v2 && diff.change_type === 'MODIFIED' ? `
            <div class="grid grid-cols-1 md:grid-cols-2 gap-2 text-[11px] font-mono pt-1">
              <div class="bg-red-50 p-2 rounded border border-red-200 text-red-900 max-h-32 overflow-y-auto">
                <div class="font-bold mb-1">V1 Original:</div>${diff.text_v1}
              </div>
              <div class="bg-emerald-50 p-2 rounded border border-emerald-200 text-emerald-900 max-h-32 overflow-y-auto">
                <div class="font-bold mb-1">V2 Revision:</div>${diff.text_v2}
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
        appendChatMessage('assistant', data.answer, data.risk_warning, data.referenced_clauses);
      } catch (err) {
        appendChatMessage('assistant', 'Sorry, I encountered an issue processing your query: ' + err.message);
      }
    }

    function sendQuickPrompt(prompt) {
      document.getElementById('chat-input').value = prompt;
      handleChatSubmit(new Event('submit'));
    }

    function appendChatMessage(sender, text, warning, cited) {
      const container = document.getElementById('chat-messages');
      const div = document.createElement('div');
      
      if (sender === 'user') {
        div.className = 'ml-auto max-w-lg p-3 bg-brand-600 text-white rounded-lg shadow-xs text-xs';
        div.innerText = text;
      } else {
        div.className = 'mr-auto max-w-xl p-3.5 bg-white text-slate-800 rounded-lg border border-slate-200 shadow-xs space-y-2 text-xs leading-relaxed';
        let warningHtml = warning ? `<div class="p-2 bg-rose-50 border border-rose-200 text-rose-800 rounded font-bold">🚨 ${warning}</div>` : '';
        let citationsHtml = (cited && cited.length > 0) ? `<div class="text-[11px] text-slate-500 font-medium">Referenced Clauses: ${cited.join(', ')}</div>` : '';
        div.innerHTML = `
          ${warningHtml}
          <div class="whitespace-pre-wrap">${text.replace(/\\n/g, '<br>')}</div>
          ${citationsHtml}
        `;
      }
      container.appendChild(div);
      container.scrollTop = container.scrollHeight;
    }

    // Startup bootstrap
    window.addEventListener('DOMContentLoaded', () => {
      initSamples();
    });
  </script>
</body>
</html>
"""
