"""
recommendations.py
==================
Maps missing skills to curated, real-world learning resources.

Each entry in COURSE_CATALOG contains:
    - skill (str)       : skill keyword to match against
    - course (str)      : human-readable course / resource title
    - platform (str)    : hosting platform name
    - url (str)         : direct link to the resource
    - level (str)       : Beginner | Intermediate | Advanced

The matching is case-insensitive and uses substring / keyword lookup so that
"deep learning" matches a catalog entry keyed by "deep learning" even if the
missing skill was extracted slightly differently.
"""

from __future__ import annotations

# ---------------------------------------------------------------------------
# Course catalog — extend freely!
# ---------------------------------------------------------------------------

COURSE_CATALOG: list[dict] = [
    # Python
    {
        "skill": "python",
        "course": "Python for Everybody Specialization",
        "platform": "Coursera",
        "url": "https://www.coursera.org/specializations/python",
        "level": "Beginner",
    },
    {
        "skill": "python",
        "course": "Automate the Boring Stuff with Python",
        "platform": "Free Online Book",
        "url": "https://automatetheboringstuff.com/",
        "level": "Beginner",
    },

    # Machine Learning / Deep Learning
    {
        "skill": "machine learning",
        "course": "Machine Learning Specialization",
        "platform": "Coursera (Andrew Ng)",
        "url": "https://www.coursera.org/specializations/machine-learning-introduction",
        "level": "Beginner",
    },
    {
        "skill": "deep learning",
        "course": "Deep Learning Specialization",
        "platform": "Coursera (Andrew Ng)",
        "url": "https://www.coursera.org/specializations/deep-learning",
        "level": "Intermediate",
    },
    {
        "skill": "natural language processing",
        "course": "NLP with Classification and Vector Spaces",
        "platform": "Coursera",
        "url": "https://www.coursera.org/learn/classification-vector-spaces-in-nlp",
        "level": "Intermediate",
    },
    {
        "skill": "nlp",
        "course": "Hugging Face NLP Course (Free)",
        "platform": "Hugging Face",
        "url": "https://huggingface.co/course",
        "level": "Intermediate",
    },
    {
        "skill": "computer vision",
        "course": "Convolutional Neural Networks (Deep Learning #4)",
        "platform": "Coursera",
        "url": "https://www.coursera.org/learn/convolutional-neural-networks",
        "level": "Intermediate",
    },

    # ML Frameworks
    {
        "skill": "tensorflow",
        "course": "TensorFlow Developer Certificate",
        "platform": "Google / Coursera",
        "url": "https://www.coursera.org/professional-certificates/tensorflow-in-practice",
        "level": "Intermediate",
    },
    {
        "skill": "pytorch",
        "course": "PyTorch for Deep Learning Bootcamp",
        "platform": "Udemy",
        "url": "https://www.udemy.com/course/pytorch-for-deep-learning/",
        "level": "Intermediate",
    },
    {
        "skill": "scikit-learn",
        "course": "Hands-On Machine Learning with Scikit-Learn, Keras & TensorFlow",
        "platform": "O'Reilly (Book)",
        "url": "https://www.oreilly.com/library/view/hands-on-machine-learning/9781492032632/",
        "level": "Intermediate",
    },

    # Cloud
    {
        "skill": "aws",
        "course": "AWS Certified Solutions Architect – Associate",
        "platform": "AWS Training",
        "url": "https://aws.amazon.com/certification/certified-solutions-architect-associate/",
        "level": "Intermediate",
    },
    {
        "skill": "azure",
        "course": "Microsoft Azure Fundamentals (AZ-900)",
        "platform": "Microsoft Learn",
        "url": "https://learn.microsoft.com/en-us/certifications/azure-fundamentals/",
        "level": "Beginner",
    },
    {
        "skill": "google cloud",
        "course": "Google Cloud Fundamentals: Core Infrastructure",
        "platform": "Google Cloud Skills Boost",
        "url": "https://www.cloudskillsboost.google/course_templates/60",
        "level": "Beginner",
    },
    {
        "skill": "gcp",
        "course": "Google Cloud Fundamentals: Core Infrastructure",
        "platform": "Google Cloud Skills Boost",
        "url": "https://www.cloudskillsboost.google/course_templates/60",
        "level": "Beginner",
    },

    # DevOps
    {
        "skill": "docker",
        "course": "Docker Mastery: with Kubernetes + Swarm",
        "platform": "Udemy",
        "url": "https://www.udemy.com/course/docker-mastery/",
        "level": "Beginner",
    },
    {
        "skill": "kubernetes",
        "course": "Kubernetes for the Absolute Beginners",
        "platform": "Udemy",
        "url": "https://www.udemy.com/course/learn-kubernetes/",
        "level": "Beginner",
    },
    {
        "skill": "ci/cd",
        "course": "GitHub Actions – The Complete Guide",
        "platform": "Udemy",
        "url": "https://www.udemy.com/course/github-actions-the-complete-guide/",
        "level": "Intermediate",
    },

    # Databases
    {
        "skill": "sql",
        "course": "The Complete SQL Bootcamp",
        "platform": "Udemy",
        "url": "https://www.udemy.com/course/the-complete-sql-bootcamp/",
        "level": "Beginner",
    },
    {
        "skill": "mongodb",
        "course": "MongoDB Basics (M001)",
        "platform": "MongoDB University (Free)",
        "url": "https://university.mongodb.com/courses/M001/about",
        "level": "Beginner",
    },
    {
        "skill": "nosql",
        "course": "MongoDB Basics (M001)",
        "platform": "MongoDB University (Free)",
        "url": "https://university.mongodb.com/courses/M001/about",
        "level": "Beginner",
    },
    {
        "skill": "postgresql",
        "course": "The Complete Python & PostgreSQL Developer Course",
        "platform": "Udemy",
        "url": "https://www.udemy.com/course/the-complete-python-postgresql-developer-course/",
        "level": "Beginner",
    },

    # Web
    {
        "skill": "react",
        "course": "React – The Complete Guide",
        "platform": "Udemy",
        "url": "https://www.udemy.com/course/react-the-complete-guide-incl-redux/",
        "level": "Intermediate",
    },
    {
        "skill": "typescript",
        "course": "Understanding TypeScript",
        "platform": "Udemy",
        "url": "https://www.udemy.com/course/understanding-typescript/",
        "level": "Intermediate",
    },
    {
        "skill": "graphql",
        "course": "GraphQL with React: The Complete Developers Guide",
        "platform": "Udemy",
        "url": "https://www.udemy.com/course/graphql-with-react-course/",
        "level": "Intermediate",
    },

    # Data Engineering
    {
        "skill": "apache spark",
        "course": "Apache Spark with Python – Big Data with PySpark",
        "platform": "Udemy",
        "url": "https://www.udemy.com/course/apache-spark-with-python-big-data-with-pyspark-and-scala/",
        "level": "Intermediate",
    },
    {
        "skill": "kafka",
        "course": "Apache Kafka Series – Learn Apache Kafka for Beginners",
        "platform": "Udemy",
        "url": "https://www.udemy.com/course/apache-kafka/",
        "level": "Intermediate",
    },
    {
        "skill": "airflow",
        "course": "The Complete Hands-On Course to Master Apache Airflow",
        "platform": "Udemy",
        "url": "https://www.udemy.com/course/the-complete-hands-on-course-to-master-apache-airflow/",
        "level": "Intermediate",
    },
    {
        "skill": "dbt",
        "course": "dbt (Data Build Tool) – Fundamentals",
        "platform": "dbt Learn (Free)",
        "url": "https://courses.getdbt.com/courses/fundamentals",
        "level": "Beginner",
    },

    # Soft skills
    {
        "skill": "leadership",
        "course": "Inspiring and Motivating Individuals",
        "platform": "Coursera",
        "url": "https://www.coursera.org/learn/motivate-people-teams",
        "level": "Beginner",
    },
    {
        "skill": "project management",
        "course": "Google Project Management Certificate",
        "platform": "Coursera",
        "url": "https://www.coursera.org/professional-certificates/google-project-management",
        "level": "Beginner",
    },

    # Fallback generic resource
    {
        "skill": "__default__",
        "course": "LinkedIn Learning – Skill Development Library",
        "platform": "LinkedIn Learning",
        "url": "https://www.linkedin.com/learning/",
        "level": "Varies",
    },
]


# ---------------------------------------------------------------------------
# Matching logic
# ---------------------------------------------------------------------------

def _find_entry(skill: str) -> dict | None:
    """Return the best catalog entry for *skill*, or None."""
    skill_lower = skill.lower()
    for entry in COURSE_CATALOG:
        catalog_key = entry["skill"].lower()
        if catalog_key == "__default__":
            continue
        # Substring match in both directions for flexibility
        if catalog_key in skill_lower or skill_lower in catalog_key:
            return entry
    return None


def get_recommendations(missing_skills: list[str]) -> list[dict]:
    """
    Generate course recommendations for a list of missing skills.

    Parameters
    ----------
    missing_skills : list[str]
        Skills the candidate lacks relative to the job description.

    Returns
    -------
    list[dict]
        Each item: {"skill", "course", "platform", "url", "level"}
        Up to one recommendation per missing skill, de-duplicated by course URL.
        Falls back to a generic resource if no specific entry is found.
    """
    recommendations: list[dict] = []
    seen_urls: set[str] = set()

    for skill in missing_skills:
        entry = _find_entry(skill)
        if entry is None:
            # Use generic fallback, labelled with the specific skill
            fallback = next(e for e in COURSE_CATALOG if e["skill"] == "__default__")
            entry = {**fallback, "skill": skill}

        if entry["url"] not in seen_urls:
            recommendations.append({
                "skill":    skill,
                "course":   entry["course"],
                "platform": entry["platform"],
                "url":      entry["url"],
                "level":    entry["level"],
            })
            seen_urls.add(entry["url"])

    return recommendations


# ---------------------------------------------------------------------------
# Quick smoke-test
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    missing = ["kubernetes", "kafka", "deep learning", "typescript", "unknown-skill"]
    recs = get_recommendations(missing)
    for r in recs:
        print(f"[{r['level']}] {r['skill']} → {r['course']} ({r['platform']})")
