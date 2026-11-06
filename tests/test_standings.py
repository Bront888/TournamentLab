import unittest

from tournament.standings import initialize_standings, calculate_standings, rank_standings, get_tournament_status, get_champion
from tournament.fixtures import generate_fixtures
from tournament.results import record_result

class TestStandings(unittest.TestCase):

    def setUp(self):
        self.teams = [
            {"id": "TM001", "name": "Red Comets"},
            {"id": "TM002", "name": "Blue Strikers"},
            {"id": "TM003", "name": "Green Giants"},
        ]

    def test_all_teams_are_initialized(self):
        standings = initialize_standings(self.teams)

        self.assertEqual(len(standings), 3)

    def test_team_ids_are_used_as_keys(self):
        standings = initialize_standings(self.teams)

        self.assertIn("TM001", standings)
        self.assertIn("TM002", standings)
        self.assertIn("TM003", standings)

    def test_initial_statistics_are_zero(self):
        standings = initialize_standings(self.teams)

        red = standings["TM001"]

        self.assertEqual(red["played"], 0)
        self.assertEqual(red["won"], 0)
        self.assertEqual(red["drawn"], 0)
        self.assertEqual(red["lost"], 0)
        self.assertEqual(red["goals_for"], 0)
        self.assertEqual(red["goals_against"], 0)
        self.assertEqual(red["goal_diff"], 0)
        self.assertEqual(red["points"], 0)

    def test_completed_match_updates_statistics(self):
        fixtures = [
            {
                "id": "FX001",
                "team1_id": "TM001",
                "team2_id": "TM002",
                "status": "played",
                "team1_score": 4,
                "team2_score": 2
            }
        ]

        standings = calculate_standings(self.teams, fixtures)

        blue = standings["TM002"]

        self.assertEqual(blue["played"], 1)
        self.assertEqual(blue["goals_for"], 2)
        self.assertEqual(blue["goals_against"], 4)
        self.assertEqual(blue["goal_diff"], -2)
        self.assertEqual(blue["points"], 0)


    def test_pending_match_does_not_affect_standings(self):
        fixtures = [
            {
                "id": "FX001",
                "team1_id": "TM001",
                "team2_id": "TM002",
                "status": "pending",
                "team1_score": None,
                "team2_score": None
            }
        ]

        standings = calculate_standings(self.teams, fixtures)

        self.assertEqual(standings["TM001"]["played"], 0)
        self.assertEqual(standings["TM002"]["played"], 0)


    def test_draw_awards_one_point_each(self):
        fixtures = [
            {
                "id": "FX001",
                "team1_id": "TM001",
                "team2_id": "TM002",
                "status": "played",
                "team1_score": 2,
                "team2_score": 2
            }
        ]

        standings = calculate_standings(self.teams, fixtures)

        self.assertEqual(standings["TM001"]["drawn"], 1)
        self.assertEqual(standings["TM002"]["drawn"], 1)
        self.assertEqual(standings["TM001"]["points"], 1)
        self.assertEqual(standings["TM002"]["points"], 1)

    def test_ranking_uses_points_first(self):
        standings = initialize_standings(self.teams)

        standings["TM001"]["points"] = 6
        standings["TM002"]["points"] = 3

        ranked = rank_standings(standings)

        self.assertEqual(ranked[0]["team_id"], "TM001")


    def test_ranking_uses_goal_difference_as_tiebreaker(self):
        standings = initialize_standings(self.teams)

        standings["TM001"]["points"] = 6
        standings["TM002"]["points"] = 6

        standings["TM001"]["goal_diff"] = 3
        standings["TM002"]["goal_diff"] = 5

        ranked = rank_standings(standings)

        self.assertEqual(ranked[0]["team_id"], "TM002")


    def test_ranking_uses_goals_for_as_third_tiebreaker(self):
        standings = initialize_standings(self.teams)

        for team_id in ("TM001", "TM002"):
            standings[team_id]["points"] = 6
            standings[team_id]["goal_diff"] = 3

        standings["TM001"]["goals_for"] = 12
        standings["TM002"]["goals_for"] = 15

        ranked = rank_standings(standings)

        self.assertEqual(ranked[0]["team_id"], "TM002")


    def test_ranking_uses_case_insensitive_name_as_final_tiebreaker(self):
        standings = initialize_standings(self.teams)

        ranked = rank_standings(standings)

        self.assertEqual(ranked[0]["name"], "Blue Strikers")

    def test_tournament_is_in_progress_with_pending_fixtures(self):
        fixtures = [
            {
                "id": "FX001",
                "team1_id": "TM001",
                "team2_id": "TM002",
                "status": "played",
                "team1_score": 2,
                "team2_score": 1
            },
            {
                "id": "FX002",
                "team1_id": "TM001",
                "team2_id": "TM003",
                "status": "pending",
                "team1_score": None,
                "team2_score": None
            }
        ]

        self.assertEqual(
            get_tournament_status(fixtures),
            "in_progress"
        )


    def test_no_champion_before_all_fixtures_are_played(self):
        fixtures = [
            {
                "id": "FX001",
                "team1_id": "TM001",
                "team2_id": "TM002",
                "status": "pending",
                "team1_score": None,
                "team2_score": None
            }
        ]

        standings = initialize_standings(self.teams)

        champion = get_champion(standings, fixtures)

        self.assertIsNone(champion)


    def test_champion_is_selected_after_all_fixtures_are_played(self):
        fixtures = [
            {
                "id": "FX001",
                "team1_id": "TM001",
                "team2_id": "TM002",
                "status": "played",
                "team1_score": 3,
                "team2_score": 1
            }
        ]

        standings = calculate_standings(self.teams, fixtures)

        champion = get_champion(standings, fixtures)

        self.assertEqual(champion["team_id"], "TM001")


    def test_empty_tournament_is_not_started(self):
        self.assertEqual(get_tournament_status([]), "not_started")

    def test_win_awards_three_points_and_loss_zero(self):
        fixtures = [
            {
                "id": "FX001",
                "team1_id": "TM001",
                "team2_id": "TM002",
                "status": "played",
                "team1_score": 3,
                "team2_score": 1
            }
        ]

        standings = calculate_standings(self.teams, fixtures)

        red = standings["TM001"]
        blue = standings["TM002"]

        self.assertEqual(red["won"], 1)
        self.assertEqual(red["points"], 3)
        self.assertEqual(blue["lost"], 1)
        self.assertEqual(blue["points"], 0)

    def test_champion_waits_for_all_six_fixtures(self):
        teams = [
            {"id": "TM001", "name": "Thunder"},
            {"id": "TM002", "name": "Comets"},
            {"id": "TM003", "name": "Phoenix"},
            {"id": "TM004", "name": "Rockets"},
        ]

        fixtures = generate_fixtures(teams)

        self.assertEqual(len(fixtures), 6)

        for fixture in fixtures[:5]:
            record_result(
                fixtures,
                fixture["id"],
                2,
                1
            )

        standings = calculate_standings(teams, fixtures)

        self.assertIsNone(get_champion(standings, fixtures))


        record_result(
            fixtures,
            fixtures[5]["id"],
            1,
            1
        )

        champion = get_champion(standings, fixtures)

        self.assertIsNotNone(champion)
        self.assertEqual(champion["team_id"], "TM001")

    if __name__ == "__main__":
        unittest.main()