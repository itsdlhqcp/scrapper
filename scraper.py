import requests
from bs4 import BeautifulSoup
import json

# List of news websites to scrape
URLS = [
    "https://www.nytimes.com/timeswire",
    "https://alterslash.org/",
    "https://www.theatlantic.com/category/washington-week-atlantic/",
    "https://www.theatlantic.com/latest/",
    "https://www.theatlantic.com/ideas/",
    "https://www.theatlantic.com/projects/",
    "https://www.theatlantic.com/politics/",
    "https://www.theatlantic.com/category/fiction/",
    "https://www.theatlantic.com/technology/",
    "https://www.theatlantic.com/science/",
    "https://www.theatlantic.com/economy/",
    "https://www.theatlantic.com/education/",
    "https://www.theatlantic.com/international/",
    "https://www.nytimes.com/section/technology",
    "https://www.nytimes.com/section/sports",
    "https://www.nytimes.com/section/science",
    "https://www.nytimes.com/section/education",
    "https://www.nytimes.com/spotlight/visual-investigations",
    "https://www.nytimes.com/section/world",
    "https://www.nytimes.com/section/opinion"
]

def fetch_articles():
    articles_data = []
    article_id = 1  # Unique ID counter across all sites

    for url in URLS:
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()  # Raise error if request fails
            
            # Parse HTML with BeautifulSoup
            soup = BeautifulSoup(response.text, "html5lib")

            # Extract all <article> elements
            articles = soup.find_all("article")

            for article in articles:
                # Extract Title (Allow varying header levels)
                title_tag = article.select_one("h1 a, h2 a, h3 a")
                title = title_tag.get_text(strip=True) if title_tag else ""

                # Extract Description (Prefer `p.o-dek` if available)
                desc_tag = article.select_one("p.o-dek") or article.find("p")
                description = desc_tag.get_text(strip=True) if desc_tag else ""

                # Extract Author from `li.o-meta__author`
                author_tag = article.select_one("li.o-meta__author")
                author = author_tag.get_text(strip=True) if author_tag else "Unknown Author"

                # Skip articles missing both title and description
                if not title and not description:
                    continue  # Don't include this article in results

                # Store structured data with unique ID
                articles_data.append({
                    "id": article_id,  # Assign unique numeric ID
                    "source": url,  # Track which site the article is from
                    "title": title if title else "No Title",
                    "description": description if description else "No Description",
                    "author": author
                })
                
                article_id += 1  # Increment article ID

        except requests.exceptions.RequestException as e:
            print(f"Error fetching {url}: {e}")

    # Print as JSON (Node.js will read this output)
    print(json.dumps({"articles": articles_data}, indent=2))

if __name__ == "__main__":
    fetch_articles()
