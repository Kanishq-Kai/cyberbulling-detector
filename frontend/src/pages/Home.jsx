import { Link } from "react-router-dom";
import { Shield, Zap, BarChart2, RefreshCw, ArrowRight, Cpu, Globe, Lock } from "lucide-react";

const FEATURES = [
  { Icon: Zap,       title: "Real-Time Analysis",   desc: "Instant toxicity scoring powered by NLP + ML as you type." },
  { Icon: BarChart2, title: "6 Toxic Categories",   desc: "Detects Toxic, Severe Toxic, Insult, Threat, Obscene, Hate Speech." },
  { Icon: RefreshCw, title: "Smart Rephrasing",     desc: "AI suggests a polite, constructive alternative for toxic comments." },
  { Icon: Cpu,       title: "ML-Powered Model",     desc: "Trained on Jigsaw dataset with TF-IDF + Logistic Regression." },
  { Icon: Globe,     title: "Analytics Dashboard",  desc: "Live pie charts, bar graphs, and trend analysis." },
  { Icon: Lock,      title: "Privacy First",        desc: "No user accounts required. Data anonymised by default." },
];

const STATS = [
  { value: "160K+", label: "Training Samples" },
  { value: "6",     label: "Toxic Categories" },
  { value: "95%",   label: "AUC-ROC Score" },
  { value: "<200ms",label: "Avg Response Time" },
];

export default function Home() {
  return (
    <main className="max-w-7xl mx-auto px-4 sm:px-6 py-12 space-y-24">

      {/* Hero */}
      <section className="text-center space-y-7 py-10">
        <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full border border-cyan-500/30 bg-cyan-500/5 text-xs text-cyan-400 font-mono mb-2">
          <span className="w-1.5 h-1.5 rounded-full bg-cyan-400 pulse-dot" />
          AI-Powered Safety System v1.0
        </div>
        <h1 className="font-display text-5xl sm:text-6xl md:text-7xl font-extrabold leading-tight tracking-tight">
          Detect Toxic Content<br />
          <span className="gradient-text">Before It Spreads</span>
        </h1>
        <p className="text-gray-400 text-lg max-w-2xl mx-auto leading-relaxed">
          An end-to-end machine learning system that classifies cyberbullying, hate speech,
          threats, and abusive language with confidence scores in real time.
        </p>
        <div className="flex flex-wrap items-center justify-center gap-3">
          <Link
            to="/analyzer"
            className="inline-flex items-center gap-2 px-7 py-3.5 rounded-xl bg-gradient-to-r from-cyan-500 to-emerald-500 text-gray-900 font-semibold hover:opacity-90 transition-opacity shadow-lg shadow-cyan-500/20"
          >
            Try the Analyzer <ArrowRight size={16} />
          </Link>
          <Link
            to="/dashboard"
            className="inline-flex items-center gap-2 px-7 py-3.5 rounded-xl border border-gray-700 text-gray-300 hover:border-gray-500 hover:text-white transition-colors"
          >
            View Dashboard <BarChart2 size={16} />
          </Link>
        </div>
      </section>

      {/* Stats */}
      <section className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {STATS.map(({ value, label }) => (
          <div key={label} className="card p-6 text-center glow-cyan">
            <div className="font-display text-3xl font-extrabold gradient-text">{value}</div>
            <div className="text-xs text-gray-500 mt-1 font-mono">{label}</div>
          </div>
        ))}
      </section>

      {/* Features grid */}
      <section className="space-y-8">
        <div className="text-center">
          <h2 className="font-display text-3xl font-bold text-white">What ToxShield Does</h2>
          <p className="text-gray-500 mt-2">A complete ML pipeline from raw text to actionable insights.</p>
        </div>
        <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-5">
          {FEATURES.map(({ Icon, title, desc }) => (
            <div key={title} className="card card-hover p-6 space-y-3">
              <div className="w-10 h-10 rounded-xl bg-cyan-500/10 flex items-center justify-center">
                <Icon size={18} className="text-cyan-400" />
              </div>
              <h3 className="font-display font-semibold text-white">{title}</h3>
              <p className="text-sm text-gray-400 leading-relaxed">{desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* CTA */}
      <section className="card p-10 text-center space-y-5 border-cyan-500/20 bg-gradient-to-br from-cyan-500/5 to-emerald-500/5">
        <Shield size={40} className="mx-auto text-cyan-400" />
        <h2 className="font-display text-3xl font-bold text-white">Ready to Analyze?</h2>
        <p className="text-gray-400 max-w-md mx-auto">
          Paste any comment and get a full toxicity breakdown with category scores, sentiment, and polite rephrasing.
        </p>
        <Link
          to="/analyzer"
          className="inline-flex items-center gap-2 px-8 py-3.5 rounded-xl bg-gradient-to-r from-cyan-500 to-emerald-500 text-gray-900 font-semibold hover:opacity-90 transition-opacity"
        >
          Open Analyzer <ArrowRight size={16} />
        </Link>
      </section>

    </main>
  );
}
