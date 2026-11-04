import json


def save_tournament(filepath, teams, fixtures, next_team_number):
    tournament_data = {
        "schema_version": 1,
        "next_team_number": next_team_number,
        "teams": teams,
        "fixtures": fixtures
    }

    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(tournament_data, file, indent=4)


def validate_tournament_data(data):
    if not isinstance(data, dict):
        raise ValueError("Tournament data must be a dictionary.")

    required_keys = {
        "schema_version",
        "next_team_number",
        "teams",
        "fixtures"
    }

    if not required_keys.issubset(data):
        raise ValueError("Tournament data is missing required fields.")

    if type(data["schema_version"]) is not int or data["schema_version"] != 1:
        raise ValueError("Unsupported tournament schema version.")

    if type(data["next_team_number"]) is not int:
        raise ValueError("Invalid team ID counter.")

    if data["next_team_number"] < 1:
        raise ValueError("Team ID counter must be positive.")

    if not isinstance(data["teams"], list):
        raise ValueError("Teams must be stored as a list.")

    if not isinstance(data["fixtures"], list):
        raise ValueError("Fixtures must be stored as a list.")

    return True

def validate_teams(teams):
    team_ids = set()
    team_names = set()

    for team in teams:
        if not isinstance(team, dict):
            raise ValueError("Each team must be a dictionary.")

        if not {"id", "name"}.issubset(team):
            raise ValueError("Team is missing required fields.")

        team_id = team["id"]
        name = team["name"]

        if (
            not isinstance(team_id, str)
            or not team_id.startswith("TM")
            or len(team_id[2:]) < 3
            or not team_id[2:].isdigit()
        ):
            raise ValueError("Invalid team ID format.")

        if not isinstance(team_id, str) or not team_id:
            raise ValueError("Invalid team ID.")

        if not isinstance(name, str):
            raise ValueError("Team name must be text.")

        clean_name = name.strip()

        if not 2 <= len(clean_name) <= 30:
            raise ValueError("Invalid team name length.")

        if team_id in team_ids:
            raise ValueError("Duplicate team ID.")

        normalized_name = clean_name.casefold()

        if normalized_name in team_names:
            raise ValueError("Duplicate team name.")

        team_ids.add(team_id)
        team_names.add(normalized_name)

    return True

def validate_fixtures(fixtures, teams):
    team_ids = {team["id"] for team in teams}

    fixture_ids = set()
    match_pairs = set()

    required_fields = {
        "id",
        "team1_id",
        "team2_id",
        "status",
        "team1_score",
        "team2_score"
    }

    for fixture in fixtures:
        expected_fixture_count = len(teams) * (len(teams) - 1) // 2

        if fixtures and len(fixtures) != expected_fixture_count:
            raise ValueError("Tournament fixture schedule is incomplete.")

        if not isinstance(fixture, dict):
            raise ValueError("Each fixture must be a dictionary.")

        if not required_fields.issubset(fixture):
            raise ValueError("Fixture is missing required fields.")

        fixture_id = fixture["id"]
        team1_id = fixture["team1_id"]
        team2_id = fixture["team2_id"]
        status = fixture["status"]
        score1 = fixture["team1_score"]
        score2 = fixture["team2_score"]

        if not isinstance(fixture_id, str) or not fixture_id:
            raise ValueError("Invalid fixture ID.")

        if fixture_id in fixture_ids:
            raise ValueError("Duplicate fixture ID.")

        if not isinstance(team1_id, str) or not isinstance(team2_id, str):
            raise ValueError("Fixture team IDs must be text.")

        if team1_id not in team_ids or team2_id not in team_ids:
            raise ValueError("Fixture references an unknown team.")

        if team1_id == team2_id:
            raise ValueError("A team cannot play itself.")

        pair = frozenset((team1_id, team2_id))

        if pair in match_pairs:
            raise ValueError("Duplicate fixture pairing.")

        if status not in ("pending", "played"):
            raise ValueError("Invalid fixture status.")

        if status == "pending":
            if score1 is not None or score2 is not None:
                raise ValueError("Pending fixtures cannot have scores.")

        else:
            if type(score1) is not int or score1 < 0:
                raise ValueError("Invalid first team score.")

            if type(score2) is not int or score2 < 0:
                raise ValueError("Invalid second team score.")

        fixture_ids.add(fixture_id)
        match_pairs.add(pair)

    return True

def validate_complete_tournament(data):
    validate_tournament_data(data)
    validate_teams(data["teams"])
    validate_fixtures(data["fixtures"], data["teams"])
    team_numbers = [
        int(team["id"][2:])
        for team in data["teams"]
    ]

    if team_numbers and data["next_team_number"] <= max(team_numbers):
        raise ValueError("Team ID counter would cause ID reuse.")

    return True

def load_tournament(filepath):
    with open(filepath, "r", encoding="utf-8") as file:
        tournament_data = json.load(file)
    validate_complete_tournament(tournament_data)
    return tournament_data