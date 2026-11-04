import unittest

from tournament.fixtures import generate_fixtures

class TestFixtureGeneration(unittest.TestCase):

    def setUp(self):
        self.teams = [
            {"id": "TM001", "name": "Red Comets"},
            {"id": "TM002", "name": "Blue Strikers"},
            {"id": "TM003", "name": "Greens Giants"},
            {"id": "TM004", "name": "Gold Eagles"},
        ]

    def test_four_teams_generate_six_fixtures(self):
        fixtures = generate_fixtures(self.teams)

        self.assertEqual(len(fixtures), 6)

    def test_fixture_ids_are_unique(self):
        fixtures = generate_fixtures(self.teams)

        fixtures_ids = [fixture["id"] for fixture in fixtures]
        
        self.assertEqual(len(fixtures_ids), len(set(fixtures_ids)))

    def test_no_team_plays_itself(self):
        fixtures = generate_fixtures(self.teams)

        for fixture in fixtures:
            self.assertNotEqual(
                fixture["team1_id"],
                fixture["team2_id"]
            )

    def test_all_fixtures_start_as_pending(self):
        fixtures = generate_fixtures(self.teams)

        for fixture in fixtures:
            self.assertEqual(fixture["status"], "pending")
            self.assertIsNone(fixture["team1_score"])
            self.assertIsNone(fixture["team2_score"])

    def test_no_duplicate_pairings(self):
        fixtures = generate_fixtures(self.teams)

        pairs = [
            frozenset((fixture["team1_id"], fixture["team2_id"]))
            for fixture in fixtures
        ]

        self.assertEqual(len(pairs), len(set(pairs)))

    def test_fewer_than_four_teams_is_rejected(self):
        with self.assertRaises(ValueError):
            generate_fixtures(self.teams[:3])

    def test_six_teams_generate_fifteen_fixtures(self):
        six_teams = self.teams + [
            {"id": "TM005", "name": "Silver Wolves"},
            {"id": "TM006", "name": "Black Panthers"}
        ]

        fixtures = generate_fixtures(six_teams)

        self.assertEqual(len(fixtures), 15)

if __name__ == "__main__":
    unittest.main()