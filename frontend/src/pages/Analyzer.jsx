import { useState, useRef } from "react";
import {
  Send, Mic, MicOff, RefreshCw, AlertTriangle, CheckCircle,
  Copy, Sparkles, ChevronDown, ChevronUp, Trash2
} from "lucide-react";
import ToxicityMeter from "../components/ToxicityMeter";
import CategoryBadges from "../components/CategoryBadges";
import LoadingAnimation from "../components/LoadingAnimation";
import { predictToxicity, rewriteComment } from "../utils/api";

const SEVERITY_CONFIG = {
  safe:     { bg: "from-emerald-500/10 to-transparent", border: "border-emerald-500/20", icon: CheckCircle,   iconColor: "text-emerald-400", label: "✅ Safe Content"                      },
  mild:     { bg: "from-yellow-500/10 to-transparent",  border: "border-yellow-500/20",  icon: AlertTriangle, iconColor: "text-yellow-400",  label: "💬 Mildly Inappropriate"              },
  moderate: { bg: "from-orange-500/10 to-transparent",  border: "border-orange-500/20",  icon: AlertTriangle, iconColor: "text-orange-400",  label: "⚠️ Moderate Toxicity"                 },
  high:     { bg: "from-red-500/10 to-transparent",     border: "border-red-500/20",     icon: AlertTriangle, iconColor: "text-red-400",     label: "🚨 High Toxicity Detected"            },
  severe:   { bg: "from-red-900/20 to-transparent",     border: "border-red-700/40",     icon: AlertTriangle, iconColor: "text-red-500",     label: "🚨 Extremely Toxic — Do Not Send"     },
};

const EXAMPLES = [
  "I love how you explained that concept — really helpful!",
  "You absolute moron, nobody likes you here.",
  "I disagree with your point but I think there's merit in both sides.",
  "Watch your back. You'll regret this.",
  "Everyone from that place is so stupid and useless.",
];

export default function Analyzer() {
  const [text, setText]           = useState("");
  const [result, setResult]       = useState(null);
  const [loading, setLoading]     = useState(false);
  const [error, setError]         = useState(null);
  const [rewrite, setRewrite]     = useState(null);
  const [rewriting, setRewriting] = useState(false);
  const [listening, setListening] = useState(false);
  const [showRaw, setShowRaw]     = useState(false);
  const [copied, setCopied]       = useState(false);
  const recognitionRef = useRef(null);

  const analyze = async () => {
    if (!text.trim()) return;
    setLoading(true); setError(null); setResult(null); setRewrite(null);
    try {
      const data = await predictToxicity(text);
      setResult(data);
    } catch (e) {
      setError(e.response?.data?.error || "API unreachable — is the backend running?");
    } finally {
      setLoading(false);
    }
  };

  const handleRewrite = async () => {
    setRewriting(true);
    try {
      const data = await rewriteComment(text);
      setRewrite(data.rewritten);
    } catch {
      setRewrite("Sorry, could not generate a rewrite right now.");
    } finally {
      setRewriting(false);
    }
  };

  const toggleVoice = () => {
    const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SR) { alert("Voice input not supported in this browser."); return; }
    if (listening) {
      recognitionRef.current?.stop(); setListening(false); return;
    }
    const r = new SR(); r.lang = "en-US"; r.continuous = false;
    r.onresult = (e) => setText(e.results[0][0].transcript);
    r.onend    = () => setListening(false);
    recognitionRef.current = r;
    r.start(); setListening(true);
  };

  const copyResult = () => {
    if (!result) return;
    navigator.clipboard.writeText(JSON.stringify(result, null, 2));
    setCopied(true); setTimeout(() => setCopied(false), 1500);
  };

  const sev = result?.severity || "safe";
  const cfg = SEVERITY_CONFIG[sev] || SEVERITY_CONFIG.safe;

  return (
    <main className="max-w-4xl mx-auto px-4 sm:px-6 py-10 space-y-6">
      <div className="text-center space-y-2">
        <h1 className="font-display text-4xl font-extrabold text-white">Toxicity Analyzer</h1>
        <p className="text-gray-400 text-sm">Enter any comment to get a full ML-powered toxicity breakdown.</p>
      </div>

      {/* Input card */}
      <div className="card p-5 space-y-4">
        <div className="flex items-center justify-between mb-1">
          <span className="text-xs text-gray-500 font-mono">COMMENT INPUT</span>
          <div className="flex gap-2">
            {/* Example selector */}
            <select
              className="text-xs bg-gray-800 border border-gray-700 rounded-lg px-2 py-1 text-gray-400 cursor-pointer"
              onChange={(e) => setText(e.target.value)}
              defaultValue=""
            >
              <option value="" disabled>Load example…</option>
              {EXAMPLES.map((ex, i) => (
                <option key={i} value={ex}>{ex.slice(0, 45)}…</option>
              ))}
            </select>
            <button onClick={() => { setText(""); setResult(null); setRewrite(null); }}
              className="p-1.5 rounded-lg text-gray-500 hover:text-red-400 hover:bg-red-500/10 transition-colors">
              <Trash2 size={14} />
            </button>
          </div>
        </div>
        <textarea
          value={text}
          onChange={(e) => setText(e.target.value)}
          onKeyDown={(e) => { if (e.key === "Enter" && e.ctrlKey) analyze(); }}
          placeholder="Type or paste a comment here… (Ctrl+Enter to analyze)"
          rows={5}
          maxLength={5000}
          className="w-full bg-gray-900/60 border border-gray-700 rounded-xl p-4 text-gray-200 placeholder-gray-600 text-sm resize-none focus:outline-none focus:border-cyan-500/60 transition-colors font-mono"
        />
        <div className="flex items-center justify-between">
          <span className="text-xs text-gray-600 font-mono">{text.length}/5000</span>
          <div className="flex gap-2">
            <button
              onClick={toggleVoice}
              className={`p-2 rounded-xl border transition-all ${listening ? "border-red-500/50 bg-red-500/10 text-red-400" : "border-gray-700 text-gray-500 hover:border-gray-500"}`}
              title="Voice input"
            >
              {listening ? <MicOff size={16} /> : <Mic size={16} />}
            </button>
            <button
              onClick={analyze}
              disabled={!text.trim() || loading}
              className="flex items-center gap-2 px-5 py-2 rounded-xl bg-gradient-to-r from-cyan-500 to-emerald-500 text-gray-900 font-semibold text-sm disabled:opacity-40 disabled:cursor-not-allowed hover:opacity-90 transition-opacity"
            >
              <Send size={14} /> Analyze
            </button>
          </div>
        </div>
      </div>

      {/* Loading */}
      {loading && <div className="card"><LoadingAnimation /></div>}

      {/* Error */}
      {error && (
        <div className="card p-4 border-red-500/30 bg-red-500/5">
          <p className="text-red-400 text-sm flex items-center gap-2">
            <AlertTriangle size={16} /> {error}
          </p>
        </div>
      )}

      {/* Results */}
      {result && !loading && (
        <div className={`card p-6 space-y-6 bg-gradient-to-b ${cfg.bg} border ${cfg.border} fade-in-up`}>
          {/* Header row */}
          <div className="flex items-center justify-between flex-wrap gap-4">
            <div className="flex items-center gap-3">
              <cfg.icon size={22} className={cfg.iconColor} />
              <div>
                <div className="font-display font-bold text-white">{cfg.label}</div>
                <div className="text-xs text-gray-500 font-mono mt-0.5 capitalize">
                  Sentiment: {result.sentiment} · Model: {result.model_used}
                </div>
              </div>
            </div>
            <ToxicityMeter score={result.toxicity_score} size="lg" />
          </div>

          {/* Warning banner */}
          {result.warning && (
            <div className="rounded-xl p-3 bg-red-500/10 border border-red-500/20 text-sm text-red-300">
              {result.warning}
            </div>
          )}

          {/* Category breakdown */}
          <div>
            <div className="text-xs text-gray-500 font-mono uppercase tracking-wider mb-3">Category Breakdown</div>
            <CategoryBadges categories={result.categories} />
          </div>

          {/* Actions */}
          <div className="flex flex-wrap gap-2 pt-2 border-t border-gray-800">
            {result.is_toxic && (
              <button
                onClick={handleRewrite}
                disabled={rewriting}
                className="flex items-center gap-2 px-4 py-2 rounded-xl bg-cyan-500/10 border border-cyan-500/20 text-cyan-400 text-sm hover:bg-cyan-500/20 transition-colors disabled:opacity-50"
              >
                {rewriting ? <RefreshCw size={14} className="animate-spin" /> : <Sparkles size={14} />}
                {rewriting ? "Rewriting…" : "Suggest Polite Alternative"}
              </button>
            )}
            <button
              onClick={copyResult}
              className="flex items-center gap-2 px-4 py-2 rounded-xl bg-gray-800 border border-gray-700 text-gray-400 text-sm hover:text-gray-200 transition-colors"
            >
              <Copy size={14} /> {copied ? "Copied!" : "Copy JSON"}
            </button>
            <button
              onClick={() => setShowRaw(s => !s)}
              className="flex items-center gap-2 px-4 py-2 rounded-xl bg-gray-800 border border-gray-700 text-gray-400 text-sm hover:text-gray-200 transition-colors ml-auto"
            >
              {showRaw ? <ChevronUp size={14} /> : <ChevronDown size={14} />}
              Raw JSON
            </button>
          </div>

          {/* Rewrite suggestion */}
          {rewrite && (
            <div className="rounded-xl p-4 bg-emerald-500/8 border border-emerald-500/20 fade-in-up space-y-1">
              <div className="text-xs text-emerald-400 font-mono uppercase tracking-wider flex items-center gap-1.5">
                <Sparkles size={11} /> Suggested Rephrasing
              </div>
              <p className="text-sm text-gray-200 leading-relaxed">{rewrite}</p>
            </div>
          )}

          {/* Raw JSON */}
          {showRaw && (
            <pre className="text-xs text-gray-400 bg-gray-900 rounded-xl p-4 overflow-auto font-mono border border-gray-800 max-h-64 fade-in-up">
              {JSON.stringify(result, null, 2)}
            </pre>
          )}
        </div>
      )}
    </main>
  );
}
