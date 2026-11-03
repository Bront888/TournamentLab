import unittest
from unittest.mock import patch

from tournament.teams import (
    validate_team_name,
    generate_team_id,
    register_team,
    list_teams
)


class TestTeamRegisteration(unittest.TestCase):
    def setUp(self):
        self.teams = []

    def test_valid_team_name(self):
        result = validate_team_name("Red Comets", self.teams)
        self.assertEqual(result, "Red Comets")

    def test_team_name_is_trimmed(self):
        result = validate_team_name(" Red Comets ", self.teams)
        self.assertEqual(result, "Red Comets")

    def test_duplicate_team_name(self):
        self.teams.append({
            "id": "TM001",
            "name": "Red comets"
        })

        with self.assertRaises(ValueError):
            validate_team_name("red comets", self.teams)

    def test_team_id_generation(self):
        self.assertEqual(generate_team_id(1), "TM001")
        self.assertEqual(generate_team_id(5), "TM005")

    def test_team_registration(self):
        team = register_team("Red Comets", self.teams, 1)

        self.assertEqual(team["id"], "TM001")
        self.assertEqual(team["name"], "Red Comets")
        self.assertEqual(len(self.teams), 1)
    
    def test_blank_team_name(self):
        with self.assertRaises(ValueError):
            validate_team_name("   ", self.teams)

    def test_team_name_too_long(self):
        long_name = "A" * 31

        with self.assertRaises(ValueError):
            validate_team_name(long_name, self.teams)

    def test_team_name_too_short(self):
        with self.assertRaises(ValueError):
            validate_team_name("A", self.teams)

    def test_invalid_registration_does_not_change_teams(self):
        with self.assertRaises(ValueError):
            register_team("A", self.teams, 1)

        self.assertEqual(len(self.teams), 0)

    def test_list_teams_when_empty(self):
        with patch("builtins.print") as mock_print:
            list_teams(self.teams)

        mock_print.assert_called_with(
            "No teams have been registered yet."
        )


    def test_list_registered_teams(self):
        self.teams.append({
            "id": "TM001",
            "name": "Red Comets"
        })

        with patch("builtins.print") as mock_print:
            list_teams(self.teams)

        mock_print.assert_called_with("TM001 - Red Comets")

    def test_cannot_register_more_than_eight_teams(self):
        for number in range(1, 9):
            register_team(f"Team {number}", self.teams, number)

        with self.assertRaises(ValueError):
            register_team("Team Nine", self.teams, 9)

        self.assertEqual(len(self.teams), 8)


if __name__ == "__main__":
    unittest.main()
