import feedparser
import json
import os
import requests
from datetime import datetime
from typing import List, Dict

# ============== YOUR EXACT RSS FEEDS (copied from your HTML) ==============
RSS_FEEDS = {
    "bbc": "https://feeds.bbci.co.uk/news/rss.xml",
    "reuters": "https://www.reuters.com/rss",
    "infowars": "http://rss.infowars.com/Alex.rss",
    "americaFirst": "https://www.spreaker.com/show/2695413/episodes/feed",
    "fbi": "https://www.fbi.gov/feeds/national-press-releases/RSS",
    "whitehouse": "https://www.whitehouse.gov/feed/",
    "dod": "https://www.defense.gov/News/RSS/",
    "state": "https://www.state.gov/rss-feed/collected-department-releases/feed/",
    "govinfo": "https://www.govinfo.gov/feeds",
    "cia": "https://www.cia.gov/readingroom/rss",
    "ap": "https://apnews.com/rss",
    "fox": "https://feeds.foxnews.com/foxnews/latest",
    "breitbart": "https://feeds.feedburner.com/breitbart",
    "aljazeera": "https://www.aljazeera.com/xml/rss/all.xml",
    "rt": "https://www.rt.com/rss/"
}

CORS_PROXY = "https://api.allorigins.win/raw?url="  # not needed in Python but kept for reference

def fetch_rss(url: str) -> List[Dict]:
    """Fetch and parse one RSS feed"""
    try:
        feed = feedparser.parse(url)
        items = []
        for entry in feed.entries[:8]:  # limit per feed like your JS
            items.append({
                "title": entry.title or "Untitled",
                "link": entry.link or "#",
                "pubDate": entry.published or entry.updated or datetime.utcnow().isoformat(),
                "source": list(RSS_FEEDS.keys())[list(RSS_FEEDS.values()).index(url)] if url in RSS_FEEDS.values() else "unknown"
            })
        return items
    except Exception:
        return []

def call_groq_ai(prompt: str) -> str:
    """Call free Groq AI (fastest in 2026)"""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("⚠️ No GROQ_API_KEY found - using simulation")
        return "Simulation mode: Palantir wins $2.4B DoD contract | JD Vance meets Kushner family"

    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "llama-3.3-70b-versatile",   # excellent free model
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.7,
                "max_tokens": 1500
            },
            timeout=30
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"AI call failed: {e}")
        return "Simulation mode: Palantir wins $2.4B DoD contract | JD Vance meets Kushner family"

def main():
    print("🚀 NEXUS OS AI Swarm Starting...")

    # 1. Fetch all headlines from your 15 sources
    all_headlines = []
    for name, url in RSS_FEEDS.items():
        print(f"Fetching {name}...")
        items = fetch_rss(url)
        all_headlines.extend(items)
        print(f"   → {len(items)} headlines from {name}")

    # 2. Build a strong AI prompt (follows best practices from your document)
    prompt = f"""
You are the NEXUS OS AI Swarm. Analyze the following recent headlines and generate fresh dashboard data.

HEADLINES:
{json.dumps(all_headlines[:50], indent=2)}

Generate JSON with this exact structure (no extra text):
{{
  "last_updated": "{datetime.utcnow().isoformat()}",
  "headlines": [ array of 12-20 objects with title, link, source ],
  "marketData": [ array of 20 objects like: {{"symbol":"PLTR", "name":"Palantir", "price":42.85, "change":4.8, "prediction":"Bullish", "confidence":92, "reason":"..."}} ],
  "conspiracy_notes": ["short analysis lines with Infowars divergence flags"],
  "events": ["2-3 recent event strings"],
  "lessons": ["2-3 swarm lessons"]
}}

Be realistic, include Palantir / Vance / defense / crypto themes where appropriate. Use Infowars as one perspective but flag divergences.
"""

    # 3. Get AI insights
    ai_response = call_groq_ai(prompt)
    print("✅ AI analysis complete")

    # 4. Fallback / parse into structured data
    try:
        # Try to extract JSON from AI response
        import re
        json_match = re.search(r'\{.*\}', ai_response, re.DOTALL)
        dashboard_data = json.loads(json_match.group(0)) if json_match else {}
    except:
        dashboard_data = {}

    # 5. Ensure required structure (fallback to your original simulation data)
    if not dashboard_data.get("headlines"):
        dashboard_data["headlines"] = all_headlines[:20] or [
            {"title": "Palantir wins $2.4B DoD contract", "link": "#", "source": "infowars"},
            {"title": "JD Vance meets with Kushner family", "link": "#", "source": "reuters"}
        ]

    if not dashboard_data.get("marketData"):
        dashboard_data["marketData"] = [  # your original rich market data as fallback
            {"symbol":"PLTR", "name":"Palantir", "price":42.85, "change":4.8, "prediction":"Bullish", "confidence":92, "reason":"DoD + Vance leverage"},
            # ... (you can keep expanding or let AI override)
        ]

    dashboard_data["last_updated"] = datetime.utcnow().isoformat()

    # 6. Save to data/dashboard-data.json
    os.makedirs("data", exist_ok=True)
    with open("data/dashboard-data.json", "w", encoding="utf-8") as f:
        json.dump(dashboard_data, f, indent=2, ensure_ascii=False)

    print("✅ dashboard-data.json updated successfully")
    print(f"   Total headlines: {len(dashboard_data.get('headlines', []))}")

if __name__ == "__main__":
    main()
