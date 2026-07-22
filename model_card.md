# 🎧 Model Card: VibeFinder 1.0

## 1. Model Name

**VibeFinder 1.0**

---

## 2. Goal / Task

VibeFinder 1.0 suggests songs that best match a user's stated music taste. Given a profile describing a favorite genre, mood, energy level, and acoustic preference, it scores every song in the catalog and returns the top matches in ranked order. It does not learn from behavior — it only uses what the user explicitly tells it.

---

## 3. Data Used

The catalog contains 18 songs across 13 genres: pop, lofi, rock, ambient, jazz, synthwave, hip-hop, country, classical, r&b, metal, reggae, and edm. Each song has 9 attributes: id, title, artist, genre, mood, energy (0–1), tempo in BPM, valence (0–1), danceability (0–1), and acousticness (0–1). The original starter had 10 songs; 8 were added for genre diversity. Key limits: no lyrics, no listen history, no artist popularity data, and some genres have only one song in the catalog.

---

## 4. Algorithm Summary

The system scores each song out of 100 points using four rules:

- **Genre match** (+40 pts): Full points if the song's genre matches the user's favorite. Zero otherwise.
- **Mood match** (+30 pts): Full points if the song's mood matches. Zero otherwise.
- **Energy closeness** (up to +20 pts): Gradually awarded based on how close the song's energy is to the user's target. A perfect match gives 20, a big gap gives close to 0. No cliff-edge pass/fail.
- **Acousticness fit** (up to +10 pts): If the user likes acoustic music, songs with higher acousticness score higher. If they prefer electronic, lower acousticness scores higher.

All songs are scored independently, then sorted from highest to lowest. The top 5 are returned with an explanation of which rules fired.

---

## 5. Observed Behavior / Biases

The genre weight of 40 points dominates the scoring. If a user's favorite genre has only one song in the catalog, that song almost always ranks first — even if its energy or mood is completely wrong. This was confirmed in the edge case experiment: an ambient/moody user with target energy 0.9 got Spacewalk Thoughts (energy 0.28) as their top result, purely because it was the only ambient song. When the genre weight was cut to 20 and energy raised to 40, the ranking corrected itself and Blinding Lights (which matched mood and energy much better) rose to #1. The system also has no diversity mechanism, so users of popular genres like pop can get five nearly identical results.

---

## 6. Evaluation Process

Four user profiles were tested:

- **High-Energy Pop** (genre=pop, mood=happy, energy=0.8): Sunrise City ranked #1 with 97.80 — correct and intuitive.
- **Chill Lofi** (genre=lofi, mood=chill, energy=0.4, likes_acoustic=True): Library Rain and Midnight Coding ranked #1 and #2 — both felt right.
- **Intense Rock** (genre=rock, mood=intense, energy=0.9): Storm Runner ranked #1 with 98.80 — correct.
- **Edge Case** (genre=ambient, mood=moody, energy=0.9, likes_acoustic=True): Exposed the genre dominance bug — a song with wildly wrong energy ranked #1.

A weight experiment (genre 40→20, energy 20→40) was also run. It fixed the edge case but reshuffled results for other profiles, showing the system is sensitive to weight choices.

---

## 7. Intended Use and Non-Intended Use

**Intended use:** A classroom simulation to explore how content-based recommenders work. Good for understanding scoring, weighting, and bias in simple AI systems.

**Not intended for:** Real music discovery, production deployment, or any use case involving real users. The catalog is too small, there is no personalization over time, and the system cannot handle preferences it has no data for (e.g., a user who likes jazz gets very limited results).

---

## 8. Ideas for Improvement

1. **Add a diversity rule** to the ranking layer so no more than 2 songs from the same genre appear in the top 5 — this would reduce the filter bubble effect.
2. **Add `target_valence` and `target_tempo` to `UserProfile`** so the currently decorative valence and tempo_bpm fields actually affect scoring.
3. **Expand the catalog to 100+ songs** so genre matching has real competition and non-genre signals (mood, energy) can meaningfully differentiate results.

---

## 9. Personal Reflection

The biggest learning moment was the weight experiment in Phase 4. I expected changing genre from 40 to 20 points to make small adjustments — instead it completely reshuffled the top results for the edge case profile. That made it concrete how much a recommendation system's "intelligence" is really just the designer's assumptions encoded as numbers. Choosing 40 points for genre isn't neutral; it's a claim that genre matters twice as much as mood, and that claim can be wrong for certain users.

AI tools helped most during the design phase — working through the scoring formula, understanding why linear falloff works better than binary matching for continuous features like energy, and catching the duplicate energy calculation bug. The one moment I needed to double-check was when the AI suggested a code structure that looked correct but had a duplicate variable assignment that silently overwrote the experimental weight change.

What surprised me most was how "real" the recommendations felt even with just four rules and 18 songs. Sunrise City at 97.80 for a pop/happy profile felt genuinely correct, not like a toy result. That gap between "simple algorithm" and "feels intelligent" is smaller than I expected — which is both reassuring and a little unsettling when you think about how much people trust real systems.

Next I would add a hybrid layer: use this content-based score as a baseline, then boost songs that users with similar profiles have historically liked. That would be the first step toward collaborative filtering without needing a massive dataset.