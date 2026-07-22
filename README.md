## How The System Works

This is a **content-based recommender** — it scores songs based on how closely 
their attributes match a user's stated taste profile, rather than looking at what 
other users listened to (collaborative filtering). Real platforms like Spotify 
combine both approaches at massive scale; our version focuses purely on song attributes.

### Song features used:
- `genre` — musical category (pop, lofi, rock, etc.)
- `mood` — emotional tone (happy, chill, intense, etc.)
- `energy` — how high-energy the track feels (0.0–1.0)
- `acousticness` — how acoustic vs electronic the song is (0.0–1.0)

### UserProfile stores:
- `favorite_genre` — preferred genre
- `favorite_mood` — preferred mood
- `target_energy` — preferred energy level (0.0–1.0)
- `likes_acoustic` — whether the user prefers acoustic songs

### Scoring Rule (per song, max 100 points):
- Genre match: +40 points
- Mood match: +30 points
- Energy closeness: up to +20 points using `20 * (1 - abs(song.energy - target_energy))`
- Acousticness fit: up to +10 points

### Ranking Rule:
All songs are scored independently, sorted highest to lowest, and the top k are returned.