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
    choice = input("Enter your choice [1-9] :)  ")
    return choice

def main():
    while True:
        display_menu()
        choice = get_user_choice()

        if choice == "9":
            print("Thank you for using TournamentLab!")
            break

        else:
            print("Feature coming soon.")


if __name__ == "__main__":
    main()