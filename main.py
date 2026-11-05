from tournament.teams import register_team, list_teams
from tournament.fixtures import generate_fixtures
from tournament.results import record_result
from tournament.standings import (
    calculate_standings,
    rank_standings,
    get_tournament_status,
    get_champion
)
from tournament.storage import save_tournament, load_tournament


# Application state
teams = []
fixtures = []
next_team_number = 1

SAVE_FILE = "tournament.json"

def display_menu():
    print("\n========== TOURNAMENTLAB ==========")
    print("         1. Register a team")
    print("       2. List registered teams")
    print("         3. Generate fixtures")
    print("           4. List fixtures")
    print("        5. Record match result")
    print("           6. View standings")
    print("           7. Save tournament")
    print("           8. Load tournament")
    print("               9. Exit")
    print("==================================")

def get_user_choice():
    choice = input("Enter your choice [1-9] :)  ").strip()
    if choice not in ("1", "2", "3", "4", "5", "6", "7", "8", "9"):
        raise ValueError("Invalid choice. Please select a number from 1 to 9.")

    return choice


def handle_team_registration():
    global next_team_number

    if fixtures:
        print("Team registration is closed because fixtures have been generated.")
        return
    
    name = input("Enter team name: ")

    try:
        team = register_team(name, teams, next_team_number)

    except ValueError as error:
        print(f"Registration failed: {error}")
    
    else:
        next_team_number += 1
        print(f"Successfully registered: {team['name']}")
        print(f"Team ID: {team['id']}")

def handle_list_teams():
    print("\n--- REGISTERED TEAMS ---")
    list_teams(teams)

def handle_generate_fixtures():
    if fixtures:
        print("Fixtures have already been generated.")
        return
    
    try:
        generate_fixture = generate_fixtures(teams)
    except ValueError as error:
        print(f"Fixture generation failed: {error}")
    else:
        fixtures.extend(generate_fixture)
        print(f"Successfully generated {len(fixtures)} fixtures.")

def handle_list_fixtures():
    if not fixtures:
        print("No fixtures have been generated yet.")
        return
    
    print("\n========== TOURNAMENT FIXTURES ==========")

    for fixture in fixtures:
        team1 = next(
            team for team in teams
            if team["id"] == fixture["team1_id"]
        )

        team2 = next(
            team for team in teams
            if team["id"] == fixture["team2_id"]
        )

        if fixture["status"] == "played":
            result = (
                f"{fixture['team1_score']} - "
                f"{fixture['team2_score']}"
            )
        
        else:
            result = "Pending"

        print(
            f"{fixture['id']} | "
            f"{team1['name']} vs {team2['name']} | "
            f"{result}"
        )

def handle_record_result():
    if not fixtures:
        print("Generate fixtures before recording results.")
        return

    fixture_id = input("Enter fixture ID: ").strip()

    team1_score = input("Enter first team's score: ")
    team2_score = input("Enter second team's score: ")

    try:
        score1 = int(team1_score)
        score2 = int(team2_score)

        record_result(
            fixtures,
            fixture_id,
            score1,
            score2
        )

    except ValueError as error:
        print(f"Result recording failed: {error}")

    else:
        print("Match result recorded successfully.")

def handle_view_standings():
    if not fixtures:
        print("Generate fixtures before viewing standings.")
        return

    standings = calculate_standings(teams, fixtures)
    ranked_teams = rank_standings(standings)

    status = get_tournament_status(fixtures)

    print("\n========== TOURNAMENT STANDINGS ==========")
    print(f"Tournament status: {status.upper()}")

    print(
        f"{'TEAM':<20} {'P':>2} {'W':>2} "
        f"{'D':>2} {'L':>2} {'GF':>3} "
        f"{'GA':>3} {'GD':>3} {'PTS':>4}"
    )

    for team in ranked_teams:
        print(
            f"{team['name']:<20} "
            f"{team['played']:>2} "
            f"{team['won']:>2} "
            f"{team['drawn']:>2} "
            f"{team['lost']:>2} "
            f"{team['goals_for']:>3} "
            f"{team['goals_against']:>3} "
            f"{team['goal_diff']:>3} "
            f"{team['points']:>4}"
        )

    if status == "completed":
        champion = get_champion(standings, fixtures)
        print(f"\nChampion: {champion['name']}")
    else:
        print("\nTournament is still in progress.")

def handle_save_tournament():
    try:
        save_tournament(
            SAVE_FILE,
            teams,
            fixtures,
            next_team_number
        )

    except OSError as error:
        print(f"Could not save tournament: {error}")

    else:
        print(f"Tournament saved successfully to {SAVE_FILE}.")

def handle_load_tournament():
    global teams, fixtures, next_team_number

    try:
        loaded_data = load_tournament(SAVE_FILE)

    except (OSError, ValueError) as error:
        print(f"Could not load tournament: {error}")

    else:
        teams = loaded_data["teams"]
        fixtures = loaded_data["fixtures"]
        next_team_number = loaded_data["next_team_number"]

        print("Tournament loaded successfully.")

def main():
    while True:
        display_menu()

        try:
            choice = get_user_choice()
        except ValueError as error:
            print(error)
            continue

        if choice == "1":
            handle_team_registration()
        
        elif choice == "2":
            handle_list_teams()

        elif choice == "3":
            handle_generate_fixtures()

        elif choice == "4":
            handle_list_fixtures()

        elif choice == "5":
            handle_record_result()
        
        elif choice == "6":
            handle_view_standings()
        
        elif choice == "7":
            handle_save_tournament()

        elif choice == "8":
            handle_load_tournament()

        elif choice == "9":
            print("Thank you for using TournamentLab!")
            break


if __name__ == "__main__":
    main()