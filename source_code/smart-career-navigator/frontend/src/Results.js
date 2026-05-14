/**
 * Results.js
 * ----------
 * Displays the full career analysis:
 *  - Career Readiness Score (animated ring)
 *  - Resume Skills & JD Skills
 *  - Matched Skills
 *  - Missing Skills
 *  - Personalized Course Recommendations
 *
 * Props:
 *   result  – API response object
 *   onReset – callback to return to the input screen
 */

import React from 'react';
import './Results.css';

/* ── Utility: skill pill color by status ── */
function SkillPill({ skill, variant = 'default' }) {
  return (
    <span className={`skill-pill skill-pill--${variant}`}>
      {variant === 'matched' && <span className="pill-dot pill-dot--green" />}
      {variant === 'missing' && <span className="pill-dot pill-dot--red" />}
      {skill}
    </span>
  );
}

/* ── Radial score ring ── */
function ScoreRing({ score }) {
  const radius = 54;
  const circumference = 2 * Math.PI * radius;
  const offset = circumference - (score / 100) * circumference;

  const color =
    score >= 75 ? '#34d399' :
    score >= 50 ? '#4f8ef7' :
    score >= 30 ? '#fbbf24' : '#f87171';

  const label =
    score >= 75 ? 'Excellent Match' :
    score >= 50 ? 'Good Match' :
    score >= 30 ? 'Partial Match' : 'Needs Work';

  return (
    <div className="score-ring-wrap">
      <svg viewBox="0 0 130 130" className="score-ring-svg">
        {/* Background track */}
        <circle
          cx="65" cy="65" r={radius}
          fill="none" stroke="var(--border)" strokeWidth="10"
        />
        {/* Progress arc */}
        <circle
          cx="65" cy="65" r={radius}
          fill="none"
          stroke={color}
          strokeWidth="10"
          strokeLinecap="round"
          strokeDasharray={circumference}
          strokeDashoffset={offset}
          transform="rotate(-90 65 65)"
          style={{ filter: `drop-shadow(0 0 8px ${color}80)` }}
        />
        {/* Score text */}
        <text x="65" y="60" textAnchor="middle" className="ring-score-text" fill={color}>
          {score}
        </text>
        <text x="65" y="75" textAnchor="middle" className="ring-pct-text" fill="var(--text-muted)">
          / 100
        </text>
      </svg>
      <div className="score-label" style={{ color }}>{label}</div>
    </div>
  );
}

/* ── Section card ── */
function Card({ title, icon, children, accent }) {
  return (
    <div className={`result-card ${accent ? `result-card--${accent}` : ''}`}>
      <div className="card-header">
        <span className="card-icon">{icon}</span>
        <h3 className="card-title">{title}</h3>
      </div>
      <div className="card-body">{children}</div>
    </div>
  );
}

/* ── Main Results component ── */
function Results({ result, onReset }) {
  const {
    resume_skills = [],
    jd_skills = [],
    matched_skills = [],
    missing_skills = [],
    career_readiness_score = 0,
    recommendations = [],
  } = result;

  return (
    <div className="results-container">
      {/* ── Top bar ── */}
      <div className="results-topbar">
        <div>
          <h2 className="results-heading">Analysis Complete</h2>
          <p className="results-sub">
            Here's how your profile matches the target role.
          </p>
        </div>
        <button className="btn-outline" onClick={onReset}>
          ← Analyse Another
        </button>
      </div>

      {/* ── Score banner ── */}
      <div className="score-banner">
        <ScoreRing score={career_readiness_score} />
        <div className="score-details">
          <h3 className="score-details-title">Career Readiness Score</h3>
          <p className="score-details-desc">
            Your score is based on how many required skills you have and how
            semantically similar your experience is to the role.
          </p>
          <div className="score-meta">
            <div className="score-meta-item">
              <span className="meta-number meta-green">{matched_skills.length}</span>
              <span className="meta-label">Skills Matched</span>
            </div>
            <div className="score-meta-item">
              <span className="meta-number meta-red">{missing_skills.length}</span>
              <span className="meta-label">Skills Missing</span>
            </div>
            <div className="score-meta-item">
              <span className="meta-number meta-blue">{jd_skills.length}</span>
              <span className="meta-label">Required Total</span>
            </div>
          </div>
        </div>
      </div>

      {/* ── Skills grid ── */}
      <div className="skills-grid">
        {/* Resume skills */}
        <Card title="Your Skills" icon="📄" accent="blue">
          {resume_skills.length === 0 ? (
            <p className="empty-state">No recognisable skills found in your resume.</p>
          ) : (
            <div className="pill-list">
              {resume_skills.map((s) => (
                <SkillPill
                  key={s}
                  skill={s}
                  variant={matched_skills.includes(s) ? 'matched' : 'default'}
                />
              ))}
            </div>
          )}
        </Card>

        {/* JD skills */}
        <Card title="Role Requirements" icon="💼" accent="purple">
          {jd_skills.length === 0 ? (
            <p className="empty-state">No skills extracted from the job description.</p>
          ) : (
            <div className="pill-list">
              {jd_skills.map((s) => (
                <SkillPill
                  key={s}
                  skill={s}
                  variant={matched_skills.includes(s) ? 'matched' : 'missing'}
                />
              ))}
            </div>
          )}
        </Card>
      </div>

      {/* ── Missing skills ── */}
      {missing_skills.length > 0 && (
        <Card title="Missing Skills" icon="🎯" accent="red">
          <p className="card-intro">
            Upskill in these areas to significantly increase your readiness score.
          </p>
          <div className="pill-list">
            {missing_skills.map((s) => (
              <SkillPill key={s} skill={s} variant="missing" />
            ))}
          </div>
        </Card>
      )}

      {/* ── Recommendations ── */}
      {recommendations.length > 0 && (
        <Card title="Learning Roadmap" icon="🚀" accent="green">
          <p className="card-intro">
            Personalised courses to close your skill gaps and land the role.
          </p>
          <div className="recs-grid">
            {recommendations.map((rec, i) => (
              <a
                key={i}
                href={rec.url}
                target="_blank"
                rel="noopener noreferrer"
                className="rec-card"
              >
                <div className="rec-header">
                  <span className="rec-skill">{rec.skill}</span>
                  <span className={`rec-level rec-level--${rec.level.toLowerCase()}`}>
                    {rec.level}
                  </span>
                </div>
                <div className="rec-course">{rec.course}</div>
                <div className="rec-platform">
                  <span className="platform-dot" />
                  {rec.platform}
                  <span className="rec-arrow">→</span>
                </div>
              </a>
            ))}
          </div>
        </Card>
      )}

      {/* ── Footer action ── */}
      <div className="results-footer">
        <button className="btn-outline" onClick={onReset}>
          ← Start a New Analysis
        </button>
      </div>
    </div>
  );
}

export default Results;
