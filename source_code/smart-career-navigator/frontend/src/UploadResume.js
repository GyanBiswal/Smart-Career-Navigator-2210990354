/**
 * UploadResume.js
 * ---------------
 * Input panel where the user pastes their resume and a job description,
 * then triggers the AI analysis.
 *
 * Props:
 *   onAnalyse(data)  – callback with { resume, jobDescription }
 *   isLoading        – boolean, shows spinner while API is running
 *   error            – string or null, displays error message
 */

import React, { useState } from 'react';
import './UploadResume.css';

/* ─── Sample data so users can try instantly ─── */
const SAMPLE_RESUME = `John Smith
john.smith@email.com | linkedin.com/in/johnsmith | github.com/johnsmith

SUMMARY
Data Scientist with 3 years of experience building machine learning models and 
data pipelines. Strong Python developer comfortable with end-to-end ML workflows.

SKILLS
Languages: Python, SQL, Bash
ML/AI: scikit-learn, TensorFlow, pandas, NumPy, matplotlib, spaCy
Databases: PostgreSQL, MongoDB
Tools: Docker, Git, GitHub, Jupyter

EXPERIENCE
Data Scientist – TechCorp (2022–Present)
• Built classification models using scikit-learn; improved churn prediction by 18%.
• Developed ETL pipelines with Python and PostgreSQL.
• Containerised model serving with Docker.
• Collaborated via GitHub with CI/CD workflows.

Junior Data Analyst – DataInsights (2021–2022)
• Performed statistical analysis on customer datasets using Python and SQL.
• Created dashboards and visualisations with matplotlib and seaborn.

EDUCATION
B.Sc. Computer Science – State University, 2021

PROJECTS
• NLP Chatbot: Built intent-classification chatbot using spaCy and Flask.
• Stock Predictor: Time-series forecasting with ARIMA and LSTM.`;

const SAMPLE_JD = `Senior Data Scientist – Machine Learning Platform

We are looking for a Senior Data Scientist to join our AI/ML team.

Required Skills:
- Strong Python programming (pandas, NumPy, scikit-learn)
- Deep learning frameworks: PyTorch or TensorFlow
- Natural Language Processing (NLP)
- SQL and NoSQL databases (PostgreSQL, MongoDB)
- Cloud deployment on AWS
- Docker and Kubernetes for containerised deployments
- CI/CD pipelines (GitHub Actions)
- Statistical analysis and hypothesis testing
- Leadership and communication skills

Nice to Have:
- Apache Spark for big data
- Apache Kafka for streaming
- MLOps experience
- dbt and data warehouse knowledge`;

function UploadResume({ onAnalyse, isLoading, error }) {
  const [resume, setResume] = useState('');
  const [jobDescription, setJobDescription] = useState('');

  const loadSampleData = () => {
    setResume(SAMPLE_RESUME);
    setJobDescription(SAMPLE_JD);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!resume.trim() || !jobDescription.trim()) return;
    onAnalyse({ resume, jobDescription });
  };

  const isEmpty = !resume.trim() || !jobDescription.trim();

  return (
    <div className="upload-container">
      {/* ── Hero section ── */}
      <div className="upload-hero">
        <h1 className="hero-title">
          Decode Your Career Gap.<br />
          <span className="hero-highlight">Bridge It with AI.</span>
        </h1>
        <p className="hero-sub">
          Paste your resume and a job description. Our AI extracts skills,
          calculates your Career Readiness Score, and recommends exactly what
          you need to learn next.
        </p>
        <div className="hero-stats">
          <div className="stat">
            <span className="stat-number">BERT</span>
            <span className="stat-label">Semantic Matching</span>
          </div>
          <div className="stat-divider" />
          <div className="stat">
            <span className="stat-number">spaCy</span>
            <span className="stat-label">Skill Extraction</span>
          </div>
          <div className="stat-divider" />
          <div className="stat">
            <span className="stat-number">NLP</span>
            <span className="stat-label">AI Analysis</span>
          </div>
        </div>
      </div>

      {/* ── Form ── */}
      <form className="upload-form" onSubmit={handleSubmit}>
        <div className="form-grid">
          {/* Resume textarea */}
          <div className="field-group">
            <label className="field-label">
              <span className="field-icon">📄</span>
              Your Resume
              <span className="field-hint">Paste the full text of your resume</span>
            </label>
            <textarea
              className="field-textarea"
              placeholder="Paste your resume here…&#10;&#10;Include skills, experience, education, projects."
              value={resume}
              onChange={(e) => setResume(e.target.value)}
              rows={16}
              spellCheck={false}
            />
            <div className="char-count">{resume.length.toLocaleString()} chars</div>
          </div>

          {/* Job description textarea */}
          <div className="field-group">
            <label className="field-label">
              <span className="field-icon">💼</span>
              Job Description
              <span className="field-hint">Paste the target role's JD</span>
            </label>
            <textarea
              className="field-textarea"
              placeholder="Paste the job description here…&#10;&#10;Include required skills, responsibilities, qualifications."
              value={jobDescription}
              onChange={(e) => setJobDescription(e.target.value)}
              rows={16}
              spellCheck={false}
            />
            <div className="char-count">{jobDescription.length.toLocaleString()} chars</div>
          </div>
        </div>

        {/* Error banner */}
        {error && (
          <div className="error-banner">
            <span className="error-icon">⚠️</span>
            <span>{error}</span>
          </div>
        )}

        {/* Actions */}
        <div className="form-actions">
          <button
            type="button"
            className="btn-secondary"
            onClick={loadSampleData}
            disabled={isLoading}
          >
            Load Sample Data
          </button>

          <button
            type="submit"
            className="btn-primary"
            disabled={isEmpty || isLoading}
          >
            {isLoading ? (
              <>
                <span className="spinner" />
                Analysing…
              </>
            ) : (
              <>
                <span>⚡</span>
                Analyse My Career
              </>
            )}
          </button>
        </div>

        {isEmpty && !isLoading && (
          <p className="form-hint">Both fields are required to run the analysis.</p>
        )}
      </form>
    </div>
  );
}

export default UploadResume;
