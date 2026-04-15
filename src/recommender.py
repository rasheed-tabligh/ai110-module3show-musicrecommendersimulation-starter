import csv
from typing import List, Dict, Tuple
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
    # Challenge 1: extended attributes (default values keep existing tests passing)
    popularity: int = 50
    release_decade: int = 2020
    liveness: float = 0.10
    speechiness: float = 0.05
    detailed_mood_tag: str = ""


@dataclass
class UserProfile:
    """Represents a user's declared taste preferences for recommendation matching."""
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool


# ── Challenge 2: Scoring mode weight presets ─────────────────────────────────
# Each mode re-weights the five core features. Max base score per mode:
#   balanced      → 2.0+1.0+2.0+1.5+1.0 = 7.5
#   genre_first   → 4.0+1.0+1.0+0.75+0.5 = 7.25
#   mood_first    → 1.0+3.0+1.0+1.5+0.5 = 7.0
#   energy_focused→ 1.0+0.5+4.0+1.0+1.0 = 7.5
SCORING_MODES: Dict[str, Dict[str, float]] = {
    "balanced": {
        "genre": 2.0, "mood": 1.0, "energy": 2.0,
        "valence": 1.5, "danceability": 1.0,
    },
    "genre_first": {
        "genre": 4.0, "mood": 1.0, "energy": 1.0,
        "valence": 0.75, "danceability": 0.5,
    },
    "mood_first": {
        "genre": 1.0, "mood": 3.0, "energy": 1.0,
        "valence": 1.5, "danceability": 0.5,
    },
    "energy_focused": {
        "genre": 1.0, "mood": 0.5, "energy": 4.0,
        "valence": 1.0, "danceability": 1.0,
    },
}


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
                "genre": song.genre, "mood": song.mood,
                "energy": song.energy, "valence": song.valence,
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
            "genre": song.genre, "mood": song.mood,
            "energy": song.energy, "valence": song.valence,
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
            song: Dict = {
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
            }
            # Challenge 1: parse extended columns if present
            if "popularity"        in row: song["popularity"]        = int(row["popularity"])
            if "release_decade"    in row: song["release_decade"]    = int(row["release_decade"])
            if "liveness"          in row: song["liveness"]          = float(row["liveness"])
            if "speechiness"       in row: song["speechiness"]       = float(row["speechiness"])
            if "detailed_mood_tag" in row: song["detailed_mood_tag"] = row["detailed_mood_tag"]
            songs.append(song)
    return songs


def score_song(
    user_prefs: Dict,
    song: Dict,
    mode: str = "balanced",
) -> Tuple[float, List[str]]:
    """
    Score one song against user preferences.

    Challenge 2: mode selects weight preset from SCORING_MODES.
    Challenge 1: scores extended features when present in both user_prefs and song.
    Returns (total_score, reasons_list).
    """
    weights = SCORING_MODES.get(mode, SCORING_MODES["balanced"])
    score = 0.0
    reasons: List[str] = []

    # ── Core features ─────────────────────────────────────────────────────────

    if song.get("genre") == user_prefs.get("genre"):
        pts = weights["genre"]
        score += pts
        reasons.append(f"genre match (+{pts:.1f})")

    if song.get("mood") == user_prefs.get("mood"):
        pts = weights["mood"]
        score += pts
        reasons.append(f"mood match (+{pts:.1f})")

    if "energy" in user_prefs and "energy" in song:
        pts = weights["energy"] * (1 - abs(user_prefs["energy"] - song["energy"]))
        score += pts
        reasons.append(f"energy proximity (+{pts:.2f})")

    if "valence" in user_prefs and "valence" in song:
        pts = weights["valence"] * (1 - abs(user_prefs["valence"] - song["valence"]))
        score += pts
        reasons.append(f"valence proximity (+{pts:.2f})")

    if "danceability" in user_prefs and "danceability" in song:
        pts = weights["danceability"] * (1 - abs(user_prefs["danceability"] - song["danceability"]))
        score += pts
        reasons.append(f"danceability proximity (+{pts:.2f})")

    # ── Challenge 1: Extended feature scoring ─────────────────────────────────

    # Detailed mood tag exact match: +0.50
    if user_prefs.get("detailed_mood_tag") and song.get("detailed_mood_tag"):
        if song["detailed_mood_tag"] == user_prefs["detailed_mood_tag"]:
            score += 0.50
            reasons.append("detailed mood tag match (+0.50)")

    # Popularity proximity (user supplies preferred_popularity 0–100): max +0.50
    if "preferred_popularity" in user_prefs and "popularity" in song:
        pts = 0.50 * (1 - abs(user_prefs["preferred_popularity"] - song["popularity"]) / 100)
        score += pts
        reasons.append(f"popularity match (+{pts:.2f})")

    # Release decade proximity (user supplies preferred_decade e.g. 2020): max +0.50
    # Gap normalised over 50 years so a 50-year span scores 0.
    if "preferred_decade" in user_prefs and "release_decade" in song:
        gap = abs(user_prefs["preferred_decade"] - song["release_decade"])
        pts = 0.50 * (1 - min(gap, 50) / 50)
        score += pts
        reasons.append(f"era match (+{pts:.2f})")

    # Liveness proximity (user supplies target_liveness 0–1): max +0.50
    if "target_liveness" in user_prefs and "liveness" in song:
        pts = 0.50 * (1 - abs(user_prefs["target_liveness"] - song["liveness"]))
        score += pts
        reasons.append(f"liveness proximity (+{pts:.2f})")

    # Speechiness proximity (user supplies target_speechiness 0–1): max +0.50
    if "target_speechiness" in user_prefs and "speechiness" in song:
        pts = 0.50 * (1 - abs(user_prefs["target_speechiness"] - song["speechiness"]))
        score += pts
        reasons.append(f"speechiness proximity (+{pts:.2f})")

    return (score, reasons)


def apply_diversity_penalty(
    scored: List[Tuple[Dict, float, str]],
    max_per_genre: int = 2,
    max_per_artist: int = 1,
) -> List[Tuple[Dict, float, str]]:
    """
    Challenge 3: Re-score to prevent any genre or artist dominating the top results.

    Works by iterating through the pre-sorted list and applying:
      -1.00 per extra song beyond max_per_genre slots used by that genre
      -0.75 per extra song beyond max_per_artist slots used by that artist
    The list is then re-sorted so penalised songs fall behind fresh ones.
    """
    genre_counts: Dict[str, int] = {}
    artist_counts: Dict[str, int] = {}
    penalised = []

    for song, sc, explanation in sorted(scored, key=lambda x: x[1], reverse=True):
        genre  = song.get("genre", "")
        artist = song.get("artist", "")
        penalty = 0.0

        if genre_counts.get(genre, 0) >= max_per_genre:
            penalty += 1.00
        if artist_counts.get(artist, 0) >= max_per_artist:
            penalty += 0.75

        genre_counts[genre]   = genre_counts.get(genre, 0) + 1
        artist_counts[artist] = artist_counts.get(artist, 0) + 1

        new_explanation = explanation
        if penalty > 0:
            new_explanation += f"; diversity penalty (-{penalty:.2f})"

        penalised.append((song, sc - penalty, new_explanation))

    return sorted(penalised, key=lambda x: x[1], reverse=True)


def recommend_songs(
    user_prefs: Dict,
    songs: List[Dict],
    k: int = 5,
    mode: str = "balanced",
    diversity: bool = False,
) -> List[Tuple[Dict, float, str]]:
    """
    Score every song, apply optional diversity penalty, sort descending, return top-k.

    Args:
        user_prefs: feature dict including optional extended keys.
        songs:      catalog loaded by load_songs().
        k:          number of results to return.
        mode:       scoring weight preset — 'balanced', 'genre_first',
                    'mood_first', or 'energy_focused'.
        diversity:  if True, apply genre/artist diversity penalty before ranking.
    """
    scored = []
    for song in songs:
        sc, reasons = score_song(user_prefs, song, mode=mode)
        explanation = "; ".join(reasons) if reasons else "no strong match"
        scored.append((song, sc, explanation))

    if diversity:
        scored = apply_diversity_penalty(scored)

    return sorted(scored, key=lambda x: x[1], reverse=True)[:k]
