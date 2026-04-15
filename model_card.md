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

The biggest limitation is the catalog size. With only 18 songs and some genres having just one entry, users with niche tastes will almost always get weak recommendations. There is just not enough variety.

The scoring also has a genre bias baked in. A genre match gives a fixed +2.0 bonus no matter what, which means a song that perfectly matches your energy and mood but is the wrong genre can still lose to a genre match that sounds nothing like what you wanted. That feels off sometimes.

The system also treats every user the same way — it does not adjust its weights based on what kind of listener you are. Someone who cares deeply about energy levels but does not really care about genre gets the same formula as someone who is very genre-loyal. That is a real oversimplification.

There is no diversity built in either. The top 5 results could easily all be from the same genre or mood cluster, which would feel repetitive in a real app.

---

## 7. Evaluation

I tested a few different user profiles mentally to see how the system would behave.

The first was a focused lofi listener — low energy, chill mood, lofi genre. The system correctly pushed the lofi tracks to the top and ranked the metal and rock tracks at the bottom. That felt right.

The second was a high-energy pop fan — energy around 0.85, happy mood. The pop and electronic tracks scored highest, which made sense. What surprised me is that the hip-hop track also ranked fairly high because its energy and danceability were a close match, even without a genre match. That actually felt like a reasonable discovery — the kind of thing a real recommender might surface.

The third profile was harder: someone who likes classical, peaceful, low energy. Since there is only one classical song in the catalog, the system had very little to recommend in that genre. The scores were all low and the results did not feel satisfying. That confirmed the catalog gap problem.

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
