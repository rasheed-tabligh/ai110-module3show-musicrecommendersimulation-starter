import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass


@dataclass
class Song:
    """Represents a song and its audio attributes loaded from the catalog."""
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float


@dataclass
class UserProfile:
    """Represents a user's declared taste preferences for recommendation matching."""
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool


class Recommender:
    """OOP recommender that scores and ranks songs against a UserProfile."""

    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Score every song against the user profile and return the top-k results."""
        user_prefs = {
            "genre": user.favorite_genre,
            "mood": user.favorite_mood,
            "energy": user.target_energy,
        }
        scored = []
        for song in self.songs:
            song_dict = {
                "genre": song.genre,
                "mood": song.mood,
                "energy": song.energy,
                "valence": song.valence,
                "danceability": song.danceability,
            }
            sc, _ = score_song(user_prefs, song_dict)
            scored.append((song, sc))
        ranked = sorted(scored, key=lambda x: x[1], reverse=True)
        return [song for song, _ in ranked[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return a plain-language explanation of why a song was recommended."""
        user_prefs = {
            "genre": user.favorite_genre,
            "mood": user.favorite_mood,
            "energy": user.target_energy,
        }
        song_dict = {
            "genre": song.genre,
            "mood": song.mood,
            "energy": song.energy,
            "valence": song.valence,
            "danceability": song.danceability,
        }
        _, reasons = score_song(user_prefs, song_dict)
        return "; ".join(reasons) if reasons else "no strong match found"


def load_songs(csv_path: str) -> List[Dict]:
    """Read songs.csv and return a list of dicts with numeric fields cast to float/int."""
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            songs.append({
                "id":           int(row["id"]),
                "title":        row["title"],
                "artist":       row["artist"],
                "genre":        row["genre"],
                "mood":         row["mood"],
                "energy":       float(row["energy"]),
                "tempo_bpm":    float(row["tempo_bpm"]),
                "valence":      float(row["valence"]),
                "danceability": float(row["danceability"]),
                "acousticness": float(row["acousticness"]),
            })
    return songs


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score one song against user preferences; returns (total_score, reasons list)."""
    score = 0.0
    reasons = []

    # Genre exact match: +2.0
    if song.get("genre") == user_prefs.get("genre"):
        score += 2.0
        reasons.append("genre match (+2.0)")

    # Mood exact match: +1.0
    if song.get("mood") == user_prefs.get("mood"):
        score += 1.0
        reasons.append("mood match (+1.0)")

    # Energy proximity: max +2.0  (rewards closeness, not just high/low)
    if "energy" in user_prefs and "energy" in song:
        energy_pts = 2.0 * (1 - abs(user_prefs["energy"] - song["energy"]))
        score += energy_pts
        reasons.append(f"energy proximity (+{energy_pts:.2f})")

    # Valence proximity: max +1.5
    if "valence" in user_prefs and "valence" in song:
        valence_pts = 1.5 * (1 - abs(user_prefs["valence"] - song["valence"]))
        score += valence_pts
        reasons.append(f"valence proximity (+{valence_pts:.2f})")

    # Danceability proximity: max +1.0
    if "danceability" in user_prefs and "danceability" in song:
        dance_pts = 1.0 * (1 - abs(user_prefs["danceability"] - song["danceability"]))
        score += dance_pts
        reasons.append(f"danceability proximity (+{dance_pts:.2f})")

    return (score, reasons)


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Score every song, sort descending by score, return top-k as (song, score, explanation)."""
    scored = []
    for song in songs:
        sc, reasons = score_song(user_prefs, song)
        explanation = "; ".join(reasons) if reasons else "no strong match"
        scored.append((song, sc, explanation))

    # sorted() returns a new list (non-destructive); reverse=True gives highest score first
    ranked = sorted(scored, key=lambda x: x[1], reverse=True)
    return ranked[:k]
