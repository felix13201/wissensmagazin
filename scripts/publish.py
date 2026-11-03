#!/usr/bin/env python3
"""Create and publish one researched German magazine issue using OpenAI Responses API."""
import datetime as dt
import json
import os
import pathlib
import re
import sys
import urllib.error
import urllib.request
from zoneinfo import ZoneInfo

ROOT = pathlib.Path(__file__).resolve().parent.parent
ARCHIVE = ROOT / "articles.json"
NOW = dt.datetime.now(ZoneInfo("Europe/Berlin"))
TODAY = NOW.date().isoformat()

def request(payload):
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        "https://api.openai.com/v1/responses",
        data=data,
        headers={
            "Authorization": "Bearer " + os.environ["OPENAI_API_KEY"],
            "Content-Type": "application/json",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=240) as response:
        return json.load(response)

def extract(response):
    pieces = []
    for item in response.get("output", []):
        if item.get("type") == "message":
            for part in item.get("content", []):
                if part.get("type") == "output_text":
                    pieces.append(part.get("text", ""))
    return "\n".join(pieces).strip()

def main():
    if os.environ.get("CHECK_HOUR") == "1" and NOW.hour != 18:
        print("Not 18:00 Europe/Berlin; skipping.")
        return
    items = json.loads(ARCHIVE.read_text(encoding="utf-8"))
    if any(a.get("date") == TODAY for a in items):
        print("Issue already exists for", TODAY)
        return
    recent = [a["title"] for a in sorted(items, key=lambda x: x["date"], reverse=True)[:25]]
    prompt = (
        "Verfasse eine eigenständige, journalistisch sorgfältige deutsche Wissenschaftsreportage "
        "mit 3500 bis 4000 Wörtern, lebendigem Einstieg, 8–14 Kapiteln, nachvollziehbaren "
        "wissenschaftlichen Erklärungen, expliziten Unsicherheiten, Quellen und 3 Reflexionsfragen. "
        "Wähle ein überraschendes Thema aus Medizin, Linguistik, Psychologie, Geopolitik, "
        "Rhetorik, Geschichte, Biologie, Mathematik oder Gesellschaft; variiere die Disziplinen. "
        "Kein Fokus auf KI/IT, Gehirnentscheidungen oder Halbleiter. "
        "Recherchiere mittels Websuche und verwende nur überprüfbare Quellen. "
        "Setze am Schluss einen Abschnitt 'Quellen und weiterführende Literatur' mit "
        "aussagekräftigen Links. Gib AUSSCHLIESSLICH valides JSON zurück, ohne Markdown-Codezaun: "
        '{"title":"...","subtitle":"...","category":"...","content":"Markdown mit # und ## Überschriften, Absätzen, Quellen und Reflexionsfragen"}'
        "\nBisherige Themen (nicht wiederholen): " + "; ".join(recent)
    )
    payload = {
        "model": os.environ.get("OPENAI_MODEL", "gpt-5.1"),
        "tools": [{"type": "web_search"}],
        "input": prompt,
        "max_output_tokens": 14000,
    }
    response = request(payload)
    raw = extract(response)
    raw = re.sub(r"^\\s*```(?:json)?\\s*|\\s*```\\s*$", "", raw)
    try:
        article = json.loads(raw)
    except json.JSONDecodeError:
        print("Model did not return valid JSON. Nothing published.", file=sys.stderr)
        sys.exit(1)
    for field in ("title", "subtitle", "category", "content"):
        if not isinstance(article.get(field), str) or not article[field].strip():
            sys.exit("Missing required field: " + field)
    words = len(article["content"].split())
    if not 3500 <= words <= 4000:
        sys.exit(f"Article has {words} words; expected 3500-4000. Not published.")
    article["id"] = TODAY
    article["date"] = TODAY
    article["status"] = "full"
    items.insert(0, article)
    ARCHIVE.write_text(json.dumps(items, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Prepared {TODAY}: {article['title']} ({words} words)")

if __name__ == "__main__":
    main()
