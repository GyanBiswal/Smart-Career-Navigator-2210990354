/**
 * App.js
 * ------
 * Root component for Smart Career Navigator.
 * Manages global state and coordinates between
 * UploadResume (input) and Results (output) panels.
 */

import React, { useState } from 'react';
import UploadResume from './UploadResume';
import Results from './Results';
import './App.css';

function App() {
  // null  → not yet analysed
  // {}    → analysis result from backend
  const [analysisResult, setAnalysisResult] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  /**
   * Called by UploadResume when the user submits.
   * Sends resume + JD to the Flask backend and stores the result.
   */
  const handleAnalyse = async ({ resume, jobDescription }) => {
    setIsLoading(true);
    setError(null);
    setAnalysisResult(null);

    try {
      const response = await fetch('/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ resume, job_description: jobDescription }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || `Server error: ${response.status}`);
      }

      setAnalysisResult(data);
    } catch (err) {
      setError(err.message || 'Something went wrong. Is the backend running?');
    } finally {
      setIsLoading(false);
    }
  };

  const handleReset = () => {
    setAnalysisResult(null);
    setError(null);
  };

  return (
    <div className="app">
      {/* ── Header ── */}
      <header className="app-header">
        <div className="header-inner">
          <div className="logo">
            <span className="logo-icon">🧭</span>
            <div className="logo-text">
              <span className="logo-title">Smart Career Navigator</span>
              <span className="logo-sub">AI-Powered Career Guidance</span>
            </div>
          </div>
          <nav className="header-nav">
            <span className="nav-badge">Beta</span>
          </nav>
        </div>
      </header>

      {/* ── Main ── */}
      <main className="app-main">
        {!analysisResult ? (
          <UploadResume
            onAnalyse={handleAnalyse}
            isLoading={isLoading}
            error={error}
          />
        ) : (
          <Results result={analysisResult} onReset={handleReset} />
        )}
      </main>

      {/* ── Footer ── */}
      <footer className="app-footer">
        <p>
          Smart Career Navigator · Built with React + Flask + BERT ·{' '}
          <span className="footer-accent">Powered by AI</span>
        </p>
      </footer>
    </div>
  );
}

export default App;
