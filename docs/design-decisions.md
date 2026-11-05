# TournamentLab — Design Decisions

This document records the principal design choices made for the current TournamentLab implementation. The challenge brief is the source of the tournament rules; this document explains how the implementation represents and enforces them.

## 1. Application shape

**Decision:** Use a small command-line application with separate Python modules and functions.

The CLI and application state live in `main.py`. Domain operations are separated into `teams.py`, `fixtures.py`, `results.py`, `standings.py`, and `storage.py`.

**Reason:** Each module has a focused responsibility. This avoids putting registration, scheduling, scoring, ranking, and persistence into one large application file.

## 2. Data representation

**Decision:** Represent teams and fixtures as dictionaries, collected in lists.

A team has this shape:

```python
{"id": "TM001", "name": "Red Comets"}
```

A fixture has this shape:

```python
{
    "id": "FX001",
    "team1_id": "TM001",
    "team2_id": "TM002",
    "status": "pending",
    "team1_score": None,
    "team2_score": None
}
```

A played fixture retains the same fields, with `status` set to `"played"` and both score fields set to nonnegative integers.

**Reason:** Dictionaries make each record's fields explicit, while lists provide a straightforward collection for iteration and JSON serialization.

## 3. Stable identifiers

**Decision:** Use team IDs in fixture references rather than team display names.

Team IDs follow the `TM001` pattern; fixture IDs follow the `FX001` pattern. The next team number is tracked separately and persisted as `next_team_number`.

**Reason:** Display names are labels and can be changed independently of the references used by fixtures. Stable IDs also prevent fixture relationships from depending on name spelling or capitalization.

IDs are not reused within a tournament. The counter is saved and validated during loading.

## 4. Team registration rules

**Decision:** Trim names, enforce a length of 2–30 characters, and compare names using `casefold()` for uniqueness. Accept between 4 and 8 teams for a tournament schedule.

Registration is locked after fixtures have been generated.

**Reason:** Trimming avoids accidental whitespace differences; case-folded comparison rejects names that differ only by letter case. Locking registration after schedule generation prevents the registered team set from becoming inconsistent with an existing round-robin schedule.

The current application does not provide team deletion or schedule regeneration.

## 5. Fixture generation

**Decision:** Generate every unordered pair once using nested loops, with the second loop beginning at the next index after the first team.

For (N) teams, the expected fixture count is:

```text
N × (N - 1) / 2
```

The generated fixture order is deterministic for a given input team order.

**Reason:** Starting the inner loop at the next index prevents self-matches and reverse duplicates. A four-team schedule contains six fixtures; a six-team schedule contains fifteen.

## 6. Result recording and validation

**Decision:** A result may be recorded only when the fixture exists and is pending. Validate both scores before mutating the fixture.

A score must satisfy both conditions:

- Its exact type is `int`; this rejects booleans as well as floats and strings.
- Its value is greater than or equal to zero.

Only after both scores pass validation are the two scores and the fixture status updated.

**Reason:** Validation-before-mutation prevents a rejected score from leaving a partially updated fixture. A played fixture cannot be submitted a second time.

The current MVP does not support editing completed results.

## 7. Standings as derived data

**Decision:** Do not store a separate mutable league table. Calculate standings from the registered teams and fixtures whose status is `"played"`.

The calculation derives played, wins, draws, losses, goals for, goals against, goal difference, and points.

**Reason:** Match records are the source of truth. Storing an independently editable table would create two representations that could disagree. Recalculation ensures that the table reflects the recorded results.

Points are awarded as follows:

- Win: 3 points.
- Draw: 1 point to each team.
- Loss: 0 points.

## 8. Ranking and champion rules

**Decision:** Sort standings by the following keys, in order:

1. Points descending.
2. Goal difference descending.
3. Goals for descending.
4. Team name after `casefold()`, ascending.

**Reason:** The explicit ordering makes ties predictable. Head-to-head is not part of the agreed ranking rules and is therefore not added.

The tournament is `not_started` when there are no fixtures, `in_progress` while any fixture is pending, and `completed` only when every fixture is played. A champion is returned only for a completed tournament.

## 9. Persistence and schema

**Decision:** Save teams, fixtures, the next team-number counter, and `schema_version: 1` in JSON. Do not persist calculated standings.

**Reason:** The saved records are sufficient to reconstruct the table. The schema version provides a marker for future format changes.

The loader validates the parsed data, including required fields, team IDs and names, fixture references, fixture IDs, duplicate pairings, status/score consistency, and counter continuity before returning the loaded state. The CLI assigns the loaded data to active state only after loading and validation succeed.

JSON syntax alone is not enough: a file can be syntactically valid while containing invalid tournament relationships.

## 10. Error handling and CLI behaviour

**Decision:** Domain operations raise `ValueError` for invalid input or invalid tournament operations. CLI handlers catch expected errors and display a useful message.

Invalid menu choices are rejected and return the user to the menu. File-system errors during save/load are reported instead of being treated as successful operations.

**Reason:** Separating domain validation from terminal messaging keeps the underlying operations reusable and makes failures visible without intentionally terminating the interactive session.

## 11. Dependencies and scope

**Decision:** Use the Python standard library. JSON handles persistence and `unittest` handles automated tests.

No external API, database, web framework, or third-party package is required for the current challenge scope.

The current CLI does not implement completed-result editing, team deletion, or demo-fixture simulation. Those features should not be assumed to exist merely because they appear as possible or required future challenge items.
