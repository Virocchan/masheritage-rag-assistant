"""Fetch public official MASHeritage source pages to data/raw/sources.
Review publisher terms before redistribution. This script preserves URLs and SHA-256 provenance.
"""
import csv, hashlib, json, re, time
from datetime import datetime, timezone
from pathlib import Path
import requests
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[2]
REGISTRY = ROOT / "data" / "sources.csv"
OUT = ROOT / "data" / "raw" / "sources"
OUT.mkdir(parents=True, exist_ok=True)

def extract_html(html):
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "noscript", "nav", "footer", "header", "form"]):
        tag.decompose()
    main = soup.find("main") or soup.find("article") or soup.body or soup
    blocks = []
    for node in main.find_all(["h1","h2","h3","h4","p","li","tr","td","th"]):
        s = re.sub(r"\s+", " ", node.get_text(" ", strip=True))
        if s and (not blocks or s != blocks[-1]):
            blocks.append(s)
    return "\n\n".join(blocks).strip()

def main():
    with REGISTRY.open(encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    records, failures = [], []
    for row in rows:
        if row["doc_type"] != "HTML":
            print("SKIP non-HTML source (download/inspect manually):", row["id"])
            continue
        try:
            r = requests.get(row["url"], timeout=40, headers={"User-Agent":"MASHeritage educational research/1.0"})
            r.raise_for_status()
            text = extract_html(r.text)
            if len(text) < 250:
                raise ValueError(f"Only {len(text)} characters extracted; inspect page/pagination")
            p = OUT / f'{row["id"]}.txt'
            p.write_text(text, encoding="utf-8")
            records.append({**row, "local_path":str(p.relative_to(ROOT)),
                "characters":len(text), "sha256":hashlib.sha256(p.read_bytes()).hexdigest(),
                "http_status":r.status_code, "final_url":r.url,
                "fetched_at_utc":datetime.now(timezone.utc).isoformat()})
            print("OK", row["id"], len(text), "characters")
        except Exception as e:
            failures.append({"id":row["id"],"url":row["url"],"error":str(e)})
            print("FAILED", row["id"], e)
        time.sleep(1)
    manifest = {"pipeline_version":"week3-v1",
        "generated_at_utc":datetime.now(timezone.utc).isoformat(),
        "successful_sources":len(records),"failed_sources":failures,"records":records}
    target = ROOT/"data"/"raw"/"source_manifest.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding="utf-8")
    print("Fetched",len(records),"HTML sources. Manifest:",target)
    if len(records) < 2:
        raise RuntimeError("At least two source documents must be fetched successfully")
if __name__ == "__main__":
    main()
