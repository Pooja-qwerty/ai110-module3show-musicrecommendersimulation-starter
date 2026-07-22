# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name

**VibeFinder 1.0**

---

## 2. Intended Use

VibeFinder 1.0 is a content-based music recommender designed to suggest songs that match a user's stated taste profile. It is intended for classroom exploration of how recommendation systems work, not for production use. The system assumes the user can accurately describe their preferences in terms of genre, mood, energy level, and acoustic preference. It makes no use of listening history, skips, or real-time behavior.

---

## 3. How the Model Works

VibeFinder scores every song in the catalog against the user's taste profile and returns the top matches. Each song gets points for matching the user's favorite genre (up to 40 points), favorite mood (up to 30 points), how close its energy level is to the user's target (up to 20 points, awarded gradually — a near miss barely loses points), and how well its acoustic quality matches whether the user prefers acoustic or electronic sounds (up to 10 points). The song with the highest total score is recommended first. Think of it like a judge scoring figure skaters: each category has a maximum, and the total determines the winner.

---

## 4. Data

The catalog contains 18 songs across 10 genres: pop, lofi, rock, ambient, jazz, synthwave, hip-hop, country, classical, r&b, metal, reggae, and edm. Moods represented include happy, chill, intense, moody, relaxed, and focused. The original starter dataset had 10 songs; 8 were added to improve genre diversity. Some musical dimensions are entirely missing from the data — lyrics, language, cultural context, artist popularity, and listener history are not represented at all.

---

## 5. Strengths

The system works well for users with clear, well-represented preferences. A "Chill Lofi" profile reliably surfaces Library Rain and Midnight Coding as top results, which intuitively makes sense — both are lofi, chill, low energy, and highly acoustic. Similarly, the "Intense Rock" profile correctly ranks Storm Runner first with a near-perfect score of 98.80. The scoring logic is fully transparent: every point is explained in plain language, so a user can see exactly why a song was or wasn't recommended.

---

## 6. Limitations and Bias

The biggest weakness is that genre match dominates at 40 points — nearly half the maximum score. This means a song that perfectly matches mood, energy, and acousticness but is in the wrong genre will almost always lose to a genre match with poor mood and energy fit. In the edge case experiment (ambient/moody/high energy), Spacewalk Thoughts ranked #1 despite having energy 0.28 vs a target of 0.90, purely because it was the only ambient song. The catalog is also tiny: genres with only one representative always return the same top song regardless of other preferences. Additionally, the system has no diversity mechanism — if five pop songs exist and the user likes pop, all five slots could be filled with pop tracks, leaving no room for cross-genre discovery that real platforms deliberately build in.

---

## 7. Evaluation

Four profiles were tested: High-Energy Pop, Chill Lofi, Intense Rock, and an adversarial edge case (ambient/moody/energy=0.9/likes_acoustic=True). The pop and rock profiles produced intuitive results — well-represented genres with multiple matching songs ranked correctly by score. The lofi profile also worked well, surfacing both lofi/chill songs in the top two slots. The edge case revealed the genre dominance problem: with only one ambient song in the catalog, it ranked #1 despite a severe energy mismatch. A weight experiment (genre reduced to 20, energy increased to 40) fixed this — Spacewalk Thoughts dropped to #4 and Blinding Lights (which matched mood and energy better) rose to #1. This confirmed that the original 40-point genre weight is too strong for niche genres with thin catalog coverage.

Comparing Chill Lofi vs Intense Rock: the lofi profile rewarded high acousticness and low energy, while the rock profile rewarded low acousticness and high energy — the acousticness scoring correctly inverted based on `likes_acoustic`. Both profiles had their correct top song score above 96, showing the system is decisive when the catalog has good coverage of the requested genre.

---

## 8. Future Work

The most impactful improvement would be adding a diversity rule to the ranking layer — for example, no more than two songs by the same artist or in the same genre in the top 5. This would prevent the "filter bubble" where a user gets five nearly identical songs. Adding `target_valence` and `target_tempo` to `UserProfile` would let the system use the currently decorative `valence` and `tempo_bpm` fields for scoring. A larger catalog (100+ songs) would make genre matching less dominant by giving non-genre signals more room to differentiate results.

---

## 9. Personal Reflection

Building this recommender made it clear how much of a recommendation is actually a design choice disguised as math. Choosing to give genre 40 points vs 30 points is not a neutral technical decision — it encodes a belief about what matters most in music taste, and that belief can produce results that feel wrong for certain users. The edge case experiment was the most surprising part: a song with completely wrong energy ranked first just because it was the only representative of its genre, which is exactly the kind of silent failure that would be hard to catch without deliberately testing adversarial profiles. Real systems like Spotify are essentially making thousands of these weight decisions simultaneously, which explains why their recommendations can feel eerily accurate for some users and completely off for others.