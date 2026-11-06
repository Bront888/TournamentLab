import unittest
import tempfile
import os
import json
from unittest.mock import patch

import main

class TestCLIStatePreservation(unittest.TestCase):
    def test_failed_load_preserves_current_tournament(self):
        current_teams = [
            {"id": "TM001", "name": "Thunder"},
            {"id": "TM002", "name": "Comets"}
        ]

        current_fixtures = [
            {
                "id": "FX001",
                "team1_id": "TM001",
                "team2_id": "TM002",
                "status": "played",
                "team1_score": 2,
                "team2_score": 1,
            }
        ]

        main.teams = current_teams.copy()
        main.fixtures = current_fixtures.copy()
        main.next_team_number = 3

        with tempfile.TemporaryDirectory() as temp_dir:
            filepath = os.path.join(temp_dir, "invalid.json")

            invalid_data = {
                "schema_version": 1,
                "next_team_number": 3,
                "teams": current_teams,
                "fixtures": [
                    {
                        "id": "FX001",
                        "team1_id": "TM001",
                        "team2_id": "TM002",
                        "status": "played",
                        "team1_score": 2,
                        "team1_score": 1
                    }
                ]
            }

            with open(filepath, "w", encoding="utf-8") as file:
                json.dump(invalid_data, file)

            with patch.object(main, "SAVE_FILE", filepath):
                main.handle_load_tournament()

        self.assertEqual(main.teams, current_teams)
        self.assertEqual(main.fixtures, current_fixtures)
        self.assertEqual(main.next_team_number, 3)

if __name__ == "__main__":
    unittest.main()