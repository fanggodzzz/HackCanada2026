import React, { useEffect } from 'react';
import { useLocation, useNavigate, Link } from 'react-router-dom';
import { AlertTriangle, CheckCircle, Info, ArrowLeft, Activity, ListChecks } from 'lucide-react';

export default function Results() {
  const location = useLocation();
  const navigate = useNavigate();
  const result = location.state?.result;

  useEffect(() => {
    if (!result) {
      navigate('/dashboard');
    }
  }, [result, navigate]);

  if (!result) return null;

  const topPrediction = result.predictions[0];
  const otherPredictions = result.predictions.slice(1);

  return (
    <div className="container py-12">
      <Link to="/dashboard" className="flex items-center gap-2 text-muted hover:text-white mb-6 transition" style={{textDecoration: 'none'}}>
        <ArrowLeft size={16} /> Back to Dashboard
      </Link>
      
      <div className="flex flex-col md:flex-row gap-8 animate-fade-in" style={{display: 'flex', gap: '2rem'}}>
        <div className="w-full md:w-1/3" style={{flex: '1', minWidth: '300px'}}>
          <div className="glass-card flex flex-col items-center">
            <img 
              src={`http://localhost:8000${result.image_path}`} 
              alt="Scan" 
              className="w-full max-w-full rounded-lg mb-4 shadow-lg border border-slate-700 object-cover"
              style={{maxHeight: '400px', width: '100%'}}
            />
            <div className="w-full text-center p-3 bg-slate-800/30 rounded-lg">
              <p className="text-muted text-sm mb-1 uppercase tracking-wide">Body Position</p>
              <p className="font-semibold text-lg">{result.body_position}</p>
            </div>
          </div>
        </div>
        
        <div className="w-full md:w-2/3" style={{flex: '2'}}>
          <div className="glass-card mb-6 border-l-4 shadow-xl" style={{borderLeftColor: topPrediction.severity === 'Serious' ? 'var(--danger)' : topPrediction.severity === 'Medium' ? 'var(--warning)' : 'var(--success)', borderLeftWidth: '4px', borderLeftStyle: 'solid'}}>
            <div className="flex justify-between items-start mb-4">
              <div>
                <h2 className="text-3xl font-bold text-main flex items-center gap-3 mb-2" style={{alignItems: 'center', display: 'flex'}}>
                  {topPrediction.disease}
                  <span className={`severity-badge severity-${topPrediction.severity.toLowerCase()}`} style={{marginLeft: '0.5rem', whiteSpace: 'nowrap'}}>
                    {topPrediction.severity}
                  </span>
                </h2>
                <div className="text-xl text-accent mt-2 flex items-center gap-2 bg-blue-900/10 p-2 px-3 rounded-lg inline-flex">
                  <Activity size={20} /> 
                  <span className="font-semibold">Confidence:</span> {(topPrediction.probability * 100).toFixed(1)}%
                </div>
              </div>
            </div>
            
            <div className="mt-8">
              <h3 className="text-xl font-bold mb-3 flex items-center gap-2 border-b border-slate-700/50 pb-2">
                <ListChecks size={20} className="text-primary" /> Recommended Action Plan
              </h3>
              <ul className="space-y-3 mt-4" style={{listStyleType: 'none', padding: 0}}>
                {topPrediction.treatments.map((treatment, idx) => (
                  <li key={idx} className="flex gap-3 items-start p-4 bg-slate-800/50 rounded-lg border border-slate-700/50 shadow-sm">
                    <CheckCircle className="text-success flex-shrink-0 mt-1" size={20} />
                    <span className="text-lg">{treatment}</span>
                  </li>
                ))}
              </ul>
              {topPrediction.severity === 'Serious' && (
                <div className="mt-6 p-5 bg-red-900/20 border border-red-500/30 rounded-lg flex gap-3 text-red-200 shadow-inner">
                  <AlertTriangle className="text-danger flex-shrink-0 mt-1" size={24} />
                  <p className="font-medium text-[15px] leading-relaxed">This is considered a serious condition. We strongly advise consulting a healthcare professional or dermatologist immediately for a formal medical diagnosis and personalized treatment plan.</p>
                </div>
              )}
            </div>
          </div>
          
          <div className="glass-card animate-fade-in animate-delay-2 p-6 shadow-lg">
            <h3 className="text-lg font-bold mb-4 text-muted flex items-center gap-2 border-b border-slate-700/50 pb-2">
              <Info size={18} /> Differential Diagnosis (Other possibilities)
            </h3>
            
            <div className="flex flex-col gap-0">
              {otherPredictions.map((pred, idx) => (
                <div key={idx} className="flex justify-between items-center p-4 border-b border-slate-700/30 last:border-0 hover:bg-slate-800/30 transition">
                  <div>
                    <h4 className="font-semibold text-main text-[17px]">{pred.disease}</h4>
                    <span className={`severity-badge severity-${pred.severity.toLowerCase()} text-xs mt-2 inline-block shadow-sm`}>
                      {pred.severity}
                    </span>
                  </div>
                  <div className="text-right">
                    <div className="font-mono font-bold text-slate-300 bg-slate-800 px-3 py-1 rounded border border-slate-700">
                      {(pred.probability * 100).toFixed(1)}%
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
          
        </div>
      </div>
    </div>
  );
}
