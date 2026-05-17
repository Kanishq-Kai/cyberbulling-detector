const CAT_META = {
  toxic:        { label: "Toxic",        color: "#FF3B3B", bg: "rgba(255,59,59,0.1)"  },
  severe_toxic: { label: "Severe Toxic", color: "#CC0000", bg: "rgba(204,0,0,0.12)"   },
  insult:       { label: "Insult",       color: "#FF8C00", bg: "rgba(255,140,0,0.1)"  },
  threat:       { label: "Threat",       color: "#DC2626", bg: "rgba(220,38,38,0.12)" },
  obscene:      { label: "Obscene",      color: "#9333EA", bg: "rgba(147,51,234,0.1)" },
  hate_speech:  { label: "Hate Speech",  color: "#F97316", bg: "rgba(249,115,22,0.1)" },
};

export default function CategoryBadges({ categories = {}, threshold = 0.35 }) {
  const entries = Object.entries(categories).sort((a, b) => b[1] - a[1]);

  return (
    <div className="space-y-2">
      {entries.map(([key, val]) => {
        const meta  = CAT_META[key] || { label: key, color: "#6B7280", bg: "rgba(107,114,128,0.1)" };
        const pct   = Math.round(val * 100);
        const flagged = val >= threshold;

        return (
          <div key={key} className="flex items-center gap-3">
            <div className="w-28 shrink-0 flex items-center gap-1.5">
              {flagged && (
                <span className="w-1.5 h-1.5 rounded-full pulse-dot" style={{ background: meta.color }} />
              )}
              <span className="text-xs text-gray-300 font-mono">{meta.label}</span>
            </div>
            <div className="flex-1 h-1.5 bg-gray-800 rounded-full overflow-hidden">
              <div
                className="h-full rounded-full transition-all duration-700"
                style={{ width: `${pct}%`, background: meta.color, boxShadow: flagged ? `0 0 6px ${meta.color}80` : "none" }}
              />
            </div>
            <span
              className="text-xs font-mono w-10 text-right font-semibold"
              style={{ color: flagged ? meta.color : "#6B7280" }}
            >
              {pct}%
            </span>
          </div>
        );
      })}
    </div>
  );
}
