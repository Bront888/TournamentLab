import json
import os
import tempfile
import unittest

from tournament.storage import save_tournament, load_tournament, validate_tournament_data, validate_teams, validate_fixtures, validate_complete_tournament
from tournament.standings import calculate_standings

class TestTournamentStorage(unittest.TestCase):

    def setUp(self):
        self.teams = [
            {"id": "TM001", "name": "Red Comets"},
            {"id": "TM002", "name": "Blue Strikers"}
        ]

        self.fixtures = [
            {
                "id": "FX001",
                "team1_id": "TM001",
                "team2_id": "TM002",
                "status": "played",
                "team1_score": 3,
                "team2_score": 1
            }
        ]

    def test_save_tournament_creates_valid_json(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            filepath = os.path.join(temp_dir, "tournament.json")

            save_tournament(
                filepath,
                self.teams,
                self.fixtures,
                3
            )

            with open(filepath, "r", encoding="utf-8") as file:
                data = json.load(file)

        self.assertEqual(data["schema_version"], 1)
        self.assertEqual(data["next_team_number"], 3)
        self.assertEqual(data["teams"], self.teams)
        self.assertEqual(data["fixtures"], self.fixtures)

    def test_save_tournament_does_not_store_standings(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            filepath = os.path.join(temp_dir, "tournament.json")

            save_tournament(
                filepath,
                self.teams,
                self.fixtures,
                3
            )

            with open(filepath, "r", encoding="utf-8") as file:
                data = json.load(file)

        self.assertNotIn("standings", data)

    def test_load_tournament_restores_saved_data(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            filepath = os.path.join(temp_dir, "tournament.json")

            save_tournament(filepath, self.teams, self.fixtures, 3)

            data = load_tournament(filepath)

        self.assertEqual(data["teams"], self.teams)
        self.assertEqual(data["fixtures"], self.fixtures)
        self.assertEqual(data["next_team_number"], 3)


    def test_load_tournament_returns_dictionary(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            filepath = os.path.join(temp_dir, "tournament.json")

            save_tournament(filepath, self.teams, self.fixtures, 3)

            data = load_tournament(filepath)

        self.assertIsInstance(data, dict)

    def test_valid_tournament_data_is_accepted(self):
        data = {
            "schema_version": 1,
            "next_team_number": 3,
            "teams": self.teams,
            "fixtures": self.fixtures
        }

        self.assertTrue(validate_tournament_data(data))


    def test_unsupported_schema_version_is_rejected(self):
        data = {
            "schema_version": 2,
            "next_team_number": 3,
            "teams": self.teams,
            "fixtures": self.fixtures
        }

        with self.assertRaises(ValueError):
            validate_tournament_data(data)


    def test_missing_required_field_is_rejected(self):
        data = {
            "schema_version": 1,
            "teams": self.teams,
            "fixtures": self.fixtures
        }

        with self.assertRaises(ValueError):
            validate_tournament_data(data)


    def test_invalid_team_counter_is_rejected(self):
        data = {
            "schema_version": 1,
            "next_team_number": True,
            "teams": self.teams,
            "fixtures": self.fixtures
        }

        with self.assertRaises(ValueError):
            validate_tournament_data(data)

    def test_valid_teams_are_accepted(self):
        self.assertTrue(validate_teams(self.teams))


    def test_duplicate_team_ids_are_rejected(self):
        teams = [
            {"id": "TM001", "name": "Red Comets"},
            {"id": "TM001", "name": "Blue Strikers"}
        ]

        with self.assertRaises(ValueError):
            validate_teams(teams)


    def test_duplicate_team_names_are_rejected(self):
        teams = [
            {"id": "TM001", "name": "Red Comets"},
            {"id": "TM002", "name": " red comets "}
        ]

        with self.assertRaises(ValueError):
            validate_teams(teams)


    def test_invalid_team_name_length_is_rejected(self):
        teams = [
            {"id": "TM001", "name": "A"}
        ]

        with self.assertRaises(ValueError):
            validate_teams(teams)


    def test_non_dictionary_team_is_rejected(self):
        with self.assertRaises(ValueError):
            validate_teams(["Red Comets"])

    def test_valid_fixtures_are_accepted(self):
        self.assertTrue(validate_fixtures(self.fixtures, self.teams))


    def test_unknown_team_reference_is_rejected(self):
        fixtures = [self.fixtures[0].copy()]
        fixtures[0]["team2_id"] = "TM999"

        with self.assertRaises(ValueError):
            validate_fixtures(fixtures, self.teams)


    def test_self_fixture_is_rejected(self):
        fixtures = [self.fixtures[0].copy()]
        fixtures[0]["team2_id"] = "TM001"

        with self.assertRaises(ValueError):
            validate_fixtures(fixtures, self.teams)


    def test_duplicate_fixture_pairing_is_rejected(self):
        fixtures = [
            self.fixtures[0],
            {
                **self.fixtures[0],
                "id": "FX002",
                "team1_id": "TM002",
                "team2_id": "TM001"
            }
        ]

        with self.assertRaises(ValueError):
            validate_fixtures(fixtures, self.teams)


    def test_negative_played_score_is_rejected(self):
        fixtures = [self.fixtures[0].copy()]
        fixtures[0]["team1_score"] = -1

        with self.assertRaises(ValueError):
            validate_fixtures(fixtures, self.teams)


    def test_boolean_played_score_is_rejected(self):
        fixtures = [self.fixtures[0].copy()]
        fixtures[0]["team1_score"] = True

        with self.assertRaises(ValueError):
            validate_fixtures(fixtures, self.teams)


    def test_pending_fixture_with_score_is_rejected(self):
        fixtures = [self.fixtures[0].copy()]
        fixtures[0]["status"] = "pending"
        fixtures[0]["team1_score"] = 3

        with self.assertRaises(ValueError):
            validate_fixtures(fixtures, self.teams)

    def test_courier_must_exceed_highest_team_id(self):
        data = {
            "schema_version": 1,
            "next_team_number": 2,
            "teams": [
                {"id": "TM001", "name": "Red Comets"},
                {"id": "TM004", "name": "Blue Strikers"}
            ],
            "fixtures": []
        }

        with self.assertRaises(ValueError):
            validate_complete_tournament(data)

    def test_invalid_team_id_format_is_rejected(self):
        teams = [
            {"id": "TEAM001", "name": "Red Comets"}
        ]

        with self.assertRaises(ValueError):
            validate_teams(teams)

    def test_loaded_tournament_preserves_standings(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            filepath = os.path.join(temp_dir, "tournament.json")

            original_standings = calculate_standings(
                self.teams,
                self.fixtures
            )

            save_tournament(filepath, self.teams, self.fixtures, 3)
            loaded_data = load_tournament(filepath)

            restored_standings = calculate_standings(
                loaded_data["teams"],
                loaded_data["fixtures"]
            )

        self.assertEqual(original_standings, restored_standings)


if __name__ == "__main__":
    unittest.main()