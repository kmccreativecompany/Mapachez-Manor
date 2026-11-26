# Service language: how staff speak to guests

Every line a staff member (you, Delores, the desk, housekeeping, dining) says **to a guest**
follows five-star service language standards. Guests' own lines, staff-to-staff sitcom scenes,
Delores coaching the player, and narration keep their relaxed sitcom voice.

## The rules
- **Full sentences.** No clipped fragments like "Two nights." or "Tray outside or inside?".
  Say "You are staying with us for two nights." and "Would you like the tray left outside your door or brought inside?"
- **No slang or casual words.** Not "yep", "okay", "sure", "alright, bye", "you guys", "coming right up", "no problem".
  Use "Certainly", "It's my pleasure", "Please enjoy your evening".
- **Gracious and engaged.** "May I…", "I would be happy to…", "Would you prefer…".
- **Use the guest's name when it is known**, warmly, not in every sentence.
- **Answer the phone fully:** greeting, the manor's name (outside lines), who you are, an offer to help.
- **Confirm details and give real times.** "I will have two fresh towels brought to your room within 10 minutes."
- **Close with warmth** and an offer to help further.
- **Apologize with words**, then say what you will do.

Wrong answers in quizzes stay casual on purpose, so players can see the difference.
No hotel or ratings brand names appear in the game.

## Where the lines live
- Guest moments: `training/silver-key.html` (English) and `training/moments-es.json` (Spanish),
  then run `tools/embed_guest_moments.py` and `tools/embed_spanish.py`.
- Everything else is in `index.html`: `KNOCK_TEXT` (texts to guests, notes, arrivals), `CHECKIN_TEXT`,
  `STAR_TEXT` + `STAR_CALLS` (three-ring phone), `HMS_QS` (guest asks at the desk), `GHOST_TEXT`,
  `MC_TEXT` (Guest Service Language and Telephone e-courses), and the Lady Vesper supper scenes.
