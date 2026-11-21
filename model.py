import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

gifts = pd.read_csv("dataset.csv")

# Text-based ML features
gifts["features"] = (
    gifts["relation"].astype(str) + " " +
    gifts["occasion"].astype(str) + " " +
    gifts["interest"].astype(str)
)

vectorizer = TfidfVectorizer()
feature_matrix = vectorizer.fit_transform(gifts["features"])


def recommend_gifts(relation, occasion, interest, budget, age):

    # Convert selected budget into maximum amount
    budget_limits = {
        "Below ₹500": 500,
        "₹500 - ₹1000": 1000,
        "₹1000 - ₹2000": 2000,
        "₹2000 - ₹5000": 5000,
        "Above ₹5000": 10000
    }

    max_budget = budget_limits.get(budget, 2000)
    age = int(age)

    # Check age and budget eligibility
    eligible = gifts[
        (gifts["budget"] <= max_budget) &
        (gifts["min_age"] <= age) &
        (gifts["max_age"] >= age)
    ].copy()

    if eligible.empty:
        return eligible

    # ML similarity calculation
    user_input = f"{relation} {occasion} {interest}"

    user_vector = vectorizer.transform([user_input])

    scores = cosine_similarity(
        user_vector,
        vectorizer.transform(eligible["features"])
    )[0]

    eligible["score"] = scores

    return eligible.sort_values(
        by="score",
        ascending=False
    ).head(5)[["gift_name", "budget", "score"]]