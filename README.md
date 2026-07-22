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

### Algorithm Recipe (finalized)

| Rule | Points | Logic |
|---|---|---|
| Genre match | 40 | +40 if song.genre == favorite_genre |
| Mood match | 30 | +30 if song.mood == favorite_mood |
| Energy closeness | 20 | 20 × (1 − abs(song.energy − target_energy)) |
| Acousticness fit | 10 | 10 × song.acousticness if likes_acoustic, else 10 × (1 − song.acousticness) |

### Potential Biases
- Genre match dominates at 40 points — a perfect genre match with wrong mood 
  still beats a wrong genre with perfect mood + energy
- With only 18 songs, some genres appear once so users of those genres 
  always get the same top recommendation
- No listen history means the system can't learn or adapt over time


## Sample Recommendation Output

```
User profile: genre=pop, mood=happy, energy=0.8, likes_acoustic=False

Top recommendations:

Sunrise City - Score: 97.80
Because: genre match: pop (+40 pts) | mood match: happy (+30 pts) | energy 0.82 vs target 0.80 (+19.6 pts) | low acousticness 0.18 suits electronic preference (+8.2 pts) | tempo: 118 BPM | danceability: 0.79 | valence: 0.84

Gym Hero - Score: 66.90
Because: genre match: pop (+40 pts) | energy 0.93 vs target 0.80 (+17.4 pts) | low acousticness 0.05 suits electronic preference (+9.5 pts) | tempo: 132 BPM | danceability: 0.88 | valence: 0.77

Levels - Score: 58.00
Because: mood match: happy (+30 pts) | energy 0.88 vs target 0.80 (+18.4 pts) | low acousticness 0.04 suits electronic preference (+9.6 pts) | tempo: 126 BPM | danceability: 0.91 | valence: 0.82

Rooftop Lights - Score: 55.70
Because: mood match: happy (+30 pts) | energy 0.76 vs target 0.80 (+19.2 pts) | low acousticness 0.35 suits electronic preference (+6.5 pts) | tempo: 124 BPM | danceability: 0.82 | valence: 0.81

Golden Hour - Score: 50.90
Because: mood match: happy (+30 pts) | energy 0.62 vs target 0.80 (+16.4 pts) | low acousticness 0.55 suits electronic preference (+4.5 pts) | tempo: 104 BPM | danceability: 0.71 | valence: 0.88
```