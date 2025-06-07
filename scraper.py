import requests
from bs4 import BeautifulSoup
import re

def parse_transfer_info(headline):
    """
    Extracts from_school and to_school from a headline string.
    Returns a dictionary with parsed values or 'Unknown'.
    """
    to_school = re.search(r'commits? to ([\w\s\'\-]+)', headline, re.IGNORECASE)
    from_school = re.search(r'([\w\s]+) transfer', headline, re.IGNORECASE)

    return {
        "from_school": from_school.group(1).strip() if from_school else "Unknown",
        "to_school": to_school.group(1).strip() if to_school else "Unknown"
    }

def get_transfer_updates():
    """
    Scrapes the On3 transfer portal site and returns a clean list of transfer updates.
    """
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

            if not title_tag or not link_tag:
                continue  # Skip malformed items

            title = title_tag.get_text(strip=True)
            link = link_tag["href"]

            parsed = parse_transfer_info(title)

            # Skip updates with no real content
            if title == "" or (parsed["from_school"] == "Unknown" and parsed["to_school"] == "Unknown"):
                continue

            updates.append({
                "title": title,
                "sport": "Unknown",  # You can extract position/sport later
                "from_school": parsed["from_school"],
                "to_school": parsed["to_school"],
                "link": link
            })

            if len(updates) >= 15:  # Get 15 solid entries
                break

        return updates

    except Exception as e:
        print(f"Scraper error: {e}")
        return []
