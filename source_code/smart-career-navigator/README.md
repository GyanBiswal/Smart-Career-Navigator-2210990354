# 🧭 Smart Career Navigator

> **AI-powered career guidance platform** that analyses your resume against a job description, identifies skill gaps, calculates a Career Readiness Score, and recommends personalised learning paths.

---

## 📸 Overview

Smart Career Navigator bridges the gap between where you are and where you want to be. Paste your resume and a target job description — our NLP pipeline does the rest:

1. **Resume Parsing** – Extracts skills from raw resume text using spaCy & a curated taxonomy.  
2. **Skill Extraction** – Identifies required skills from any job description.  
3. **Semantic Matching** – Uses BERT embeddings (all-MiniLM-L6-v2) + cosine similarity to match skills intelligently — "ML" matches "machine learning", etc.  
4. **Missing Skill Identification** – Pinpoints exactly what you need to learn.  
5. **Career Readiness Score (0–100)** – Weighted blend of coverage and semantic confidence.  
6. **Personalised Recommendations** – Curated courses from Coursera, Udemy, Google, and more.

---

## ✨ Features

| Feature | Details |
|---|---|
| Semantic skill matching | BERT sentence embeddings + cosine similarity (threshold 0.60) |
| NLP skill extraction | spaCy en_core_web_sm + curated 100+ skill taxonomy |
| Career Readiness Score | `0.7 × coverage + 0.3 × avg_similarity` formula |
| Course recommendations | 30+ curated courses mapped to skills |
| Clean React UI | Responsive, dark-themed, accessible |
| Sample data | One-click load of a realistic resume + JD for instant demo |

---

## 🛠 Tech Stack

### Frontend
- **React 18** – Component-based UI
- **Axios** – HTTP client (via `fetch` API)
- **Custom CSS** – No heavy UI libraries, fully hand-crafted design

### Backend
- **Python 3.10+**
- **Flask 3** – Lightweight REST API
- **Flask-CORS** – Cross-origin support for local dev

### AI / NLP
- **spaCy** (`en_core_web_sm`) – Tokenisation & noun-chunk extraction
- **Sentence Transformers** (`all-MiniLM-L6-v2`) – BERT-based embeddings
- **NumPy** – Cosine similarity computation

### Database *(optional)*
- **MongoDB** via `pymongo` – Ready to wire up for storing analyses

---

## 📁 Project Structure

```
smart-career-navigator/
├── backend/
│   ├── app.py               # Flask API (POST /analyze)
│   ├── resume_parser.py     # Skill extraction with spaCy
│   ├── similarity.py        # BERT embeddings + cosine similarity
│   ├── recommendations.py   # Course recommendation engine
│   ├── sample_jd.txt        # Sample job description
│   └── requirements.txt     # Python dependencies
│
├── frontend/
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── App.js           # Root component + API call
│   │   ├── App.css
│   │   ├── UploadResume.js  # Input panel (resume + JD)
│   │   ├── UploadResume.css
│   │   ├── Results.js       # Analysis results display
│   │   ├── Results.css
│   │   ├── index.js
│   │   └── index.css        # Global styles & CSS variables
│   └── package.json
│
└── README.md
```

---

## 🚀 Installation & Setup

### Prerequisites
- **Node.js** ≥ 18.x and **npm** ≥ 9.x
- **Python** ≥ 3.10
- **pip** ≥ 23

---

### 1 · Backend Setup

```bash
# Navigate to backend directory
cd smart-career-navigator/backend

# Create and activate a virtual environment (recommended)
python -m venv venv

# macOS / Linux
source venv/bin/activate

# Windows
venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt

# Download the spaCy English language model
python -m spacy download en_core_web_sm
```

> **Note:** The first run downloads the `all-MiniLM-L6-v2` model (~80 MB) automatically. This may take a minute depending on your connection.

### 2 · Start the Backend

```bash
# From the backend/ directory (with venv active)
python app.py
```

You should see:
```
Starting Smart Career Navigator API on http://localhost:5000
```

Test it's working:
```bash
curl http://localhost:5000/
# → {"message": "Smart Career Navigator API is live.", "status": "ok"}
```

---

### 3 · Frontend Setup

```bash
# Open a new terminal, navigate to frontend/
cd smart-career-navigator/frontend

# Install Node dependencies
npm install

# Start the React dev server
npm start
```

The app opens at **http://localhost:3000**. The `"proxy": "http://localhost:5000"` in `package.json` forwards API calls to Flask automatically.

---

## 🧪 Testing the API Directly

```bash
curl -X POST http://localhost:5000/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "resume": "Experienced Python developer with TensorFlow, Docker, and SQL skills.",
    "job_description": "Looking for a data scientist with Python, PyTorch, Kubernetes, and AWS experience."
  }'
```

Expected response shape:
```json
{
  "resume_skills": ["docker", "python", "sql", "tensorflow"],
  "jd_skills": ["aws", "kubernetes", "python", "pytorch"],
  "matched_skills": ["python"],
  "missing_skills": ["aws", "kubernetes", "pytorch"],
  "career_readiness_score": 42,
  "recommendations": [
    {
      "skill": "aws",
      "course": "AWS Certified Solutions Architect – Associate",
      "platform": "AWS Training",
      "url": "https://aws.amazon.com/...",
      "level": "Intermediate"
    }
  ]
}
```

---

## ⚙️ Configuration

### Matching Threshold
In `backend/similarity.py`, change `MATCH_THRESHOLD` (default `0.60`) to control how strict semantic matching is:
- Lower (e.g. `0.50`) → more permissive, higher scores
- Higher (e.g. `0.75`) → stricter, highlights more gaps

### Score Formula
In `backend/similarity.py`, adjust `calculate_readiness_score()`:
- `0.70` weight on coverage (breadth)
- `0.30` weight on similarity (depth)

### Skill Taxonomy
In `backend/resume_parser.py`, add skills to `SKILL_TAXONOMY` (lowercase):
```python
SKILL_TAXONOMY = {
    ...,
    "your new skill",
}
```

### Course Catalog
In `backend/recommendations.py`, add entries to `COURSE_CATALOG`:
```python
{
    "skill": "your new skill",
    "course": "Course Name",
    "platform": "Platform",
    "url": "https://...",
    "level": "Beginner",
},
```

---

## 🗄 MongoDB Integration (Optional)

The project includes `pymongo` in requirements. To store analysis results:

1. Install and start MongoDB locally, or use [MongoDB Atlas](https://www.mongodb.com/cloud/atlas).
2. Add to `backend/app.py`:

```python
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["career_navigator"]
analyses = db["analyses"]

# Inside the /analyze route, after building the response:
analyses.insert_one({**response_data, "timestamp": datetime.utcnow()})
```

---

## 🤝 Contributing

1. Fork the repository.
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Commit your changes: `git commit -m "feat: add my feature"`
4. Push and open a Pull Request.

---

## 📄 License

MIT License — free to use, modify, and distribute.

---

## 💡 Future Ideas

- PDF resume upload (via `pdfplumber` or `PyMuPDF`)
- User authentication & saved analyses
- LinkedIn job scraping integration
- Salary range display alongside job matches
- Progress tracker to monitor skill development over time
