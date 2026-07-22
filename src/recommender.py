from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
import csv


@dataclass
class Song:
    """Represents a song and its attributes."""
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
    """Represents a user's taste preferences."""
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool


class Recommender:
    """OOP implementation of the recommendation logic."""

    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Sort songs by score and return top k matches for the user."""
        def score(song: Song) -> float:
            total = 0.0
            if song.genre == user.favorite_genre:
                total += 40
            if song.mood == user.favorite_mood:
                total += 30
            total += 20 * (1 - abs(song.energy - user.target_energy))
            if user.likes_acoustic:
                total += 10 * song.acousticness
            else:
                total += 10 * (1 - song.acousticness)
            return total

        return sorted(self.songs, key=score, reverse=True)[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return a human-readable explanation for why a song was recommended."""
        reasons = []
        if song.genre == user.favorite_genre:
            reasons.append(f"matches your favorite genre ({song.genre})")
        if song.mood == user.favorite_mood:
            reasons.append(f"matches your favorite mood ({song.mood})")
        energy_diff = abs(song.energy - user.target_energy)
        if energy_diff < 0.2:
            reasons.append(
                f"energy {song.energy:.2f} is close to your target {user.target_energy:.2f}"
            )
        if user.likes_acoustic and song.acousticness > 0.6:
            reasons.append(f"high acousticness ({song.acousticness:.2f}) suits your preference")
        if not user.likes_acoustic and song.acousticness < 0.4:
            reasons.append(f"low acousticness ({song.acousticness:.2f}) suits your preference")
        if not reasons:
            reasons.append("general match based on overall profile")
        return "; ".join(reasons)


def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from a CSV file and return a list of dicts with typed values."""
    songs = []
    with open(csv_path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["id"] = int(row["id"])
            row["energy"] = float(row["energy"])
            row["tempo_bpm"] = float(row["tempo_bpm"])
            row["valence"] = float(row["valence"])
            row["danceability"] = float(row["danceability"])
            row["acousticness"] = float(row["acousticness"])
            songs.append(row)
    return songs


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score a single song against user preferences and return (score, reasons)."""
    score = 0.0
    reasons = []

    # Genre match — 40 points
    if song["genre"] == user_prefs["genre"]:
        score += 40
        reasons.append(f"genre match: {song['genre']} (+40 pts)")

    # Mood match — 30 points
    if song["mood"] == user_prefs["mood"]:
        score += 30
        reasons.append(f"mood match: {song['mood']} (+30 pts)")

    # Energy closeness — up to 20 points (linear falloff)
    energy_diff = abs(song["energy"] - user_prefs["energy"])
    energy_score = 20 * (1 - energy_diff)
    score += energy_score
    reasons.append(
        f"energy {song['energy']:.2f} vs target {user_prefs['energy']:.2f} "
        f"(+{energy_score:.1f} pts)"
    )

    # Acousticness fit — up to 10 points
    likes_acoustic = user_prefs.get("likes_acoustic", False)
    if likes_acoustic:
        acoustic_score = 10 * song["acousticness"]
        reasons.append(
            f"acousticness {song['acousticness']:.2f} suits acoustic preference "
            f"(+{acoustic_score:.1f} pts)"
        )
    else:
        acoustic_score = 10 * (1 - song["acousticness"])
        reasons.append(
            f"low acousticness {song['acousticness']:.2f} suits electronic preference "
            f"(+{acoustic_score:.1f} pts)"
        )
    score += acoustic_score

    # Decorative info (not scored)
    reasons.append(
        f"tempo: {song['tempo_bpm']:.0f} BPM | "
        f"danceability: {song['danceability']:.2f} | "
        f"valence: {song['valence']:.2f}"
    )

    return score, reasons


def recommend_songs(
    user_prefs: Dict, songs: List[Dict], k: int = 5
) -> List[Tuple[Dict, float, str]]:
    """Score and rank all songs, returning the top k as (song, score, explanation) tuples."""
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        explanation = " | ".join(reasons)
        scored.append((song, score, explanation))
    # sorted() returns a new list (non-destructive); .sort() would mutate in place
    scored = sorted(scored, key=lambda x: x[1], reverse=True)
    return scored[:k]