"""
Command line runner for the Music Recommender Simulation.
Run from the project root with:  python -m src.main
"""

import os
from src.recommender import load_songs, recommend_songs

CSV_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "songs.csv")


def main() -> None:
    songs = load_songs(CSV_PATH)
    print(f"Loaded {len(songs)} songs from catalog.\n")

    # Example taste profile — edit these to test different users
    user_prefs = {
        "genre":        "pop",
        "mood":         "happy",
        "energy":       0.80,
        "valence":      0.80,
        "danceability": 0.80,
    }

    print("User profile:")
    for key, val in user_prefs.items():
        print(f"  {key}: {val}")

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print(f"\n{'='*52}")
    print(f"  Top {len(recommendations)} Recommendations")
    print(f"{'='*52}")

    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"\n#{rank}  {song['title']}  —  {song['artist']}")
        print(f"    Genre: {song['genre']}  |  Mood: {song['mood']}  |  Energy: {song['energy']}")
        print(f"    Score: {score:.2f} / 7.50")
        print(f"    Why:   {explanation}")

    print(f"\n{'='*52}\n")


if __name__ == "__main__":
    main()
