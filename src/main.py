"""
Command line runner for the Music Recommender Simulation.
Run from the project root with:  python -m src.main

Demonstrates:
  Challenge 1 – Extended song features (popularity, era, liveness, speechiness, mood tag)
  Challenge 2 – Four scoring modes: balanced / genre_first / mood_first / energy_focused
  Challenge 3 – Diversity penalty preventing genre/artist monopolies
  Challenge 4 – Tabulate-formatted output table with score breakdown
"""

import os
from tabulate import tabulate
from src.recommender import load_songs, recommend_songs, SCORING_MODES

CSV_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "songs.csv")

# ── User profiles ─────────────────────────────────────────────────────────────

PROFILES = {
    "High-Energy Pop": {
        "genre": "pop", "mood": "happy",
        "energy": 0.85, "valence": 0.82, "danceability": 0.85,
        # Extended (Challenge 1)
        "detailed_mood_tag": "euphoric",
        "preferred_popularity": 80,
        "preferred_decade": 2020,
        "target_liveness": 0.10,
        "target_speechiness": 0.04,
    },
    "Chill Lofi": {
        "genre": "lofi", "mood": "chill",
        "energy": 0.40, "valence": 0.60, "danceability": 0.58,
        "detailed_mood_tag": "dreamy",
        "preferred_popularity": 40,
        "preferred_decade": 2020,
        "target_liveness": 0.07,
        "target_speechiness": 0.03,
    },
    "Deep Intense Rock": {
        "genre": "rock", "mood": "intense",
        "energy": 0.92, "valence": 0.45, "danceability": 0.65,
        "detailed_mood_tag": "aggressive",
        "preferred_popularity": 60,
        "preferred_decade": 2010,
        "target_liveness": 0.20,
        "target_speechiness": 0.05,
    },
}

EDGE_PROFILES = {
    "Classical + Angry + High Energy (conflicting)": {
        "genre": "classical", "mood": "angry",
        "energy": 0.90, "valence": 0.28, "danceability": 0.50,
        "detailed_mood_tag": "aggressive",
        "preferred_popularity": 50,
        "preferred_decade": 2000,
    },
    "K-Pop Fan (genre not in catalog)": {
        "genre": "k-pop", "mood": "happy",
        "energy": 0.80, "valence": 0.85, "danceability": 0.88,
        "detailed_mood_tag": "euphoric",
        "preferred_popularity": 75,
        "preferred_decade": 2020,
    },
    "High Energy + Sad Mood (contradictory vibe)": {
        "genre": "electronic", "mood": "sad",
        "energy": 0.90, "valence": 0.25, "danceability": 0.70,
        "detailed_mood_tag": "melancholic",
        "preferred_popularity": 60,
        "preferred_decade": 2020,
    },
}


# ── Challenge 4: tabulate-based output ────────────────────────────────────────

def print_table(label: str, user_prefs: dict, songs: list,
                mode: str = "balanced", diversity: bool = False, k: int = 5) -> None:
    """Print a formatted recommendation table for one profile."""
    results = recommend_songs(user_prefs, songs, k=k, mode=mode, diversity=diversity)

    mode_label = f"mode={mode}" + (" + diversity" if diversity else "")
    print(f"\n{'─'*72}")
    print(f"  Profile : {label}")
    print(f"  Settings: {mode_label}")
    print(f"  Prefs   : genre={user_prefs['genre']}  mood={user_prefs['mood']}  "
          f"energy={user_prefs['energy']}")
    print(f"{'─'*72}")

    rows = []
    for rank, (song, score, explanation) in enumerate(results, start=1):
        # Truncate explanation to keep table readable
        short_why = explanation[:68] + "…" if len(explanation) > 68 else explanation
        rows.append([
            rank,
            song["title"],
            song["artist"],
            song["genre"],
            song["mood"],
            song["energy"],
            f"{score:.2f}",
            short_why,
        ])

    headers = ["#", "Title", "Artist", "Genre", "Mood", "Energy", "Score", "Why"]
    print(tabulate(rows, headers=headers, tablefmt="rounded_outline"))


# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    songs = load_songs(CSV_PATH)
    print(f"\nLoaded {len(songs)} songs  |  Scoring modes available: {', '.join(SCORING_MODES)}")

    # ── Challenge 2: Show all four modes for one profile ──────────────────────
    print("\n" + "═"*72)
    print("  CHALLENGE 2 — SCORING MODES  (profile: High-Energy Pop)")
    print("═"*72)
    for mode in SCORING_MODES:
        print_table("High-Energy Pop", PROFILES["High-Energy Pop"], songs, mode=mode)

    # ── Standard profiles with extended features (balanced + diversity off) ───
    print("\n" + "═"*72)
    print("  CHALLENGE 1 — EXTENDED FEATURES  (balanced mode, all profiles)")
    print("═"*72)
    for label, prefs in PROFILES.items():
        print_table(label, prefs, songs, mode="balanced")

    # ── Challenge 3: Diversity penalty comparison ─────────────────────────────
    print("\n" + "═"*72)
    print("  CHALLENGE 3 — DIVERSITY PENALTY  (Chill Lofi: off vs on)")
    print("═"*72)
    print_table("Chill Lofi — no diversity", PROFILES["Chill Lofi"], songs, diversity=False)
    print_table("Chill Lofi — diversity ON", PROFILES["Chill Lofi"], songs, diversity=True)

    # ── Adversarial edge cases ─────────────────────────────────────────────────
    print("\n" + "═"*72)
    print("  ADVERSARIAL EDGE CASES  (balanced mode + diversity)")
    print("═"*72)
    for label, prefs in EDGE_PROFILES.items():
        print_table(label, prefs, songs, mode="balanced", diversity=True)


if __name__ == "__main__":
    main()
