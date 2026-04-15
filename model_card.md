# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name

**VibeFinder 1.0**

---

## 2. Intended Use

This system is built to suggest songs from a small catalog based on what kind of music a person feels like listening to right now. You give it your favorite genre, your current mood, and a sense of how high or low energy you want, and it goes through every song in the list and figures out which ones fit best.

It is not meant for real users or a real product. I built it as a learning exercise to understand how apps like Spotify actually think when they recommend music. The assumption it makes is that the user knows what they want — it does not learn over time or adapt based on listening history.

---

## 3. How the Model Works

Imagine you walk into a record store and tell the person behind the counter: "I want something chill, lofi, medium energy." They mentally go through every record in the store and score how well each one matches what you described.

That is basically what this system does. For each song in the catalog, it checks two things categorically — does the genre match, and does the mood match. Those are worth the most points because they define what kind of music something fundamentally is. Then it looks at three numbers — energy, valence (basically how happy or sad a song feels), and danceability — and gives points based on how close each one is to what you asked for. The closer, the higher the score.

Once every song has a score, they get sorted from highest to lowest and the top results are returned as recommendations.

---

## 4. Data

The catalog has 18 songs total. I started with the original 10 that came with the project and added 8 more to make it more diverse. The original set was pretty limited — mostly pop, lofi, and rock — so I added genres like hip-hop, r&b, country, classical, metal, reggae, electronic, and folk to cover a wider range of tastes and moods.

The moods now include things like energetic, romantic, nostalgic, peaceful, angry, and sad alongside the originals like chill, happy, and intense.

That said, the catalog is still tiny. Some genres only have one song, which means if you are a country or classical fan the system does not have much to work with. The data also reflects a pretty mainstream Western taste — there is no K-pop, Afrobeats, Latin, or regional music in here at all, which is a real gap.

---

## 5. Strengths

The system works best when the user has a clear and specific preference. If you say you want chill lofi with low energy, it does a solid job surfacing those tracks and pushing high-energy metal or pop to the bottom of the list. The gap in scores between a good match and a bad match is big enough that the ranking feels intuitive.

It is also easy to understand why a recommendation was made. Because the scoring is rule-based and transparent, you can look at any song's score and trace exactly where the points came from. There are no black-box decisions — which I actually think is one of the things this kind of simple system does better than more complex ones.

---

## 6. Limitations and Bias

The biggest weakness I discovered through testing is what I am calling the **genre anchor problem**. The fixed +2.0 for a genre match is so large that it can drag a song to the top even when every other feature is a bad fit. The clearest example I found was the "Classical + Angry + High Energy" edge case: the only classical song in the catalog scored #2 despite having energy of 0.21 when the user wanted 0.90. The genre match alone kept it in the results even though it sounds nothing like what the profile was asking for.

A second bias I noticed is the **catalog echo chamber**. When I tested the Chill Lofi profile, the top 3 results were all lofi songs, which is technically correct but also means the system never discovers anything outside the genre the user already declared. Real recommenders work hard to inject some variety; this one has no mechanism to do that at all.

The third issue is **missing genre silence**. When I tested a K-Pop profile — a genre not in the catalog — the system lost its +2.0 genre bonus entirely and fell back on mood and numeric features only. The results were reasonable but the scores dropped by 2 full points for every song, meaning a K-Pop fan will always get a weaker, less confident recommendation than a pop fan, just because of a label mismatch. The system has no way to say "I don't know this genre; let me fall back to something similar."

Finally, the **energy-only middle ground** is an issue. Songs in the 0.45–0.65 energy range don't strongly match any extreme profile, so they cluster in the bottom half of almost every ranking regardless of how good their mood and valence fit is. The formula penalizes the middle.

---

## 7. Evaluation

I ran six profiles against the system: three standard and three adversarial edge cases.

**Standard profiles:**

The **High-Energy Pop** profile worked exactly as expected. Sunrise City scored 7.35/7.50 — almost a perfect match because it hits genre, mood, and all three numeric features simultaneously. Gym Hero came second even though its mood was "intense" rather than "happy," because the genre match and energy proximity made up the difference. That feels like a reasonable alternative — someone who likes happy pop might also enjoy a high-energy pop workout track.

The **Chill Lofi** profile produced very clean results. Library Rain and Midnight Coding both scored above 7.3 and are genuinely similar tracks. What surprised me here is #4: Spacewalk Thoughts (ambient, chill) appearing despite being a completely different genre. It got there purely on mood match and numeric proximity. That actually felt like a realistic discovery — ambient and lofi do share a similar energy space.

The **Deep Intense Rock** profile surfaced Storm Runner at 7.43 — the only rock song in the catalog — which was the right call. But then #2 was Gym Hero (pop), which felt off. It got there on mood match ("intense") and energy proximity, but pop and rock are very different listening experiences. This is the genre anchor problem in reverse: mood + energy can overpower the genre gap when the catalog is small.

**Adversarial profiles:**

The **Classical + Angry + High Energy** profile was the most revealing test. The user wants high-energy angry music but declared "classical" as their genre. Iron Threshold (metal, angry) ranked #1 — because the mood match and energy proximity outweighed the missing genre bonus. Morning Suite No. 3 (the only classical song) ranked #2 despite energy of 0.21 vs. the user's target of 0.90. This shows the genre anchor dragging a completely wrong-energy song into the top results.

The **K-Pop Fan** profile confirmed the missing genre gap. With no k-pop songs in the catalog, the system lost the genre bonus for every song and relied entirely on mood, energy, and valence. The results were actually decent — Sunrise City and Rooftop Lights are bright, upbeat tracks that would overlap with a K-pop taste profile — but all scores were capped around 5.0 instead of 7.0+, making every recommendation feel uncertain.

The **High Energy + Sad Mood** profile was the most interesting contradiction. Pulse Protocol (electronic, energetic) ranked #1 because it nailed the genre and energy but completely missed the sad mood. Empty Roads (folk, sad) ranked #4 with a low score of 3.87 — it matched the mood but was too quiet. The system had no way to find a "sad banger" because none exists in the catalog. This gap between what the user wants and what the data contains is something a larger real-world system would solve with a bigger catalog.

**Weight experiment:**

I also ran a version where genre weight was halved (1.0) and energy weight was doubled (4.0). The top-ranked songs stayed mostly the same — the strongest matches still won — but the score gaps between them compressed. Gym Hero fell from #2 to #3 in the High-Energy Pop ranking because its genre bonus was now worth less than the better energy proximity of Rooftop Lights. This confirmed that energy is actually the most descriptive feature for these profiles, and the genre weight might be slightly over-tuned in the original version.

---

## 8. Future Work

The first thing I would fix is the catalog — 18 songs is not enough to test anything meaningfully. Even 100 songs would make a big difference.

I would also add a diversity rule so the top results cannot all come from the same genre or mood. Getting five lofi tracks in a row when you asked for lofi is technically correct but boring in practice.

It would also be interesting to let the user set weights themselves. Someone who really cares about energy but does not care about genre should be able to say that, and the formula should reflect it.

Longer term, adding listening history — like tracking skips and replays — would let the system learn over time rather than always relying on what the user explicitly told it. That is basically how Spotify works, and it makes a huge difference in how natural the recommendations feel.

---

## 9. Personal Reflection

Before this project I never really thought about what was happening behind the scenes when Spotify or YouTube recommended something. It just felt like magic. Building even this simple version made it clear that there is nothing magical about it — it is just math applied to attributes. The "magic" comes from having millions of data points and tuning the weights really carefully over time.

What surprised me most is how much the weights matter. Changing how much a genre match is worth versus an energy match completely changes the character of the recommendations. A small tweak in one number can make the system feel totally different. That made me realize how much human judgment goes into these systems — someone had to decide what mattered more, and that decision shapes what every user experiences.

It also made me think differently about bias. The system I built would do a poor job for anyone whose taste does not fit the Western, mainstream genres I included. That is not a technical problem — it is a data problem that started with the choices I made about what songs to add. Real recommenders have the same issue, just at a much larger scale.
