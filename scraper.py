import requests
from bs4 import BeautifulSoup
import re

def parse_transfer_info(headline):
    to_school = re.search(r'commits? to ([\w\s\'\-]+)', headline, re.IGNORECASE)
    from_school = re.search(r'([A-Z][\w\s]+) transfer', headline)

    return {
        "from_school": from_school.group(1).strip() if from_school else "Unknown",
        "to_school": to_school.group(1).strip() if to_school else "Unknown"
    }

def get_transfer_updates():
    try:
        url = "https://www.on3.com/transfer-portal/"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        updates = []

        for article in soup.select("article")[:20]:
            title_tag = article.select_one("h3")
            link_tag = article.find("a", href=True)

            title = title_tag.text.strip() if title_tag else "Unnamed"
            link = link_tag["href"] if link_tag else "#"

            parsed = parse_transfer_info(title)

            updates.append({
                "title": title,
                "sport": "Unknown",
                "from_school": parsed["from_school"],
                "to_school": parsed["to_school"],
                "link": link
            })

        return updates
    except Exception as e:
        print(f"Scraper failed: {e}")
        return []
