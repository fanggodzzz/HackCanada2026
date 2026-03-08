import React from 'react';
import { Link } from 'react-router-dom';
import { ShieldCheck, Zap, Activity } from 'lucide-react';

export default function Home() {
  return (
    <div className="container">
      <div className="flex flex-col items-center justify-center text-center py-12 animate-fade-in">
        <div className="glass-card max-w-4xl w-full mt-12 mb-12">
          <h1 className="text-5xl font-bold mb-6">
            Intelligent Skin Care <br/> 
            <span className="text-accent">Powered by AI</span>
          </h1>
          <p className="text-xl text-muted mb-8 max-w-2xl mx-auto">
            Upload an image of your skin condition and let our advanced neural network predict up to 10+ diseases with corresponding severity and treatment recommendations.
          </p>
          <div className="flex justify-center gap-4">
            <Link to="/scan" className="btn-primary flex items-center gap-2 text-lg" style={{textDecoration: 'none'}}>
              Start Scanning
            </Link>
          </div>
        </div>

        <div className="flex gap-8 w-full mt-8" style={{flexWrap: 'wrap', justifyContent: 'center'}}>
          <div className="glass-card animate-fade-in animate-delay-1 flex flex-col items-center text-center" style={{flex: '1', minWidth: '300px'}}>
            <div className="mb-4" style={{color: 'var(--accent)'}}>
              <Zap size={48} />
            </div>
            <h3 className="text-xl font-bold mb-2">Instant Analysis</h3>
            <p className="text-muted">Get results in seconds using state-of-the-art ResNet transfer learning.</p>
          </div>
          <div className="glass-card animate-fade-in animate-delay-2 flex flex-col items-center text-center" style={{flex: '1', minWidth: '300px'}}>
            <div className="mb-4" style={{color: 'var(--accent)'}}>
              <ShieldCheck size={48} />
            </div>
            <h3 className="text-xl font-bold mb-2">Secure & Private</h3>
            <p className="text-muted">Your data is processed securely and efficiently without requiring an account.</p>
          </div>
          <div className="glass-card animate-fade-in animate-delay-3 flex flex-col items-center text-center" style={{flex: '1', minWidth: '300px'}}>
            <div className="mb-4" style={{color: 'var(--accent)'}}>
              <Activity size={48} />
            </div>
            <h3 className="text-xl font-bold mb-2">Actionable Insights</h3>
            <p className="text-muted">Receive severity indicators and recognized medical treatment guidelines.</p>
          </div>
        </div>
      </div>
    </div>
  );
}
