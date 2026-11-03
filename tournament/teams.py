MIN_TEAMS = 4
MAX_TEAMS = 8

MIN_NAME_LENGTH = 2
MAX_NAME_LENGTH = 30

def validate_team_name(name, teams):
    if not isinstance(name, str):
        raise ValueError("Team name must be text.")

    name = name.strip()

    if len(name) < MIN_NAME_LENGTH:
        raise ValueError("Team name is too short.")

    if len(name) > MAX_NAME_LENGTH:
        raise ValueError("Team name is too long.")

    for team in teams:
        if team["name"].casefold() == name.casefold():
            raise ValueError("This team name is already registered.")

    return name

def generate_team_id(next_team_number):
    return f"TM{next_team_number:03d}"

def register_team(name, teams, next_team_number):
    clean_name = validate_team_name(name, teams)
    if len(teams) >= MAX_TEAMS:
        raise ValueError("A tournament cannot have more than 8 teams")

    team_id = generate_team_id(next_team_number)
    new_team = {
        "id": team_id,
        "name": clean_name
    }
    teams.append(new_team)

    return new_team

def list_teams(teams):
    if not teams:
        print("No teams have been registered yet.")
        return

    for team in teams:
        print(f"{team["id"]} - {team["name"]}")

