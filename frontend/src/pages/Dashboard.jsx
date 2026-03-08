import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { ShieldCheck, Calendar, Info, ChevronRight } from 'lucide-react';
import api from '../api';

export default function Dashboard() {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const response = await api.get('/history');
        setHistory(response.data);
      } catch (err) {
        console.error("Error fetching history:", err);
      } finally {
        setLoading(false);
      }
    };
    
    fetchHistory();
  }, [navigate]);

  if (loading) {
    return <div className="container py-12 text-center text-xl mt-12">Loading scans...</div>;
  }

  return (
    <div className="container py-12">
      <div className="flex justify-between items-center mb-8 mt-8">
        <h2 className="text-3xl font-bold">Your Scan History</h2>
        <Link to="/scan" className="btn-primary" style={{textDecoration: 'none'}}>New Scan</Link>
      </div>
      
      {history.length === 0 ? (
        <div className="glass-card text-center py-12 animate-fade-in border border-slate-700/50">
          <div className="flex justify-center mb-4 text-muted"><Info size={48} /></div>
          <h3 className="text-xl font-bold mb-2">No scans yet</h3>
          <p className="text-muted mb-6">Upload your first image to get an AI skin analysis.</p>
          <Link to="/scan" className="btn-primary" style={{textDecoration: 'none'}}>Start Scan</Link>
        </div>
      ) : (
        <div className="history-grid animate-fade-in">
          {history.map((scan) => (
            <div key={scan.id} className="glass-card flex flex-col p-4 border border-slate-700/50 hover:border-slate-600 transition">
              <img 
                src={`http://localhost:8000${scan.image_path}`} 
                alt="Scan" 
                className="history-card-img object-cover rounded shadow-lg"
              />
              <div className="flex justify-between items-start mb-2">
                <div>
                  <h4 className="font-bold text-lg">{scan.top_disease}</h4>
                  <div className="text-sm text-muted flex items-center gap-1 mt-1">
                    <Calendar size={14} /> 
                    {new Date(scan.created_at).toLocaleDateString()}
                  </div>
                </div>
                <span className={`severity-badge severity-${scan.severity.toLowerCase()}`}>
                  {scan.severity}
                </span>
              </div>
              <div className="mt-4 text-sm bg-blue-900/20 p-3 rounded-lg border border-blue-800/30">
                <span className="font-semibold text-accent">Confidence: </span> 
                {((scan.probability) * 100).toFixed(1)}%
              </div>
              <div className="mt-2 text-sm text-slate-400 pl-1">
                <span className="font-semibold text-main">Position: </span> 
                {scan.body_position}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
