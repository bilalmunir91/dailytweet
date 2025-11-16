

import os
import random
import requests
from datetime import datetime
from pytrends.request import TrendReq

X_BEARER_TOKEN = os.environ.get("X_BEARER_TOKEN")
X_POST_URL = "https://api.x.com/2/tweets"

def get_trending_topic(country_code: str = "US") -> str:
    pytrend = TrendReq()
    try:
        df = pytrend.today_searches(pn=country_code)
        topics = df[0].tolist() if not df.empty else []
    except Exception:
        topics = []
    if not topics:
        return "AI"
    subset = topics[:10] if len(topics) >= 10 else topics
    return random.choice(subset)

def build_prediction(topic: str) -> str:
    templates = [
        "Prediction: {topic} will be everywhere this week.",
        "Prediction: {topic} hype will rise in the next 48 hours.",
        "Prediction: everyone will be talking about {topic} soon.",
        "Prediction: memes about {topic} will explode.",
        "Prediction: {topic} will fade in days, but screenshots will live forever."
    ]
    return random.choice(templates).format(topic=topic)

def build_tweet(topic: str) -> str:
    today = datetime.utcnow().strftime("%Y-%m-%d")
    prediction = build_prediction(topic)
    tweet = (
        f"🔥 Today’s Trending Topic ({today}): {topic}\n\n"
        f"{prediction}\n\n"
        f"#trending #prediction"
    )
    if len(tweet) > 280:
        tweet = f"Trending: {topic}\n{prediction}"
    return tweet

def post_to_x(text: str) -> dict:
    if not X_BEARER_TOKEN:
        raise RuntimeError("X_BEARER_TOKEN not set")
    headers = {
        "Authorization": f"Bearer {X_BEARER_TOKEN}",
        "Content-Type": "application/json",
    }
    payload = {"text": text}
    resp = requests.post(X_POST_URL, headers=headers, json=payload, timeout=10)
    try:
        return resp.json()
    except Exception:
        return {"error": resp.text, "status": resp.status_code}

def main():
    country = os.environ.get("TREND_COUNTRY", "US")
    topic = get_trending_topic(country)
    tweet = build_tweet(topic)
    print("Tweet content:\n", tweet)
    result = post_to_x(tweet)
    print("Posted:", result)

if __name__ == "__main__":
    main()

