"""
similarity.py
=============
Semantic skill matching using Sentence-BERT embeddings and cosine similarity.

Pipeline
--------
1. Encode all resume skills and JD skills into dense vector embeddings
   using the 'all-MiniLM-L6-v2' model (fast, 384-dim).
2. For every JD skill, find the most similar resume skill via cosine
   similarity.  If the best match exceeds a configurable threshold, the
   JD skill is considered "matched".
3. The matched set and raw similarity scores feed the readiness calculator.

Why sentence embeddings?
------------------------
Exact keyword matching misses synonyms ("machine learning" ≠ "ML") and
related skills ("PyTorch" covers "deep learning" partially).  Embeddings
handle these nuances gracefully.
"""

from __future__ import annotations

from typing import Optional

import numpy as np

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

# Similarity threshold: if the best-match cosine score for a JD skill is
# above this value, the skill is considered "matched" from the resume.
MATCH_THRESHOLD = 0.60

# Fallback: if sentence-transformers is unavailable, we fall back to a simple
# Jaccard/token-overlap similarity so the API still functions.
_FALLBACK_MODE = False

# ---------------------------------------------------------------------------
# Model loading (lazy, cached)
# ---------------------------------------------------------------------------

_model = None


def _get_model():
    """Load the SentenceTransformer model once and cache it."""
    global _model, _FALLBACK_MODE
    if _model is not None:
        return _model

    try:
        from sentence_transformers import SentenceTransformer
        print("[similarity] Loading SentenceTransformer model (all-MiniLM-L6-v2)…")
        _model = SentenceTransformer("all-MiniLM-L6-v2")
        print("[similarity] Model loaded successfully.")
    except ImportError:
        print("[similarity] WARNING: sentence-transformers not installed. "
              "Falling back to token-overlap similarity.")
        _FALLBACK_MODE = True
        _model = None

    return _model


# ---------------------------------------------------------------------------
# Cosine similarity helpers
# ---------------------------------------------------------------------------

def _cosine(a: np.ndarray, b: np.ndarray) -> float:
    """Cosine similarity between two 1-D vectors."""
    denom = np.linalg.norm(a) * np.linalg.norm(b)
    if denom == 0:
        return 0.0
    return float(np.dot(a, b) / denom)


def _embed(texts: list[str]) -> Optional[np.ndarray]:
    """Return (N, D) embedding matrix or None if model unavailable."""
    model = _get_model()
    if model is None:
        return None
    return model.encode(texts, convert_to_numpy=True, normalize_embeddings=True)


# ---------------------------------------------------------------------------
# Fallback: token-overlap Jaccard
# ---------------------------------------------------------------------------

def _jaccard(s1: str, s2: str) -> float:
    t1, t2 = set(s1.lower().split()), set(s2.lower().split())
    if not t1 and not t2:
        return 1.0
    return len(t1 & t2) / len(t1 | t2)


def _fallback_similarity(resume_skills: list[str], jd_skills: list[str]):
    """Token-overlap matching when embeddings are unavailable."""
    matched: set[str] = set()
    scores: dict[str, float] = {}

    for jd_skill in jd_skills:
        best_score = 0.0
        for r_skill in resume_skills:
            sc = _jaccard(jd_skill, r_skill)
            if sc > best_score:
                best_score = sc
        scores[jd_skill] = best_score
        if best_score >= MATCH_THRESHOLD:
            matched.add(jd_skill)

    return matched, scores


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def compute_similarity(
    resume_skills: list[str],
    jd_skills: list[str],
) -> tuple[set[str], dict[str, float]]:
    """
    Compare resume skills against JD skills using semantic embeddings.

    Parameters
    ----------
    resume_skills : list[str]
        Skills extracted from the candidate's resume.
    jd_skills : list[str]
        Skills required by the job description.

    Returns
    -------
    matched_skills : set[str]
        Subset of *jd_skills* that are semantically covered by *resume_skills*.
    similarity_scores : dict[str, float]
        Best cosine similarity score for each JD skill (keyed by skill name).
    """
    if not resume_skills or not jd_skills:
        return set(), {skill: 0.0 for skill in jd_skills}

    # --- Attempt embedding-based matching ---
    embeddings = _embed(resume_skills + jd_skills)

    if embeddings is None or _FALLBACK_MODE:
        return _fallback_similarity(resume_skills, jd_skills)

    r_emb = embeddings[: len(resume_skills)]     # (R, D)
    j_emb = embeddings[len(resume_skills) :]     # (J, D)

    # Cosine similarity matrix: (J, R)  [embeddings are L2-normalised → dot == cosine]
    sim_matrix = j_emb @ r_emb.T                 # shape (J, R)

    matched: set[str] = set()
    scores: dict[str, float] = {}

    for j_idx, jd_skill in enumerate(jd_skills):
        best_score = float(sim_matrix[j_idx].max())
        scores[jd_skill] = round(best_score, 4)
        if best_score >= MATCH_THRESHOLD:
            matched.add(jd_skill)

    return matched, scores


def find_missing_skills(
    jd_skills: list[str],
    matched_skills: set[str],
) -> list[str]:
    """
    Return JD skills not covered by the candidate's resume.

    Parameters
    ----------
    jd_skills : list[str]
        Full list of skills from the job description.
    matched_skills : set[str]
        Skills already semantically matched in the resume.

    Returns
    -------
    list[str]
        Unmatched / missing skills.
    """
    return [s for s in jd_skills if s not in matched_skills]


def calculate_readiness_score(
    jd_skills: list[str],
    matched_skills: set[str],
    similarity_scores: dict[str, float],
) -> int:
    """
    Career Readiness Score (0–100).

    Formula
    -------
    score = 0.7 * coverage_ratio  +  0.3 * avg_similarity_of_matched

    - coverage_ratio    : fraction of JD skills matched (0–1).
    - avg_similarity    : mean cosine similarity of matched skills (0–1).

    The weighted blend rewards both breadth (covering many JD skills) and
    depth (high-confidence matches on the skills that are covered).

    Parameters
    ----------
    jd_skills : list[str]
    matched_skills : set[str]
    similarity_scores : dict[str, float]

    Returns
    -------
    int
        Score clamped to [0, 100].
    """
    if not jd_skills:
        return 0

    coverage = len(matched_skills) / len(jd_skills)

    matched_scores = [similarity_scores.get(s, 0.0) for s in matched_skills]
    avg_sim = float(np.mean(matched_scores)) if matched_scores else 0.0

    raw_score = 0.70 * coverage + 0.30 * avg_sim
    return int(round(min(max(raw_score * 100, 0), 100)))


# ---------------------------------------------------------------------------
# Quick smoke-test
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    resume_skills = ["python", "machine learning", "tensorflow", "docker", "sql"]
    jd_skills = ["python", "deep learning", "pytorch", "kubernetes", "nosql", "aws"]

    matched, scores = compute_similarity(resume_skills, jd_skills)
    missing = find_missing_skills(jd_skills, matched)
    score = calculate_readiness_score(jd_skills, matched, scores)

    print("Matched :", matched)
    print("Missing :", missing)
    print("Scores  :", scores)
    print("Readiness Score:", score)
