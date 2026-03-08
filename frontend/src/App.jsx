import React from 'react';
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';
import { Stethoscope } from 'lucide-react';
import Home from './pages/Home';
import Dashboard from './pages/Dashboard';
import Scan from './pages/Scan';
import Results from './pages/Results';
import './index.css';

function Navbar() {
  return (
    <nav className="navbar glass">
      <Link to="/" className="logo">
        <Stethoscope size={28} />
        SkinScan AI
      </Link>
      <div className="nav-links">
        <Link to="/dashboard" style={{color: 'var(--text-main)', textDecoration: 'none'}}>Dashboard</Link>
        <Link to="/scan" className="btn-primary flex items-center gap-2" style={{textDecoration: 'none'}}>
          <Stethoscope size={18} /> New Scan
        </Link>
      </div>
    </nav>
  );
}

function App() {
  return (
    <BrowserRouter>
      <Navbar />
      <div className="page-content">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/scan" element={<Scan />} />
          <Route path="/results" element={<Results />} />
        </Routes>
      </div>
    </BrowserRouter>
  );
}

export default App;
