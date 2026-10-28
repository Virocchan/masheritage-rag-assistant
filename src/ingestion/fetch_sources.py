"""Download pages listed in data/sources.csv and save cleaned text to data/processed/.
Check each site's terms of use before running this on it."""
import csv
import pathlib
import time

import requests
from bs4 import BeautifulSoup
from langdetect import detect

OUT = pathlib.Path("data/processed")
OUT.mkdir(parents=True, exist_ok=True)

with open("data/sources.csv", newline="", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))

if not rows:
    print("data/sources.csv is empty. Add at least 3 sources first.")

for row in rows:
    resp = requests.get(row["url"], timeout=30, headers={"User-Agent": "MASHeritage-student-project"})
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    for tag in soup(["script", "style", "nav", "footer"]):
        tag.decompose()
    text = " ".join(soup.get_text(" ").split())
    path = OUT / f"{row['id']}.txt"
    path.write_text(text, encoding="utf-8")
    print(f"{row['id']}: {len(text)} chars, detected language: {detect(text[:2000])}")
    time.sleep(2)  # be polite to servers
