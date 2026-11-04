from tournament.teams import MIN_TEAMS, MAX_TEAMS

def generate_fixtures(teams):
    if len(teams) < MIN_TEAMS:
        raise ValueError("At least 4 teams are required.")

    if len(teams) > MAX_TEAMS:
        raise ValueError("A tournament cannot have more than 8 teams.")

    fixtures = []
    fixture_number = 1

    for i in range(len(teams)):
        for j in range(i +1, len(teams)):
            fixture = {
                "id": f"FX{fixture_number:03d}",
                "team1_id": teams[i]["id"],
                "team2_id": teams[j]["id"],
                "status": "pending",
                "team1_score": None,
                "team2_score": None
            }

            fixtures.append(fixture)
            fixture_number += 1

    return fixtures