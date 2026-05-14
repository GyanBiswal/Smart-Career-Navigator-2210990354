"""
Smart Career Navigator - Flask Backend API
==========================================
Main application entry point. Exposes POST /analyze endpoint that
accepts resume + job description text and returns career analysis.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS

from resume_parser import extract_skills
from similarity import compute_similarity, find_missing_skills, calculate_readiness_score
from recommendations import get_recommendations

# ---------------------------------------------------------------------------
# App setup
# ---------------------------------------------------------------------------

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests from the React frontend


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.route("/", methods=["GET"])
def health_check():
    """Simple health-check so you can confirm the server is running."""
    return jsonify({"status": "ok", "message": "Smart Career Navigator API is live."})


@app.route("/analyze", methods=["POST"])
def analyze():
    """
    Main analysis endpoint.

    Expected JSON body:
        {
            "resume": "<resume text>",
            "job_description": "<JD text>"
        }

    Returns:
        {
            "resume_skills":        [...],
            "jd_skills":            [...],
            "matched_skills":       [...],
            "missing_skills":       [...],
            "career_readiness_score": <int 0-100>,
            "recommendations":      [{"skill": ..., "course": ..., "platform": ..., "url": ...}]
        }
    """
    data = request.get_json(silent=True)

    # --- Input validation ---
    if not data:
        return jsonify({"error": "Request body must be JSON."}), 400

    resume_text = data.get("resume", "").strip()
    jd_text = data.get("job_description", "").strip()

    if not resume_text:
        return jsonify({"error": "Field 'resume' is required and cannot be empty."}), 400
    if not jd_text:
        return jsonify({"error": "Field 'job_description' is required and cannot be empty."}), 400

    # --- Core pipeline ---
    try:
        # 1. Extract skills from both texts
        resume_skills = extract_skills(resume_text)
        jd_skills = extract_skills(jd_text)

        # 2. Semantic matching via sentence embeddings + cosine similarity
        matched_skills, similarity_scores = compute_similarity(resume_skills, jd_skills)

        # 3. Identify missing skills (JD skills not semantically matched)
        missing_skills = find_missing_skills(jd_skills, matched_skills)

        # 4. Career Readiness Score (0-100)
        score = calculate_readiness_score(jd_skills, matched_skills, similarity_scores)

        # 5. Personalised course recommendations for missing skills
        recommendations = get_recommendations(missing_skills)

        return jsonify({
            "resume_skills":          sorted(resume_skills),
            "jd_skills":              sorted(jd_skills),
            "matched_skills":         sorted(matched_skills),
            "missing_skills":         sorted(missing_skills),
            "career_readiness_score": score,
            "recommendations":        recommendations,
        })

    except Exception as exc:
        # Surface errors clearly during development
        return jsonify({"error": f"Analysis failed: {str(exc)}"}), 500


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("Starting Smart Career Navigator API on http://localhost:5000")
    app.run(debug=True, port=5000)
