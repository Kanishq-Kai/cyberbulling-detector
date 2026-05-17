export default function LoadingAnimation() {
  return (
    <div className="flex flex-col items-center justify-center py-12 gap-5">
      {/* Orbital spinner */}
      <div className="relative w-16 h-16">
        <div className="absolute inset-0 rounded-full border-2 border-gray-800" />
        <div className="absolute inset-0 rounded-full border-2 border-transparent border-t-cyan-400 animate-spin" />
        <div className="absolute inset-2 rounded-full border-2 border-transparent border-b-emerald-400 animate-spin" style={{ animationDuration: "0.7s", animationDirection: "reverse" }} />
        <div className="absolute inset-0 flex items-center justify-center">
          <div className="w-2 h-2 rounded-full bg-cyan-400 animate-pulse" />
        </div>
      </div>
      <div className="text-center space-y-1">
        <p className="text-sm text-gray-300 font-medium">Analyzing comment…</p>
        <p className="text-xs text-gray-500 font-mono">Running NLP pipeline</p>
      </div>
      {/* Fake progress bar */}
      <div className="w-48 h-0.5 bg-gray-800 rounded-full overflow-hidden">
        <div className="h-full bg-gradient-to-r from-cyan-400 to-emerald-400 rounded-full animate-pulse" style={{ width: "70%" }} />
      </div>
    </div>
  );
}
