import { Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import Home from "./pages/Home";
import Analyzer from "./pages/Analyzer";
import Dashboard from "./pages/Dashboard";
import About from "./pages/About";
import { useTheme } from "./hooks/useTheme";

export default function App() {
  const { dark, toggle } = useTheme();
  return (
    <div className={dark ? "dark" : "light"}>
      <div className="min-h-screen bg-[#0A0E1A] dark:bg-[#0A0E1A] text-gray-100 transition-colors duration-300">
        <div className="scan-line" />
        <Navbar dark={dark} toggle={toggle} />
        <Routes>
          <Route path="/"          element={<Home />} />
          <Route path="/analyzer"  element={<Analyzer />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/about"     element={<About />} />
        </Routes>
      </div>
    </div>
  );
}
