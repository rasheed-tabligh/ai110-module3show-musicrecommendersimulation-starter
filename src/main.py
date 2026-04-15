"""
Command line runner for the Music Recommender Simulation.
Run from the project root with:  python -m src.main
"""

import os
from src.recommender import load_songs, recommend_songs

CSV_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "songs.csv")

# ── Standard profiles ────────────────────────────────────────────────────────
PROFILES = {
    "High-Energy Pop": {
        "genre": "pop", "mood": "happy",
        "energy": 0.85, "valence": 0.82, "danceability": 0.85,
    },
    "Chill Lofi": {
        "genre": "lofi", "mood": "chill",
        "energy": 0.40, "valence": 0.60, "danceability": 0.58,
    },
    "Deep Intense Rock": {
        "genre": "rock", "mood": "intense",
        "energy": 0.92, "valence": 0.45, "danceability": 0.65,
    },
}

# ── Adversarial / edge-case profiles ─────────────────────────────────────────
EDGE_PROFILES = {
    "Classical + Angry + High Energy (conflicting)": {
        "genre": "classical", "mood": "angry",
        "energy": 0.90, "valence": 0.28, "danceability": 0.50,
    },
    "K-Pop Fan (genre not in catalog)": {
        "genre": "k-pop", "mood": "happy",
        "energy": 0.80, "valence": 0.85, "danceability": 0.88,
    },
    "High Energy + Sad Mood (contradictory vibe)": {
        "genre": "electronic", "mood": "sad",
        "energy": 0.90, "valence": 0.25, "danceability": 0.70,
    },
}


def print_recommendations(label: str, user_prefs: dict, songs: list, k: int = 5) -> None:
    """Print a formatted recommendation block for one user profile."""
    recommendations = recommend_songs(user_prefs, songs, k=k)
    print(f"\n{'='*60}")
    print(f"  Profile: {label}")
    print(f"  Prefs:   genre={user_prefs['genre']}  mood={user_prefs['mood']}  "
          f"energy={user_prefs['energy']}")
    print(f"{'='*60}")
    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"\n  #{rank}  {song['title']}  —  {song['artist']}")
        print(f"       Genre: {song['genre']}  |  Mood: {song['mood']}  |  Energy: {song['energy']}")
        print(f"       Score: {score:.2f} / 7.50")
        print(f"       Why:   {explanation}")
    print()


def main() -> None:
    songs = load_songs(CSV_PATH)
    print(f"Loaded {len(songs)} songs from catalog.")

    print("\n" + "─"*60)
    print("  STANDARD PROFILES")
    print("─"*60)
    for label, prefs in PROFILES.items():
        print_recommendations(label, prefs, songs)

    print("\n" + "─"*60)
    print("  ADVERSARIAL / EDGE-CASE PROFILES")
    print("─"*60)
    for label, prefs in EDGE_PROFILES.items():
        print_recommendations(label, prefs, songs)


if __name__ == "__main__":
    main()
