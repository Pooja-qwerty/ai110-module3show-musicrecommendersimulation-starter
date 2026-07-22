"""
Command line runner for the Music Recommender Simulation.
"""

from src.recommender import load_songs, recommend_songs


def print_recommendations(label: str, user_prefs: dict, songs: list, k: int = 5):
    """Print top k recommendations for a given user profile."""
    print(f"\n{'='*60}")
    print(f"Profile: {label}")
    print(f"Prefs: {user_prefs}")
    print(f"{'='*60}")
    recommendations = recommend_songs(user_prefs, songs, k=k)
    for i, (song, score, explanation) in enumerate(recommendations, 1):
        print(f"\n{i}. {song['title']} by {song['artist']} — Score: {score:.2f}")
        print(f"   Because: {explanation}")


def main() -> None:
    songs = load_songs("data/songs.csv")

    profiles = {
        "High-Energy Pop": {
            "genre": "pop", "mood": "happy", "energy": 0.8, "likes_acoustic": False
        },
        "Chill Lofi": {
            "genre": "lofi", "mood": "chill", "energy": 0.4, "likes_acoustic": True
        },
        "Intense Rock": {
            "genre": "rock", "mood": "intense", "energy": 0.9, "likes_acoustic": False
        },
        "Edge Case — High Energy but Sad": {
            "genre": "ambient", "mood": "moody", "energy": 0.9, "likes_acoustic": True
        },
    }

    for label, prefs in profiles.items():
        print_recommendations(label, prefs, songs)


if __name__ == "__main__":
    main()