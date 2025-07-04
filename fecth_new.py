import os
import random
import requests
from dotenv import load_dotenv
from newspaper import Article

# Load API key
load_dotenv()
api_key = os.getenv("NEWS_API_KEY")
if not api_key:
    raise ValueError("Missing NEWS_API_KEY in .env")

# --- Categories ---
categories = ["technology", "science", "general", "business","world", "nation", "entertainment", "sports","current_affairs"]
country = "us"

def get_full_article(url):
    try:
        article = Article(url)
        article.download()
        article.parse()
        return article.title, article.text[:6000]
    except Exception as e:
        return None, None

def main():
    chosen_category = random.choice(categories)
    print(f"🔍 Random category selected: {chosen_category}")

    # Step 1: Fetch one article from that category
    top_url = "https://newsapi.org/v2/top-headlines"
    params = {
        "country": country,
        "category": chosen_category,
        "pageSize": 1,
        "apiKey": api_key
    }
    resp = requests.get(top_url, params=params).json()
    articles = resp.get("articles", [])
    if not articles:
        print("❌ No articles found.")
        return

    selected = articles[0]
    url = selected.get("url")

    # Step 2: Get full content of the article
    title, text = get_full_article(url)
    if not title or not text:
        print("❌ Failed to extract article.")
        return

    # Step 3: Write to file
    with open("news_full.txt", "w", encoding="utf-8") as f:
        f.write(f"Title: {title}\n")
        f.write(f"URL: {url}\n\n")
        f.write(text + "\n")

    print("✅ Saved full article to news_full.txt")

if __name__ == "__main__":
    main()
