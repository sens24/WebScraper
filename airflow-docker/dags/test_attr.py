import requests
from bs4 import BeautifulSoup

html = requests.get("https://store.steampowered.com/app/730/", timeout=30).text
soup = BeautifulSoup(html, "html.parser")

print("user_reviews_count spans:", len(soup.find_all("span", class_="user_reviews_count")))
for el in soup.find_all("div", class_="user_reviews_summary_row"):
    print("ROW tooltip:", el.get("data-tooltip-html"))
for el in soup.find_all("span", class_="game_review_summary"):
    print("SUMMARY:", el.get_text(strip=True))