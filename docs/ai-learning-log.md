# TournamentLab — AI Learning Log

This log records three learning cycles from the TournamentLab build. It is intended to show what was learned and how ideas were checked against reasoning, small examples, and the implementation.

> **Record-integrity note:** The original coaching conversation is not preserved here as a verbatim prompt transcript. The prompt descriptions below are reconstructed summaries of the topics discussed; they are not presented as exact quotations. The learner explanations are summaries of the reasoning demonstrated during the sessions. Where an exact prompt, command output, or commit reference is not available, this log says so rather than inventing evidence.

## Learning cycle 1 — Strict score validation and Python booleans

### Topic I needed to understand

Why a Boolean value must not be accepted as a match score, even though Python treats `bool` as a subclass of `int`.

### Prompt used

Reconstructed prompt summary: Explain Python's relationship between `bool` and `int`, then help me classify possible match-score inputs and decide how to validate a score that must be a nonnegative integer.

### Explanation in my own words

Python's `True` and `False` behave like integers in some contexts: `True` is treated as 1 and `False` as 0. That means a broad integer check such as `isinstance(score, int)` can accept a Boolean by mistake.

TournamentLab has a stricter rule. A score must be an integer value, but it must not be a Boolean, and it cannot be negative. The validation therefore checks the exact type and then checks the value.

### Small independent experiment

I considered these values as possible scores:

```python
[2, 0, True, -1, 3.5, "4"]
```

The valid values are `2` and `0`. The Boolean, negative integer, float, and string must be rejected.

### Actual result

The diagnostic exercise correctly classified the values. In the implementation, `validate_score` uses an exact type check and rejects negative values. The learner reported that the result-validation tests ran cleanly, including the Boolean and invalid-score cases.

### Corrected understanding / decision

I learned that checking whether something is an instance of `int` is not always strict enough for business rules. I used `type(score) is int` so that Booleans cannot pass as goals.

### Related implementation

- `tournament/results.py` — `validate_score` and `record_result`.
- `tests/test_results.py` — score validation and result-recording cases.

---

## Learning cycle 2 — Round-robin combinations and nested loops

### Topic I needed to understand

How to generate every unique pairing without producing a team's match against itself or generating the same pairing in reverse order.

### Prompt used

Reconstructed prompt summary: Teach me how nested loops can produce unique unordered pairs from a list of teams, explain why the inner loop should begin after the current outer-loop index, and help me derive the fixture count.

### Explanation in my own words

The outer loop selects the first team. The inner loop selects only teams that come after it in the list. Beginning the inner loop at the next index means the selected team cannot play itself, and the reverse pairing is never generated later.

For (N) teams, the number of unique pairings is (N(N-1)/2). This gives six fixtures for four teams and fifteen fixtures for six teams.

### Small independent experiment

For four teams — Red, Blue, Green, and Yellow — I listed the unique pairs:

- Red–Blue
- Red–Green
- Red–Yellow
- Blue–Green
- Blue–Yellow
- Green–Yellow

There are six pairings. I also checked the expected count for six teams: fifteen.

### Actual result

I identified the need for the inner loop to start at `i + 1`. The fixture tests later confirmed six fixtures for four teams and fifteen for six teams, with no self-matches or duplicate unordered pairings. The learner reported that the fixture tests passed.

### Corrected understanding / decision

The important part is not simply using two loops. It is controlling the starting index of the inner loop. That index is what prevents self-pairings and reverse duplicates while keeping the generation deterministic.

### Evidence-backed implementation choice

I retained the nested-loop implementation in `generate_fixtures`. It directly expresses the pair-generation logic being learned and keeps the algorithm straightforward. This log does not claim that a particular AI-generated alternative was rejected; no such deliberate rejection is documented in the available session record.

### Related implementation

- `tournament/fixtures.py` — `generate_fixtures`.
- `tests/test_fixtures.py` — fixture counts, self-match prevention, and duplicate-pair checks.

---

## Learning cycle 3 — Derived standings and source of truth

### Topic I needed to understand

Why the league table should be calculated from played fixtures instead of being maintained as a separate set of mutable team totals.

### Prompt used

Reconstructed prompt summary: Explain derived state using a league-table example. Help me calculate played, wins, draws, losses, goals for, goals against, goal difference, and points from match records, and explain why pending fixtures must not affect the table.

### Explanation in my own words

The match records are the source of truth. The standings are a calculation based on those records. If I separately store and update both match results and team totals, the two can disagree if one update succeeds and the other does not.

Recalculating the standings from played fixtures avoids that second mutable scoreboard. Pending fixtures are ignored because they do not have a result yet.

### Small independent experiment

I calculated the table for these three matches:

- Red 2–0 Blue
- Blue 1–1 Green
- Red 0–1 Green

My hand calculation was:

| Team | Played | Wins | Draws | Losses | Points |
|  --- |  ---:  |  ---:|   ---:|    ---:|    ---:|
| Green|    2   |   1  |   1   |   0    |    4   |
|  Red |    2   |   1  |   0   |   1    |    3   |
| Blue |    2   |   0  |   1   |   1    |    1   |

### Actual result

The hand-calculated points were correct. The implementation tests covered aggregation from played fixtures, ignored pending fixtures, draw points, ranking tie-breaks, and champion eligibility. The learner reported that the standings tests passed.

### Corrected understanding / decision

I learned to separate stored facts from calculated information. Fixtures are stored; standings are derived. The champion is available only when all fixtures have been played.

### Related implementation

- `tournament/standings.py` — `calculate_standings`, `rank_standings`, `get_tournament_status`, and `get_champion`.
- `tests/test_standings.py` — aggregation, pending-fixture handling, ranking, and champion cases.

---

## Reflection and evidence boundaries

These cycles document learning about strict validation, combinatorial scheduling, and derived state. The explanations and experiment summaries are reconstructed from the recorded coaching and implementation history; they should be reviewed and edited if they do not accurately reflect my own understanding.

The project was built incrementally: I typed the implementation, ran it, shared results, and corrected issues before moving to the next mission. I manually exercised the CLI, including saving a tournament, exiting, restarting, loading it, and checking that the teams, fixtures, and results were restored.

The following claims are intentionally **not** made in this log:

- That the full Stage 4 Professional Test Lab was completed. That stage was intentionally skipped.
- That the complete challenge test checklist has been independently audited.
- That an Engineer A / Engineer B peer review or pull-request approval occurred.
- That exact verbatim AI prompts or complete terminal transcripts are available here.

The purpose of this log is to preserve genuine learning evidence and distinguish observed results from reconstructed notes.
