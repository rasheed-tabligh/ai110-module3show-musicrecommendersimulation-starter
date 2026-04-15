# Reflection: Comparing User Profiles

This file compares what happened when I ran different user profiles through the recommender and explains why the results made sense — or did not.

---

## High-Energy Pop vs. Chill Lofi

These two profiles are basically opposites, and the results showed it clearly. The High-Energy Pop profile surfaced pop and indie pop tracks with high energy (0.76–0.93) and happy moods. The Chill Lofi profile surfaced lofi tracks with low energy (0.35–0.42) and chill moods. The top scores were both above 7.3, meaning the system was very confident in both cases.

What is interesting is that the #4 result for Chill Lofi was Spacewalk Thoughts (ambient), not a lofi track. It got there because ambient music shares the same energy and mood space as lofi — low energy, calm feel. The system does not know that ambient and lofi are "similar genres" — it just noticed the numbers matched. That is actually a reasonable recommendation in real life, but it happened for the right reason accidentally, not because the system was designed to understand genre relationships.

---

## High-Energy Pop vs. Deep Intense Rock

Both profiles want high energy, but they expect completely different sounds. The Pop profile got bright, danceable tracks. The Rock profile got Storm Runner at the top, which was the right call — it's the only rock song and it matched almost perfectly.

But then #2 for Rock was Gym Hero (pop), which felt wrong. It appeared because it matched the "intense" mood and had high energy, but pop and rock sound nothing alike. This showed me that mood + energy can override genre in the ranking when the catalog is small. In a real app with thousands of songs, there would be enough intense rock tracks to fill the top 5 without pulling in pop. The small catalog is doing most of the damage here.

---

## Chill Lofi vs. Deep Intense Rock

The contrast here was the clearest of all. The Lofi profile's top song scored 7.40; the Rock profile's top song scored 7.43. Both are near-perfect matches, which makes sense — there happen to be multiple lofi songs and one rock song that align very closely with each profile.

The gap is in what comes after #1. The Lofi profile has 2 more strong lofi songs to fall back on (scores 6.46+). The Rock profile drops to 4.77 at #2 because it runs out of rock songs immediately and starts pulling from other genres. This shows that catalog depth matters more for some profiles than others. If you are a lofi listener, this system works reasonably well. If you are a rock listener, it runs out of ideas quickly.

---

## K-Pop Fan vs. High-Energy Pop

These two profiles are similar in what they want — upbeat, happy, energetic music — but the K-Pop profile gets significantly lower scores because the genre label "k-pop" does not appear in the catalog. Every song is automatically missing the +2.0 genre bonus.

Both profiles ended up recommending Sunrise City and Rooftop Lights at the top, which is actually correct — those tracks would fit both tastes. But the K-Pop profile's confidence was much lower (5.36 vs 7.35 for the same song). The system is saying "I think this might work for you" rather than "this is exactly what you want." That is an honest limitation. In a real product this would need to be addressed — maybe by mapping "k-pop" to similar genres like pop or indie pop when there is no direct match.

---

## Classical + Angry + High Energy vs. Deep Intense Rock

This was the adversarial test that exposed the genre anchor problem most clearly. The Rock profile got Storm Runner (rock, intense) at the top, which was correct. The Classical + Angry + High Energy profile got Iron Threshold (metal, angry) at the top — which is actually a reasonable result because the user said they want angry and high energy, and metal delivers that.

But Morning Suite No. 3 — the only classical song — ranked #2 despite having energy of 0.21 when the user wanted 0.90. The genre match (+2.0) pulled it up even though every other feature was wrong. In plain terms: the system saw the word "classical" in the profile, found the only classical song, and gave it bonus points regardless of how different it sounded from what the user actually described. That is a bug that comes from the weight design, not the data. A genre match should only count as a bonus if the other features are at least in the right ballpark.

---

## High Energy + Sad Mood vs. Chill Lofi

This comparison shows what happens when a user's preferences do not fit neatly into the available catalog. The Chill Lofi profile had good matches because the catalog has songs built for that vibe. The High Energy + Sad profile is asking for something the catalog does not have — a loud, sad song. No such track exists in the 18-song dataset.

The result was that the system split its recommendations: either high energy but wrong mood (Pulse Protocol, Iron Threshold), or correct mood but too quiet (Empty Roads). Neither group fully satisfied what the user was describing. This is not a flaw in the algorithm — it is a flaw in the data. The algorithm correctly identified the best available options. But a good recommender would ideally flag when no strong match exists rather than presenting mediocre results with the same confidence as a perfect match.
