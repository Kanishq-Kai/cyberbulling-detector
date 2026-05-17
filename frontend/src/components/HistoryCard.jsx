import { Clock, AlertTriangle, CheckCircle } from "lucide-react";

const SEVERITY_STYLES = {
  safe:     { bg: "rgba(0,214,143,0.08)",  border: "rgba(0,214,143,0.2)",  text: "#00D68F" },
  mild:     { bg: "rgba(163,230,53,0.08)", border: "rgba(163,230,53,0.2)", text: "#A3E635" },
  moderate: { bg: "rgba(255,140,0,0.08)",  border: "rgba(255,140,0,0.2)",  text: "#FF8C00" },
  high:     { bg: "rgba(255,59,59,0.08)",  border: "rgba(255,59,59,0.2)",  text: "#FF3B3B" },
  severe:   { bg: "rgba(204,0,0,0.1)",     border: "rgba(204,0,0,0.3)",    text: "#CC0000" },
};

export default function HistoryCard({ comment }) {
  const sev  = comment.severity || (comment.is_toxic ? "high" : "safe");
  const styl = SEVERITY_STYLES[sev] || SEVERITY_STYLES.safe;
  const pct  = Math.round((comment.toxicity_score || 0) * 100);

  const timeAgo = (iso) => {
    const diff = Date.now() - new Date(iso);
    const mins = Math.floor(diff / 60000);
    if (mins < 1) return "just now";
    if (mins < 60) return `${mins}m ago`;
    const hrs = Math.floor(mins / 60);
    if (hrs < 24) return `${hrs}h ago`;
    return `${Math.floor(hrs / 24)}d ago`;
  };

  return (
    <div
      className="card card-hover p-4 fade-in-up"
      style={{ borderColor: styl.border, background: styl.bg }}
    >
      <div className="flex items-start justify-between gap-3">
        <div className="flex-1 min-w-0">
          <p className="text-sm text-gray-200 line-clamp-2 leading-relaxed">
            {comment.text}
          </p>
          <div className="flex items-center gap-3 mt-2 flex-wrap">
            <span className="flex items-center gap-1 text-xs text-gray-500">
              <Clock size={11} />
              {timeAgo(comment.created_at)}
            </span>
            <span className="text-xs font-mono" style={{ color: styl.text }}>
              {pct}% toxic
            </span>
            <span className="text-xs text-gray-500 capitalize">
              {comment.sentiment}
            </span>
          </div>
        </div>
        <div className="shrink-0 flex flex-col items-center gap-1">
          {comment.is_toxic
            ? <AlertTriangle size={18} style={{ color: styl.text }} />
            : <CheckCircle   size={18} className="text-emerald-400" />
          }
          <span className="text-xs font-mono capitalize" style={{ color: styl.text }}>
            {sev}
          </span>
        </div>
      </div>
    </div>
  );
}
