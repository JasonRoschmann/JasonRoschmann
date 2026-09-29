"""Selbsttest des Profil-Stempels: python3 .github/test_profil_stand.py"""
from profil_stand import stempel

D = {"stand": "2026-09-30T05:40:00Z", "erster_merge": "2026-08-07",
     "gemergt": {"gesamt": 59, "flowki": 50, "eigen": 6, "kunden": 3}}
R = "Teamprojekt · <!--pr:flowki-->49<!--/pr--> eigene PRs gemergt\n\n<!--pr-zeile-->alt<!--/pr-zeile-->\n"


def test_setzt_zahl_und_zeile():
    neu = stempel(R, D)
    assert "<!--pr:flowki-->50<!--/pr-->" in neu
    assert ("<!--pr-zeile-->**59 gemergte Pull Requests** seit Aug. 2026 (Flowki Studio 50 · eigene Repos 6 · "
            "Kundenprojekte 3) · Stand 30.09.2026, täglich automatisch gezählt – "
            "[Methodik](https://github.com/JasonRoschmann/cv#wie-die-pr-zahl-entsteht)<!--/pr-zeile-->") in neu


def test_idempotent():
    assert stempel(stempel(R, D), D) == stempel(R, D)


def test_fehlende_marker_sind_fehler():
    try:
        stempel("README ohne Marker", D)
    except ValueError:
        return
    raise AssertionError("README ohne Marker wurde still akzeptiert")


def test_zahl_muss_ganzzahl_sein():
    try:
        stempel(R, {**D, "gemergt": {**D["gemergt"], "gesamt": "59 [Link](https://example.com)"}})
    except ValueError:
        return
    raise AssertionError("Nicht-Zahl aus der JSON landete im README")


if __name__ == "__main__":
    rot = 0
    for name, f in list(globals().items()):
        if name.startswith("test_"):
            try:
                f(); print("OK  ", name)
            except AssertionError as e:
                rot += 1; print("FAIL", name, e)
    raise SystemExit(1 if rot else 0)
