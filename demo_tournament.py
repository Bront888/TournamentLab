from tournament.teams import register_team
from tournament.fixtures import generate_fixtures
from tournament.results import record_result
from tournament.standings import calculate_standings, rank_standings, get_champion, get_tournament_status
from tournament.storage import save_tournament, load_tournament


teams = []
next_team_number = 1

team_names = [
    "Thunder",
    "Comets",
    "Phoenix",
    "Rockets"
]

for name in team_names:
    register_team(name, teams, next_team_number)
    next_team_number += 1


fixtures = generate_fixtures(teams)

print(f"Registered teams: {len(teams)}")
print(f"Generated fixtures: {len(fixtures)}")


# Record the first match as a win
record_result(fixtures, "FX001", 3, 1)

# Record the second match as a draw
record_result(fixtures, "FX002", 2, 2)


print("\n--- CURRENT FIXTURE STATUS ---")

for fixture in fixtures:
    print(
        fixture["id"],
        fixture["status"],
        fixture["team1_score"],
        fixture["team2_score"]
    )


print("\n--- CURRENT STANDINGS ---")

standings = calculate_standings(teams, fixtures)
ranked_teams = rank_standings(standings)

for team in ranked_teams:
    print(
        team["name"],
        "Played:", team["played"],
        "Won:", team["won"],
        "Drawn:", team["drawn"],
        "Lost:", team["lost"],
        "Points:", team["points"]
    )

print("\nTournament status:", get_tournament_status(fixtures))
print("Champion:", get_champion(standings, fixtures))

print("\n--- INVALID SCORE TEST ---")

standings_before = calculate_standings(teams, fixtures)

try:
    record_result(fixtures, "FX003", -2, 1)
except ValueError as error:
    print("Rejected:", error)

standings_after = calculate_standings(teams, fixtures)

print("Standings unchanged:", standings_before == standings_after)

print("\n--- SAVE AND RELOAD TEST ---")

demo_file = "demo_tournament.json"

save_tournament(
    demo_file,
    teams,
    fixtures,
    next_team_number
)

print("Demonstration tournament saved.")

loaded_data = load_tournament(demo_file)

restored_teams = loaded_data["teams"]
restored_fixtures = loaded_data["fixtures"]

restored_standings = calculate_standings(
    restored_teams,
    restored_fixtures
)

print("Teams preserved:", restored_teams == teams)
print("Fixtures preserved:", restored_fixtures == fixtures)
print(
    "Standings preserved:",
    restored_standings == calculate_standings(teams, fixtures)
)

print("\n--- COMPLETING THE TOURNAMENT ---")

remaining_results = [
    (2, 0),
    (1, 0),
    (2, 1),
    (0, 1)
]

for fixture, scores in zip(
    restored_fixtures[2:],
    remaining_results
):
    record_result(
        restored_fixtures,
        fixture["id"],
        scores[0],
        scores[1]
    )


final_standings = calculate_standings(
    restored_teams,
    restored_fixtures
)

ranked_teams = rank_standings(final_standings)

print("\n--- FINAL STANDINGS ---")

for position, team in enumerate(ranked_teams, start=1):
    print(
        position,
        team["name"],
        "Played:", team["played"],
        "Won:", team["won"],
        "Drawn:", team["drawn"],
        "Lost:", team["lost"],
        "Points:", team["points"]
    )

champion = get_champion(final_standings, restored_fixtures)

print("\nTournament status:", get_tournament_status(restored_fixtures))
print("Champion:", champion["name"] if champion else "None")