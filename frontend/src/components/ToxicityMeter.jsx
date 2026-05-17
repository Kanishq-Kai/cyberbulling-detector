export default function ToxicityMeter({ score = 0, size = "md" }) {
  const pct = Math.round(score * 100);

  const color =
    pct < 15 ? "#00D68F" :
    pct < 40 ? "#A3E635" :
    pct < 65 ? "#FF8C00" :
    pct < 85 ? "#FF3B3B" :
               "#CC0000";

  const label =
    pct < 15 ? "Safe" :
    pct < 40 ? "Mild" :
    pct < 65 ? "Moderate" :
    pct < 85 ? "High" :
               "Severe";

  const radius = size === "lg" ? 70 : 50;
  const stroke = size === "lg" ? 8  : 6;
  const viewBox = (radius + stroke) * 2;
  const cx = radius + stroke;
  const cy = radius + stroke;
  const circumference = 2 * Math.PI * radius;
  const dashOffset = circumference - (pct / 100) * circumference;

  return (
    <div className="flex flex-col items-center gap-2">
      <div className="relative" style={{ width: viewBox, height: viewBox }}>
        <svg width={viewBox} height={viewBox} viewBox={`0 0 ${viewBox} ${viewBox}`}>
          {/* Track */}
          <circle
            cx={cx} cy={cy} r={radius}
            fill="none" stroke="#1F2937" strokeWidth={stroke}
          />
          {/* Fill */}
          <circle
            cx={cx} cy={cy} r={radius}
            fill="none"
            stroke={color}
            strokeWidth={stroke}
            strokeLinecap="round"
            strokeDasharray={circumference}
            strokeDashoffset={dashOffset}
            transform={`rotate(-90 ${cx} ${cy})`}
            style={{ transition: "stroke-dashoffset 0.8s cubic-bezier(0.34,1.56,0.64,1)", filter: `drop-shadow(0 0 6px ${color}80)` }}
          />
        </svg>
        {/* Center text */}
        <div className="absolute inset-0 flex flex-col items-center justify-center">
          <span className="font-display font-bold" style={{ color, fontSize: size === "lg" ? 28 : 20 }}>
            {pct}%
          </span>
          {size === "lg" && (
            <span className="text-xs text-gray-400 mt-0.5 font-mono">{label}</span>
          )}
        </div>
      </div>
      {size !== "lg" && (
        <span className="text-xs font-mono font-medium" style={{ color }}>{label}</span>
      )}
    </div>
  );
}
