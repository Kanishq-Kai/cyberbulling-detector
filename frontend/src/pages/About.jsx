import { Github, Database, Cpu, Layers, Code2, BookOpen } from "lucide-react";

const STACK = [
  { layer: "Frontend",    items: ["React 18",   "Tailwind CSS",   "Recharts",        "React Router"],  color: "#00E5FF" },
  { layer: "Backend",     items: ["Python Flask","Flask-CORS",     "PyMongo",         "Gunicorn"],       color: "#00D68F" },
  { layer: "ML / NLP",    items: ["Scikit-learn","NLTK",           "Pandas / NumPy",  "Joblib"],         color: "#FF8C00" },
  { layer: "Database",    items: ["MongoDB",     "PyMongo driver", "Atlas (optional)","JSON schemas"],   color: "#9333EA" },
];

const PIPELINE = [
  { step: "1", title: "Raw Input",          desc: "User submits a comment via the web interface." },
  { step: "2", title: "Text Preprocessing", desc: "Lowercase, URL removal, HTML stripping, punctuation removal." },
  { step: "3", title: "Tokenization",       desc: "NLTK word_tokenize splits text into tokens." },
  { step: "4", title: "Stopword Removal",   desc: "Common words (the, is, a…) removed from token list." },
  { step: "5", title: "Lemmatization",      desc: "WordNetLemmatizer normalises word forms (running→run)." },
  { step: "6", title: "TF-IDF Vectorization","desc": "Tokens converted to 50K-feature TF-IDF matrix." },
  { step: "7", title: "Model Inference",    desc: "6 Logistic Regression classifiers output per-category probabilities." },
  { step: "8", title: "Response & Storage", desc: "Result returned via API; record persisted to MongoDB." },
];

export default function About() {
  return (
    <main className="max-w-5xl mx-auto px-4 sm:px-6 py-12 space-y-16">
      {/* Hero */}
      <section className="text-center space-y-4">
        <h1 className="font-display text-4xl font-extrabold text-white">About ToxShield</h1>
        <p className="text-gray-400 max-w-2xl mx-auto leading-relaxed">
          A final-year AI/ML project demonstrating an end-to-end machine learning system for
          cyberbullying and hate speech detection. Built with a focus on accuracy, explainability,
          and a production-quality user experience.
        </p>
      </section>

      {/* NLP Pipeline */}
      <section className="space-y-6">
        <div className="flex items-center gap-3">
          <Cpu size={20} className="text-cyan-400" />
          <h2 className="font-display text-2xl font-bold text-white">NLP Processing Pipeline</h2>
        </div>
        <div className="relative">
          {/* Vertical line */}
          <div className="absolute left-5 top-6 bottom-6 w-px bg-gradient-to-b from-cyan-500/50 to-transparent hidden sm:block" />
          <div className="space-y-4">
            {PIPELINE.map(({ step, title, desc }) => (
              <div key={step} className="card card-hover p-4 sm:pl-16 relative">
                <div className="absolute left-3 top-1/2 -translate-y-1/2 hidden sm:flex w-5 h-5 rounded-full bg-cyan-500/20 border border-cyan-500/40 items-center justify-center">
                  <span className="text-xs text-cyan-400 font-mono font-bold">{step}</span>
                </div>
                <div className="font-semibold text-white text-sm">{title}</div>
                <div className="text-xs text-gray-400 mt-0.5">{desc}</div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Tech Stack */}
      <section className="space-y-6">
        <div className="flex items-center gap-3">
          <Layers size={20} className="text-cyan-400" />
          <h2 className="font-display text-2xl font-bold text-white">Tech Stack</h2>
        </div>
        <div className="grid sm:grid-cols-2 gap-4">
          {STACK.map(({ layer, items, color }) => (
            <div key={layer} className="card p-5 space-y-3">
              <div className="flex items-center gap-2">
                <span className="w-2 h-2 rounded-full" style={{ background: color }} />
                <span className="font-semibold text-sm text-white">{layer}</span>
              </div>
              <div className="flex flex-wrap gap-2">
                {items.map(item => (
                  <span key={item}
                    className="text-xs px-2.5 py-1 rounded-full font-mono"
                    style={{ background: `${color}12`, color, border: `1px solid ${color}30` }}>
                    {item}
                  </span>
                ))}
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* Model info */}
      <section className="space-y-5">
        <div className="flex items-center gap-3">
          <Database size={20} className="text-cyan-400" />
          <h2 className="font-display text-2xl font-bold text-white">Model & Dataset</h2>
        </div>
        <div className="card p-6 space-y-4 text-sm text-gray-300 leading-relaxed">
          <p><span className="text-cyan-400 font-mono font-semibold">Dataset:</span> Jigsaw Toxic Comment Classification Challenge (Kaggle) — ~160,000 Wikipedia talk-page comments, multi-label annotated.</p>
          <p><span className="text-cyan-400 font-mono font-semibold">Algorithm:</span> One-vs-Rest Logistic Regression with L2 regularisation per category. Class-weight balancing handles the label imbalance (toxic comments are ~10% of data).</p>
          <p><span className="text-cyan-400 font-mono font-semibold">Vectorization:</span> TF-IDF with 50,000 features, unigrams + bigrams, sublinear TF scaling.</p>
          <p><span className="text-cyan-400 font-mono font-semibold">Metrics:</span> ROC-AUC typically reaches 0.97–0.98 for the main "toxic" category. F1-score varies per category due to class imbalance.</p>
          <p><span className="text-cyan-400 font-mono font-semibold">Persistence:</span> Models serialised with Joblib to <code className="text-yellow-400 bg-gray-800 px-1 rounded">.pkl</code> files. Loaded once at API startup for fast inference.</p>
        </div>
      </section>

      {/* Links */}
      <section className="card p-6 text-center space-y-4 border-cyan-500/20">
        <h2 className="font-display font-bold text-white text-xl">Resources</h2>
        <div className="flex flex-wrap justify-center gap-3">
          {[
            { href: "https://www.kaggle.com/c/jigsaw-toxic-comment-classification-challenge", label: "Jigsaw Dataset", Icon: Database },
            { href: "https://scikit-learn.org",   label: "Scikit-learn Docs", Icon: BookOpen },
            { href: "https://flask.palletsprojects.com", label: "Flask Docs", Icon: Code2 },
          ].map(({ href, label, Icon }) => (
            <a key={label} href={href} target="_blank" rel="noopener noreferrer"
              className="flex items-center gap-2 px-4 py-2 rounded-xl border border-gray-700 text-gray-400 hover:text-cyan-400 hover:border-cyan-500/40 text-sm transition-colors">
              <Icon size={14} /> {label}
            </a>
          ))}
        </div>
      </section>
    </main>
  );
}
