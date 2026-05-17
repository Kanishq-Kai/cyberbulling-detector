import { Link, useLocation } from "react-router-dom";
import { Shield, Sun, Moon, BarChart2, Search, Home, Info } from "lucide-react";

const links = [
  { to: "/",          label: "Home",      Icon: Home      },
  { to: "/analyzer",  label: "Analyzer",  Icon: Search    },
  { to: "/dashboard", label: "Dashboard", Icon: BarChart2 },
  { to: "/about",     label: "About",     Icon: Info      },
];

export default function Navbar({ dark, toggle }) {
  const { pathname } = useLocation();
  return (
    <nav className="sticky top-0 z-50 border-b border-gray-800 bg-[#060910]/90 backdrop-blur-md">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 flex items-center justify-between h-16">
        {/* Logo */}
        <Link to="/" className="flex items-center gap-2 group">
          <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-cyan-400 to-emerald-400 flex items-center justify-center shadow-lg group-hover:shadow-cyan-500/30 transition-shadow">
            <Shield size={18} className="text-gray-900" />
          </div>
          <span className="font-display font-700 text-xl tracking-tight">
            <span className="text-white">Tox</span>
            <span className="gradient-text">Shield</span>
          </span>
        </Link>

        {/* Nav links */}
        <div className="hidden md:flex items-center gap-1">
          {links.map(({ to, label, Icon }) => {
            const active = pathname === to;
            return (
              <Link
                key={to}
                to={to}
                className={`flex items-center gap-1.5 px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
                  active
                    ? "bg-cyan-500/10 text-cyan-400"
                    : "text-gray-400 hover:text-gray-100 hover:bg-white/5"
                }`}
              >
                <Icon size={15} />
                {label}
              </Link>
            );
          })}
        </div>

        {/* Theme toggle */}
        <button
          onClick={toggle}
          className="w-9 h-9 rounded-xl border border-gray-700 flex items-center justify-center text-gray-400 hover:text-cyan-400 hover:border-cyan-500/40 transition-all"
          aria-label="Toggle theme"
        >
          {dark ? <Sun size={16} /> : <Moon size={16} />}
        </button>
      </div>

      {/* Mobile nav */}
      <div className="md:hidden flex border-t border-gray-800">
        {links.map(({ to, label, Icon }) => {
          const active = pathname === to;
          return (
            <Link
              key={to}
              to={to}
              className={`flex-1 flex flex-col items-center py-2 text-xs gap-1 transition-colors ${
                active ? "text-cyan-400" : "text-gray-500"
              }`}
            >
              <Icon size={16} />
              {label}
            </Link>
          );
        })}
      </div>
    </nav>
  );
}
