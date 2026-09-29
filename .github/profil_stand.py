"""Profil-README: setzt die PR-Zahlen aus pr-stand.json des Web-CVs ein (dieselbe Quelle wie der Lebenslauf).

Aufruf:  python3 .github/profil_stand.py <pr-stand.json> [README.md]
"""
import datetime
import json
import re
import sys
from pathlib import Path

MON_DE = ["Jan.", "Feb.", "März", "Apr.", "Mai", "Juni", "Juli", "Aug.", "Sep.", "Okt.", "Nov.", "Dez."]
METHODIK = "https://github.com/JasonRoschmann/cv#wie-die-pr-zahl-entsteht"
ZAHL = re.compile(r"(<!--pr:([a-z]+)-->)(.*?)(<!--/pr-->)")
ZEILE = re.compile(r"(<!--pr-zeile-->)(.*?)(<!--/pr-zeile-->)")


def _zahl(v) -> int:
    if isinstance(v, bool) or not isinstance(v, int):
        raise ValueError(f"keine Ganzzahl in pr-stand.json: {v!r}")   # nur Zahlen gelangen ins README
    return v


def stempel(text: str, d: dict) -> str:
    g = {k: _zahl(v) for k, v in d["gemergt"].items()}
    t, s = datetime.date.fromisoformat(d["stand"][:10]), datetime.date.fromisoformat(d["erster_merge"][:10])
    zeile = (f"**{g['gesamt']} gemergte Pull Requests** seit {MON_DE[s.month - 1]} {s.year} "
             f"(Flowki Studio {g['flowki']} · eigene Repos {g['eigen']} · Kundenprojekte {g['kunden']}) · "
             f"Stand {t:%d.%m.%Y}, täglich automatisch gezählt – [Methodik]({METHODIK})")
    text, n_zahl = ZAHL.subn(lambda m: m.group(1) + str(g[m.group(2)]) + m.group(4), text)
    text, n_zeile = ZEILE.subn(lambda m: m.group(1) + zeile + m.group(3), text)
    if not (n_zahl and n_zeile):
        raise ValueError("Marker <!--pr:…--> oder <!--pr-zeile--> fehlen im README")
    return text


def main(argv: list[str]) -> int:
    d = json.loads(Path(argv[1]).read_text(encoding="utf-8"))
    readme = Path(argv[2]) if len(argv) > 2 else Path(__file__).resolve().parents[1] / "README.md"
    alt = readme.read_text(encoding="utf-8")
    neu = stempel(alt, d)
    if neu == alt:
        print("README unverändert"); return 0
    readme.write_text(neu, encoding="utf-8")
    print("README aktualisiert:", d["gemergt"]["gesamt"], "gemergte PRs, Stand", d["stand"][:10]); return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
