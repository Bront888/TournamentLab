def initialize_standings(teams):
    standings = {}

    for team in teams:
        team_id = team["id"]

        standings[team_id] = {
            "team_id": team_id,
            "name": team["name"],
            "played": 0,
            "won": 0,
            "drawn": 0,
            "lost": 0,
            "goals_for": 0,
            "goals_against": 0,
            "goal_diff": 0,
            "points": 0,
        }

    return standings

def calculate_standings(teams, fixtures):
    standings = initialize_standings(teams)

    for fixture in fixtures:
        if fixture["status"] != "played":
            continue

        team1 = standings[fixture["team1_id"]]
        team2 = standings[fixture["team2_id"]]

        score1 = fixture["team1_score"]
        score2 = fixture["team2_score"]

        team1["played"] += 1
        team2["played"] += 1

        team1["goals_for"] += score1
        team1["goals_against"] += score2

        team2["goals_for"] += score2
        team2["goals_against"] += score1

        if score1 > score2:
            team1["won"] += 1
            team2["lost"] += 1
            team1["points"] += 3
        elif score2 > score1:
            team2["won"] += 1
            team1["lost"] += 1
            team2["points"] += 3
        else:
            team1["drawn"] += 1
            team2["drawn"] += 1
            team1["points"] += 1
            team2["points"] += 1

    for team in standings.values():
        team["goal_diff"] = (
            team["goals_for"] - team["goals_against"]
        )

    return standings

def rank_standings(standings):
    return sorted(
        standings.values(),
        key=lambda team: (
            -team["points"],
            -team["goal_diff"],
            -team["goals_for"],
            team["name"].casefold()
        )
    )

def get_tournament_status(fixtures):
    if not fixtures:
        return "not_started"

    for fixture in fixtures:
        if fixture["status"] != "played":
            return "in_progress"

    return "completed"


def get_champion(standings, fixtures):
    status = get_tournament_status(fixtures)

    if status != "completed":
        return None

    ranked = rank_standings(standings)

    return ranked[0]