# TournamentLab

TournamentLab is a Python command-line application for managing a single round-robin esports league. It supports team registration, fixture generation, match-result entry, automatically calculated standings, champion determination, and JSON save/load.

The project was built as a Python engineering challenge focused on fair scheduling, reliable score validation, predictable rankings, and data integrity.

## Features

- Register 4–8 teams with names between 2 and 30 characters.
- Reject duplicate team names without regard to letter case.
- Generate each unordered team pairing exactly once.
- Assign stable team IDs and fixture IDs.
- Display fixtures and whether each is pending or played.
- Record nonnegative integer scores once per fixture.
- Calculate standings from played fixtures rather than storing a separately editable table.
- Rank teams using the documented tie-break sequence.
- Show a champion only after every scheduled fixture has been played.
- Save and restore tournament data using versioned JSON with validation.

## Requirements

- Python 3.12 or newer.
- No third-party Python packages are required.

Python 3.12+ is required by the current source syntax in `tournament/teams.py`.

## Getting started

Clone the repository and open a terminal in the project directory:

```powershell
git clone https://github.com/Bront888/TournamentLab.git
cd TournamentLab
```

Run the application:

```powershell
py main.py
```

The application displays a menu. Select an option by entering its number:

| Option | Action |
|---|---|
| 1 | Register a team |
| 2 | List registered teams |
| 3 | Generate fixtures |
| 4 | List fixtures |
| 5 | Record a match result |
| 6 | View standings |
| 7 | Save the tournament |
| 8 | Load the tournament |
| 9 | Exit |

Invalid menu choices are rejected and the menu is displayed again. Team registration closes after fixtures have been generated.

## Tournament rules

### Team registration

- A tournament accepts a minimum of 4 and a maximum of 8 teams.
- A team name is trimmed before it is stored.
- The trimmed name must contain 2–30 characters.
- Names are unique under case-insensitive `casefold()` comparison.
- Team IDs are separate from display names, so fixture references do not depend on the spelling of a name.
- Registration is locked after the schedule has been generated.

### Round-robin schedule

Every team plays every other team exactly once. The number of fixtures for (N) teams is:

```text
N × (N - 1) / 2
```

Examples:
- 4 teams produce 6 fixtures.
- 6 teams produce 15 fixtures.
- 8 teams produce 28 fixtures.

A schedule can only be generated once for the current tournament.

### Results and points

A result can be recorded only for an existing pending fixture. Both scores must be nonnegative integers. Boolean values are not valid scores, and a completed fixture cannot receive a second result.

| Match outcome | Points |
|---|---:|
| Win | 3 |
| Draw | 1 per team |
| Loss | 0 |

Standings are calculated from played fixtures. Pending fixtures do not contribute to the table.

### Standings and tie-breakers

Teams are ranked in this order:

1. Points — descending.
2. Goal difference — descending.
3. Goals scored — descending.
4. Normalized team name using `casefold()` — ascending.

Head-to-head results are not an additional tie-breaker.

The standings are marked **in progress** while at least one fixture remains pending. A champion is reported only when all fixtures have been played.

## Example season

The following is an illustrative four-team season, not a claim about the contents of the saved tournament file.

| Fixture | Result |
|---|---|
| Thunder vs Comets | 2–1 |
| Phoenix vs Rockets | 0–0 |

After these two matches, the standings would be:

| Team | P | W | D | L | GF | GA | GD | Pts |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Thunder | 1 | 1 | 0 | 0 | 2 | 1 | +1 | 3 |
| Phoenix | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 1 |
| Rockets | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 1 |
| Comets | 1 | 0 | 0 | 1 | 1 | 2 | -1 | 0 |

The season remains in progress because four fixtures are still pending.

## Saving and loading

Tournament data is saved to `tournament.json` in the project directory. The JSON document contains:

- `schema_version`
- `next_team_number`
- `teams`
- `fixtures`

Standings are not stored; they are recalculated from the saved fixtures after loading. The loader validates the data before the application replaces its active tournament state. The schema version is currently `1`.

The generated `tournament.json` file is runtime data. Do not put private or sensitive information in it.

## Project structure

```text
TournamentLab/
├── main.py
├── tournament/
│   ├── __init__.py
│   ├── teams.py
│   ├── fixtures.py
│   ├── results.py
│   ├── standings.py
│   └── storage.py
├── tests/
│   ├── test_teams.py
│   ├── test_fixtures.py
│   ├── test_results.py
│   ├── test_standings.py
│   └── test_storage.py
└── docs/
    ├── design-decisions.md
    └── ai-learning-log.md
```

### Module responsibilities

- `main.py` — menu, user interaction, and application state.
- `teams.py` — team-name validation, team IDs, registration, and listing.
- `fixtures.py` — deterministic round-robin fixture generation.
- `results.py` — score validation and one-time result recording.
- `standings.py` — standings aggregation, ranking, tournament status, and champion selection.
- `storage.py` — JSON serialization, schema/data validation, and loading.
- `tests/` — automated unit tests for the application modules.

## Running the tests

From the repository root:

```powershell
py -m unittest discover -s tests -v
```

The project includes unit-test modules for teams, fixtures, results, standings, and storage. The challenge's separate Stage 4 professional test-lab review was intentionally skipped; this README does not claim that the full challenge test checklist has been independently audited.

## Current scope

The current CLI implements registration, scheduling, result entry, standings, champion reporting, and JSON persistence. Editing a completed result, deleting teams, and a demo-fixture simulation workflow are not part of the current CLI.

## Documentation

- [Design decisions](docs/design-decisions.md) — key data-model and business-rule decisions.
- [AI learning log](docs/ai-learning-log.md) — learning cycles and experiments recorded during development.

## Project status

The implementation missions A–F have been completed and the CLI workflow has been manually exercised, including a save/exit/restart/load round trip. Automated test-lab review and the later collaboration/defence stages of the challenge remain separate activities.
