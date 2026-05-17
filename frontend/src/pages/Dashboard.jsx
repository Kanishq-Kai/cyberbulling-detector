import { useState, useEffect } from "react";
import {
  PieChart, Pie, Cell, Tooltip, ResponsiveContainer,
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Legend,
  LineChart, Line, Area, AreaChart
} from "recharts";
import { getAnalytics, getHistory } from "../utils/api";
import HistoryCard from "../components/HistoryCard";
import { RefreshCw, TrendingUp, TrendingDown, MessageCircle, AlertTriangle, CheckCircle, Shield } from "lucide-react";

const PIE_COLORS = ["#FF3B3B","#CC0000","#FF8C00","#DC2626","#9333EA","#F97316"];
const SEVERITY_COLORS = { safe:"#00D68F", mild:"#A3E635", moderate:"#FF8C00", high:"#FF3B3B", severe:"#CC0000" };

const StatCard = ({ label, value, sub, Icon, color }) => (
  <div className="card p-5 space-y-3">
    <div className="flex items-center justify-between">
      <span className="text-xs text-gray-500 font-mono uppercase tracking-wider">{label}</span>
      <div className="w-8 h-8 rounded-lg flex items-center justify-center" style={{ background: `${color}15` }}>
        <Icon size={15} style={{ color }} />
      </div>
    </div>
    <div className="font-display text-3xl font-extrabold" style={{ color }}>{value}</div>
    {sub && <div className="text-xs text-gray-500">{sub}</div>}
  </div>
);

const CustomTooltip = ({ active, payload, label }) => {
  if (!active || !payload?.length) return null;
  return (
    <div className="bg-gray-900 border border-gray-700 rounded-xl p-3 text-xs shadow-xl">
      <p className="text-gray-400 mb-1">{label}</p>
      {payload.map((p, i) => (
        <p key={i} style={{ color: p.color }}>{p.name}: {p.value}</p>
      ))}
    </div>
  );
};

export default function Dashboard() {
  const [analytics, setAnalytics] = useState(null);
  const [history,   setHistory]   = useState([]);
  const [loading,   setLoading]   = useState(true);
  const [error,     setError]     = useState(null);

  const load = async () => {
    setLoading(true); setError(null);
    try {
      const [a, h] = await Promise.all([getAnalytics(), getHistory(1, 10)]);
      setAnalytics(a);
      setHistory(h.comments || []);
    } catch (e) {
      setError("Could not load analytics — is the backend running?");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { load(); }, []);

  if (loading) return (
    <div className="flex items-center justify-center min-h-[60vh]">
      <RefreshCw size={24} className="text-cyan-400 animate-spin" />
    </div>
  );

  if (error) return (
    <div className="max-w-4xl mx-auto px-4 py-12 text-center space-y-4">
      <AlertTriangle size={40} className="text-red-400 mx-auto" />
      <p className="text-red-400">{error}</p>
      <button onClick={load} className="px-5 py-2 rounded-xl border border-gray-700 text-gray-400 hover:text-white transition-colors text-sm">
        Retry
      </button>
    </div>
  );

  // Build chart data
  const catData = Object.entries(analytics?.category_dist || {}).map(([k, v]) => ({
    name: k.replace("_", " "),
    value: v,
  }));

  const sevData = Object.entries(analytics?.severity_dist || {}).map(([k, v]) => ({
    name: k,
    count: v,
    fill: SEVERITY_COLORS[k] || "#6B7280",
  }));

  const sentData = Object.entries(analytics?.sentiment_dist || {}).map(([k, v]) => ({
    name: k,
    value: v,
  }));

  const trend = analytics?.daily_trend || [];

  const pieOverall = [
    { name: "Toxic", value: analytics?.toxic || 0 },
    { name: "Safe",  value: analytics?.safe  || 0 },
  ];

  return (
    <main className="max-w-7xl mx-auto px-4 sm:px-6 py-10 space-y-8">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="font-display text-3xl font-extrabold text-white">Analytics Dashboard</h1>
          <p className="text-gray-500 text-sm mt-1">Real-time toxicity monitoring & insights</p>
        </div>
        <button onClick={load}
          className="flex items-center gap-2 px-4 py-2 rounded-xl border border-gray-700 text-gray-400 hover:text-white text-sm transition-colors">
          <RefreshCw size={14} /> Refresh
        </button>
      </div>

      {/* KPI row */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard label="Total Analyzed" value={analytics?.total ?? 0}        Icon={MessageCircle} color="#00E5FF" sub="All time"                          />
        <StatCard label="Toxic Comments" value={analytics?.toxic ?? 0}        Icon={AlertTriangle} color="#FF3B3B" sub={`${analytics?.toxic_rate ?? 0}% of total`} />
        <StatCard label="Safe Comments"  value={analytics?.safe  ?? 0}        Icon={CheckCircle}   color="#00D68F" sub="Passed moderation"                 />
        <StatCard label="Toxic Rate"     value={`${analytics?.toxic_rate ?? 0}%`} Icon={Shield}    color="#FF8C00" sub="Higher = more toxic traffic"       />
      </div>

      {/* Charts row 1 */}
      <div className="grid lg:grid-cols-3 gap-5">
        {/* Overall pie */}
        <div className="card p-5 space-y-3">
          <div className="text-xs text-gray-500 font-mono uppercase tracking-wider">Toxic vs Safe</div>
          <ResponsiveContainer width="100%" height={200}>
            <PieChart>
              <Pie data={pieOverall} cx="50%" cy="50%" innerRadius={55} outerRadius={80} paddingAngle={3} dataKey="value">
                <Cell fill="#FF3B3B" />
                <Cell fill="#00D68F" />
              </Pie>
              <Tooltip content={<CustomTooltip />} />
            </PieChart>
          </ResponsiveContainer>
          <div className="flex justify-center gap-4">
            {pieOverall.map((d, i) => (
              <div key={d.name} className="flex items-center gap-1.5 text-xs text-gray-400">
                <span className="w-2 h-2 rounded-full" style={{ background: i === 0 ? "#FF3B3B" : "#00D68F" }} />
                {d.name}: {d.value}
              </div>
            ))}
          </div>
        </div>

        {/* Category distribution */}
        <div className="card p-5 space-y-3 lg:col-span-2">
          <div className="text-xs text-gray-500 font-mono uppercase tracking-wider">Category Distribution</div>
          <ResponsiveContainer width="100%" height={200}>
            <BarChart data={catData} margin={{ top: 5, right: 10, left: -20, bottom: 5 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#1F2937" />
              <XAxis dataKey="name" tick={{ fill: "#6B7280", fontSize: 10 }} />
              <YAxis tick={{ fill: "#6B7280", fontSize: 10 }} />
              <Tooltip content={<CustomTooltip />} />
              <Bar dataKey="value" radius={[4,4,0,0]}>
                {catData.map((_, i) => <Cell key={i} fill={PIE_COLORS[i % PIE_COLORS.length]} />)}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Charts row 2 */}
      <div className="grid lg:grid-cols-2 gap-5">
        {/* Daily trend */}
        <div className="card p-5 space-y-3">
          <div className="text-xs text-gray-500 font-mono uppercase tracking-wider">7-Day Comment Trend</div>
          <ResponsiveContainer width="100%" height={200}>
            <AreaChart data={trend}>
              <defs>
                <linearGradient id="trendGrad" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%"  stopColor="#00E5FF" stopOpacity={0.3} />
                  <stop offset="95%" stopColor="#00E5FF" stopOpacity={0}   />
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="#1F2937" />
              <XAxis dataKey="date" tick={{ fill: "#6B7280", fontSize: 10 }} />
              <YAxis tick={{ fill: "#6B7280", fontSize: 10 }} />
              <Tooltip content={<CustomTooltip />} />
              <Area type="monotone" dataKey="count" stroke="#00E5FF" strokeWidth={2} fill="url(#trendGrad)" name="Comments" />
            </AreaChart>
          </ResponsiveContainer>
        </div>

        {/* Sentiment */}
        <div className="card p-5 space-y-3">
          <div className="text-xs text-gray-500 font-mono uppercase tracking-wider">Sentiment Distribution</div>
          <ResponsiveContainer width="100%" height={200}>
            <PieChart>
              <Pie data={sentData} cx="50%" cy="50%" innerRadius={50} outerRadius={75} paddingAngle={4} dataKey="value">
                <Cell fill="#00D68F" />
                <Cell fill="#FF3B3B" />
                <Cell fill="#6B7280" />
              </Pie>
              <Tooltip content={<CustomTooltip />} />
            </PieChart>
          </ResponsiveContainer>
          <div className="flex flex-wrap justify-center gap-4">
            {sentData.map((d, i) => (
              <div key={d.name} className="flex items-center gap-1.5 text-xs text-gray-400 capitalize">
                <span className="w-2 h-2 rounded-full" style={{ background: ["#00D68F","#FF3B3B","#6B7280"][i] }} />
                {d.name}: {d.value}
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Recent history */}
      <div className="space-y-4">
        <div className="text-xs text-gray-500 font-mono uppercase tracking-wider">Recent Comments</div>
        {history.length === 0 ? (
          <div className="card p-10 text-center text-gray-600 text-sm">
            No comments analyzed yet. Try the Analyzer!
          </div>
        ) : (
          <div className="grid sm:grid-cols-2 gap-3">
            {history.map((c, i) => <HistoryCard key={i} comment={c} />)}
          </div>
        )}
      </div>
    </main>
  );
}
