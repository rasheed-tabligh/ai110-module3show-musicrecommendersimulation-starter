# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name

VibeFinder 1.0

---

## 2. Goal / Task

VibeFinder's goal is to predict which songs from an 18-track catalog will best match a user's declared taste profile. It does this by scoring every song against the user's preferred genre, mood, energy level, emotional positivity (valence), and danceability, then returning the top-ranked results with a plain-language explanation for each one.

Intended use: Classroom exploration and learning. This is a simulation built to understand how content-based recommenders work. It is appropriate for experimenting with weights, testing edge cases, and discussing how data shapes recommendations.

Non-intended use: This system should not be used as a real music recommendation product. It has only 18 songs, no learning from listening history, no user feedback loop, and no diversity enforcement. It would give poor results for anyone whose preferred genre is not in the catalog (K-pop, Afrobeats, Latin, etc.). It also should not be used to make decisions about what music is "good" or "popular" — the catalog reflects one person's choices and has no statistical validity.

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

The biggest weakness I discovered through testing is what I am calling the genre anchor problem. The fixed +2.0 for a genre match is so large that it can drag a song to the top even when every other feature is a bad fit. The clearest example I found was the "Classical + Angry + High Energy" edge case: the only classical song in the catalog scored #2 despite having energy of 0.21 when the user wanted 0.90. The genre match alone kept it in the results even though it sounds nothing like what the profile was asking for.

A second bias I noticed is the catalog echo chamber. When I tested the Chill Lofi profile, the top 3 results were all lofi songs, which is technically correct but also means the system never discovers anything outside the genre the user already declared. Real recommenders work hard to inject some variety; this one has no mechanism to do that at all.

The third issue is missing genre silence. When I tested a K-Pop profile — a genre not in the catalog — the system lost its +2.0 genre bonus entirely and fell back on mood and numeric features only. The results were reasonable but the scores dropped by 2 full points for every song, meaning a K-Pop fan will always get a weaker, less confident recommendation than a pop fan, just because of a label mismatch. The system has no way to say "I don't know this genre; let me fall back to something similar."

Finally, the energy-only middle ground is an issue. Songs in the 0.45–0.65 energy range don't strongly match any extreme profile, so they cluster in the bottom half of almost every ranking regardless of how good their mood and valence fit is. The formula penalizes the middle.

---

## 7. Evaluation

I ran six profiles against the system: three standard and three adversarial edge cases.

Standard profiles:

The High-Energy Pop profile worked exactly as expected. Sunrise City scored 7.35/7.50 — almost a perfect match because it hits genre, mood, and all three numeric features simultaneously. Gym Hero came second even though its mood was "intense" rather than "happy," because the genre match and energy proximity made up the difference. That feels like a reasonable alternative — someone who likes happy pop might also enjoy a high-energy pop workout track.

The Chill Lofi profile produced very clean results. Library Rain and Midnight Coding both scored above 7.3 and are genuinely similar tracks. What surprised me here is #4: Spacewalk Thoughts (ambient, chill) appearing despite being a completely different genre. It got there purely on mood match and numeric proximity. That actually felt like a realistic discovery — ambient and lofi do share a similar energy space.

The Deep Intense Rock profile surfaced Storm Runner at 7.43 — the only rock song in the catalog — which was the right call. But then #2 was Gym Hero (pop), which felt off. It got there on mood match ("intense") and energy proximity, but pop and rock are very different listening experiences. This is the genre anchor problem in reverse: mood + energy can overpower the genre gap when the catalog is small.

Adversarial profiles:

The Classical + Angry + High Energy profile was the most revealing test. The user wants high-energy angry music but declared "classical" as their genre. Iron Threshold (metal, angry) ranked #1 — because the mood match and energy proximity outweighed the missing genre bonus. Morning Suite No. 3 (the only classical song) ranked #2 despite energy of 0.21 vs. the user's target of 0.90. This shows the genre anchor dragging a completely wrong-energy song into the top results.

The K-Pop Fan profile confirmed the missing genre gap. With no k-pop songs in the catalog, the system lost the genre bonus for every song and relied entirely on mood, energy, and valence. The results were actually decent — Sunrise City and Rooftop Lights are bright, upbeat tracks that would overlap with a K-pop taste profile — but all scores were capped around 5.0 instead of 7.0+, making every recommendation feel uncertain.

The High Energy + Sad Mood profile was the most interesting contradiction. Pulse Protocol (electronic, energetic) ranked #1 because it nailed the genre and energy but completely missed the sad mood. Empty Roads (folk, sad) ranked #4 with a low score of 3.87 — it matched the mood but was too quiet. The system had no way to find a "sad banger" because none exists in the catalog. This gap between what the user wants and what the data contains is something a larger real-world system would solve with a bigger catalog.

Weight experiment:

I also ran a version where genre weight was halved (1.0) and energy weight was doubled (4.0). The top-ranked songs stayed mostly the same — the strongest matches still won — but the score gaps between them compressed. Gym Hero fell from #2 to #3 in the High-Energy Pop ranking because its genre bonus was now worth less than the better energy proximity of Rooftop Lights. This confirmed that energy is actually the most descriptive feature for these profiles, and the genre weight might be slightly over-tuned in the original version.

---

## 8. Future Work

The first thing I would fix is the catalog — 18 songs is not enough to test anything meaningfully. Even 100 songs would make a big difference.

I would also add a diversity rule so the top results cannot all come from the same genre or mood. Getting five lofi tracks in a row when you asked for lofi is technically correct but boring in practice.

It would also be interesting to let the user set weights themselves. Someone who really cares about energy but does not care about genre should be able to say that, and the formula should reflect it.

Longer term, adding listening history — like tracking skips and replays — would let the system learn over time rather than always relying on what the user explicitly told it. That is basically how Spotify works, and it makes a huge difference in how natural the recommendations feel.

---

## 9. Personal Reflection

Biggest learning moment

The biggest thing I learned is that a recommendation is just a score — and a score is just a set of rules someone wrote down. Before this project I thought of Spotify as something intelligent that "knows" you. After building this, I understand it is a system that measures how close you are to things it has already seen. The intelligence is in the data and the weight choices, not in the algorithm itself. That was a genuinely surprising shift in how I think about it.

How AI tools helped — and when I had to double-check them

AI tools were genuinely useful for generating the initial song data, drafting the scoring formula, and structuring the README and model card. They saved a lot of time on boilerplate and helped me think through edge cases I would not have considered on my own, like the K-Pop missing genre scenario or the conflicting classical + angry + high energy profile.

But I had to double-check the math carefully. At one point I was given a formula that would have added scores together in a way where a perfect genre + mood match alone could push a song above its actual maximum — the weights did not add up to what was claimed. I caught it by running the numbers manually against a known song. The AI gave me a reasonable-looking result that was subtly wrong, and I would have missed it if I had not verified it myself. That is the main lesson: AI-generated logic needs to be traced through at least one real example before you trust it.

What surprised me about simple algorithms feeling like recommendations

The thing that surprised me most is how quickly a handful of weighted rules starts to feel "right." When I ran the Chill Lofi profile and the top two results were Library Rain and Midnight Coding — two genuinely similar ambient study tracks — it felt like the system understood something. It did not. It just found the two songs with the closest numbers. But the outcome felt intuitive, which made me understand why people trust these systems more than they should. The feeling of a good recommendation does not mean the reasoning behind it is sound.

What I would try next

If I extended this project, the first thing I would add is a way to handle unknown genres gracefully — instead of silently dropping the bonus, try to map unfamiliar labels to something close. Second, I would add a diversity penalty so the same genre cannot take more than two spots in the top 5. Third, and most interesting to me, I would experiment with learning from skips — if a user skips a genre match, reduce that genre's weight for them specifically. That is the step from a rule-based system to something that actually adapts, and it is where the real complexity of systems like Spotify begins.
