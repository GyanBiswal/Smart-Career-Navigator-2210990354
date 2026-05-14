"""
resume_parser.py
================
Extracts skills from raw text (resume or job description) using a
curated skill dictionary and optional spaCy NLP for noun-chunk refinement.

Strategy
--------
1. Normalise the input text to lowercase.
2. Check each token / bigram / trigram against a predefined skill list.
3. Optionally use spaCy noun-chunks to catch compound terms not in the list.
4. Return a deduplicated set of matched skill strings.
"""

import re
import string

# ---------------------------------------------------------------------------
# Predefined skill taxonomy
# ---------------------------------------------------------------------------
# Organised by domain for easy extension. All entries are lowercase.

SKILL_TAXONOMY = {
    # --- Programming Languages ---
    "python", "java", "javascript", "typescript", "c++", "c#", "go", "golang",
    "rust", "kotlin", "swift", "scala", "r", "matlab", "perl", "ruby", "php",
    "bash", "shell scripting", "powershell",

    # --- Web / Frontend ---
    "react", "react.js", "reactjs", "angular", "vue", "vue.js", "next.js",
    "nuxt.js", "html", "css", "sass", "tailwind css", "bootstrap", "jquery",
    "webpack", "vite", "redux", "graphql", "rest api", "restful api",

    # --- Backend / Frameworks ---
    "flask", "django", "fastapi", "express", "node.js", "nodejs", "spring boot",
    "asp.net", "laravel", "rails", "ruby on rails",

    # --- Data & ML ---
    "machine learning", "deep learning", "natural language processing", "nlp",
    "computer vision", "data analysis", "data science", "feature engineering",
    "model deployment", "mlops", "reinforcement learning", "transfer learning",
    "time series", "statistical analysis", "hypothesis testing",

    # --- ML Libraries / Frameworks ---
    "tensorflow", "keras", "pytorch", "scikit-learn", "sklearn", "xgboost",
    "lightgbm", "catboost", "hugging face", "transformers", "spacy", "nltk",
    "opencv", "pandas", "numpy", "scipy", "matplotlib", "seaborn", "plotly",

    # --- Databases ---
    "sql", "mysql", "postgresql", "sqlite", "mongodb", "redis", "elasticsearch",
    "cassandra", "dynamodb", "firebase", "oracle", "microsoft sql server",
    "nosql",

    # --- Cloud & DevOps ---
    "aws", "azure", "google cloud", "gcp", "docker", "kubernetes", "terraform",
    "ansible", "jenkins", "github actions", "ci/cd", "devops", "linux",
    "nginx", "apache", "microservices", "serverless",

    # --- Data Engineering ---
    "apache spark", "hadoop", "kafka", "airflow", "dbt", "etl", "data pipeline",
    "data warehouse", "snowflake", "bigquery", "redshift", "databricks",

    # --- Version Control & Tools ---
    "git", "github", "gitlab", "bitbucket", "jira", "confluence", "trello",
    "agile", "scrum", "kanban",

    # --- Soft / Misc ---
    "communication", "leadership", "problem solving", "critical thinking",
    "teamwork", "project management", "time management", "presentation skills",
}

# Build bigram/trigram lookup for multi-word skills
MULTI_WORD_SKILLS = {s for s in SKILL_TAXONOMY if " " in s}
SINGLE_WORD_SKILLS = SKILL_TAXONOMY - MULTI_WORD_SKILLS


# ---------------------------------------------------------------------------
# Helper: try to load spaCy (graceful fallback if not installed / model missing)
# ---------------------------------------------------------------------------

def _load_spacy():
    try:
        import spacy
        nlp = spacy.load("en_core_web_sm")
        return nlp
    except Exception:
        return None


_NLP = _load_spacy()


# ---------------------------------------------------------------------------
# Core extraction
# ---------------------------------------------------------------------------

def _normalise(text: str) -> str:
    """Lowercase, collapse whitespace, remove non-printable chars."""
    text = text.lower()
    text = re.sub(r"[^\x20-\x7e]", " ", text)   # non-ASCII → space
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def _tokenise(text: str) -> list[str]:
    """
    Return list of word tokens, stripping punctuation except '.' and '+' which
    are part of language names (c++, asp.net, etc.).
    """
    # Keep alphanumerics, spaces, dots, plus signs, forward-slash, and #
    cleaned = re.sub(r"[^\w\s.+/#]", " ", text)
    return cleaned.split()


def extract_skills(text: str) -> list[str]:
    """
    Extract skills from *text* and return a deduplicated list (sorted).

    Parameters
    ----------
    text : str
        Raw resume or job-description text.

    Returns
    -------
    list[str]
        Unique skill names found in the text (original casing from taxonomy).
    """
    normalised = _normalise(text)
    found: set[str] = set()

    # --- 1. Multi-word skill scan (trigrams → bigrams → single words) ---
    tokens = _tokenise(normalised)
    n = len(tokens)

    i = 0
    while i < n:
        # Try longest match first (trigram)
        matched = False
        for length in (3, 2, 1):
            if i + length > n:
                continue
            candidate = " ".join(tokens[i: i + length])
            if candidate in SKILL_TAXONOMY:
                found.add(candidate)
                i += length
                matched = True
                break
        if not matched:
            i += 1

    # --- 2. spaCy noun-chunk pass (catches domain terms not in taxonomy) ---
    if _NLP:
        doc = _NLP(normalised[:500_000])  # cap length for performance
        for chunk in doc.noun_chunks:
            chunk_text = chunk.text.strip()
            if chunk_text in SKILL_TAXONOMY:
                found.add(chunk_text)

    return sorted(found)


# ---------------------------------------------------------------------------
# Quick smoke-test
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    sample = (
        "Experienced data scientist with strong Python and pandas skills. "
        "Built deep learning models using TensorFlow and PyTorch. "
        "Deployed models on AWS with Docker and CI/CD pipelines. "
        "Collaborated using Git and Agile methodologies."
    )
    skills = extract_skills(sample)
    print("Extracted skills:", skills)
