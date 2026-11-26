"""Fair answers: the best answer must not be guessable from its length.

Before this check, the best answer was the longest one in the original 52 guest moments, so a
player could win by always tapping the longest choice. These tests read the moments
straight from index.html and training/silver-key.html (no browser needed).

Run: python tests/test_answers.py
"""
import json
import re
import unittest
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = (ROOT / 'index.html').read_text(encoding='utf-8')


def const(name):
    match = re.search(r'(?m)^const ' + name + r' = (\[.*\]);$', HTML)
    return json.loads(match.group(1))


MOMENTS = const('GUEST_MOMENTS')
SPANISH = const('MOMENTS_ES')


def best_index(moment):
    scores = [c[1] for c in moment['choices']]
    return scores.index(max(scores))


def positions(texts_for):
    """Where the best answer sits by length in each moment: longest, middle or shortest."""
    count = Counter()
    for i, moment in enumerate(MOMENTS):
        lengths = [len(t) for t in texts_for(i)]
        best = lengths[best_index(moment)]
        count['longest' if best == max(lengths) else 'shortest' if best == min(lengths) else 'middle'] += 1
    return count


def strategy_wins(texts_for, pick):
    return sum(pick([len(t) for t in texts_for(i)]) == best_index(m) for i, m in enumerate(MOMENTS))


ENGLISH = lambda i: [c[0] for c in MOMENTS[i]['choices']]
ESPANOL = lambda i: SPANISH[i]['choices']
LONGEST = lambda ls: ls.index(max(ls))
SHORTEST = lambda ls: ls.index(min(ls))
MIDDLE = lambda ls: sorted(range(len(ls)), key=ls.__getitem__)[len(ls) // 2]


class FairAnswers(unittest.TestCase):
    def test_01_spanish_lines_up_with_english(self):
        self.assertEqual(len(MOMENTS), len(SPANISH))
        for en, es in zip(MOMENTS, SPANISH):
            self.assertEqual(en['title'], es['en'])
            self.assertEqual(len(en['choices']), len(es['choices']))

    def test_02_no_length_strategy_beats_chance_by_much(self):
        # Three real choices, so guessing wins about a third of the time. Allow some slack,
        # but no single length rule (always longest, shortest or middle) may win over 45%.
        limit = int(len(MOMENTS) * 0.45)
        for name, texts in (('English', ENGLISH), ('Spanish', ESPANOL)):
            for rule_name, rule in (('longest', LONGEST), ('shortest', SHORTEST), ('middle', MIDDLE)):
                wins = strategy_wins(texts, rule)
                self.assertLessEqual(wins, limit, f'{name}: always picking the {rule_name} answer wins {wins} of {len(MOMENTS)}')

    def test_03_best_answer_is_sometimes_the_shortest(self):
        for name, texts in (('English', ENGLISH), ('Spanish', ESPANOL)):
            self.assertGreaterEqual(positions(texts)['shortest'], len(MOMENTS) // 4, name)

    def test_04_training_desk_uses_the_same_answers(self):
        training = (ROOT / 'training/silver-key.html').read_text(encoding='utf-8')
        for moment in MOMENTS:
            for text, _ in moment['choices']:
                self.assertIn(json.dumps(text)[1:-1], training, text)

    def test_05_helpful_words_do_not_give_the_best_answer_away(self):
        # "ask", "confirm", "offer" and "check" used to sit in the best answer far more often than
        # in the others, so a player could guess by spotting them. Wrong answers use them too now.
        words = re.compile(r'\b(ask|asks|asking|confirm|confirms|offer|offers|offering|check|checks|checking)\b', re.I)
        wins = 0.0
        for moment in MOMENTS:
            texts = [c[0] for c in moment['choices']]
            picks = [k for k, t in enumerate(texts) if words.search(t)] or list(range(len(texts)))
            wins += (best_index(moment) in picks) / len(picks)
        self.assertLessEqual(wins, len(MOMENTS) * 0.45, f'picking answers with helpful words wins {wins:.1f} of {len(MOMENTS)}')

    def test_06_the_garlic_question_talks_about_garlic(self):
        garlic = next(m for m in MOMENTS if m['title'] == 'The garlic question')
        for text, _ in garlic['choices']:
            self.assertNotIn('fish', text)


if __name__ == '__main__':
    unittest.main()
