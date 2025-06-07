import requests
from bs4 import BeautifulSoup
import re

def parse_transfer_info(headline):
    to_school = re.search(r'commits? to ([\w\s\'\-]+)', headline, re.IGNORECASE)
    from_school = re.search(r'([\w\s]+) transfer', headline, re.IGNORECASE)
    return {
        "from_school": from_school.group(1).strip() if from_school else "Unknown",
        "to_school": to_school.group(1).strip() if to_school else "Unknown"
    }

def get_transfer_updates():
    try:
        url = "https://www.on3.com/transfer-portal/"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        updates = []
        articles = soup.select("article")

        for article in articles:
            title_tag = article.select_one("h3")
            link_tag = article.find("a", href=True)
            img_tag = article.find("img")

            if not title_tag or not link_tag:
                continue

            title = title_tag.get_text(strip=True)
            link = link_tag["href"]
            image = img_tag["src"] if img_tag and img_tag.get("src") else None

            parsed = parse_transfer_info(title)

            if title == "" or (parsed["from_school"] == "Unknown" and parsed["to_school"] == "Unknown"):
                continue

            updates.append({
                "title": title,
                "sport": "Unknown",
                "from_school": parsed["from_school"],
                "to_school": parsed["to_school"],
                "link": link,
                "image": image
            })

            if len(updates) >= 15:
                break

        return updates

    except Exception as e:
        print(f"Scraper error: {e}")
        return []
