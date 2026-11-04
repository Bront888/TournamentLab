import unittest

from tournament.results import validate_score, record_result

class TestResultRecording(unittest.TestCase):

    def setUp(self):
        self.fixtures = [
            {
                "id": "FX001",
                "team1_id": "TM001",
                "team2_id": "TM002",
                "status": "pending",
                "team1_score": None,
                "team2_score": None
            }
        ]

    def test_valid_score(self):
        self.assertEqual(validate_score(3), 3)

    def test_zero_is_valid_score(self):
        self.assertEqual(validate_score(0), 0)

    def test_negative_score_is_rejected(self):
        with self.assertRaises(ValueError):
            validate_score(-1)

    def test_float_score_is_rejected(self):
        with self.assertRaises(ValueError):
            validate_score(2.6)

    def test_boolean_score_is_rejected(self):
        with  self.assertRaises(ValueError):
            validate_score(True)

    def test_string_score_is_rejected(self):
        with self.assertRaises(ValueError):
            validate_score("3")

    def test_valid_score_is_recorded(self):
        result = record_result(
            self.fixtures,
            "FX001",
            3,
            1
        )

        self.assertEqual(result["team1_score"], 3)
        self.assertEqual(result["team2_score"], 1)
        self.assertEqual(result["status"], "played")

    def test_unknown_fixture_is_rejected(self):
        with self.assertRaises(ValueError):
            record_result(self.fixtures, "FX999", 2, 1)

    def test_duplicate_result_is_rejected(self):
        record_result(self.fixtures, "FX001", 3, 1)

        with self.assertRaises(ValueError):
            record_result(self.fixtures, "FX001", 3, 1)

    def test_invalid_second_score_does_not_modify_fixture(self):
        original = self.fixtures[0].copy()

        with self.assertRaises(ValueError):
            record_result(self.fixtures, "FX001", 3, -1)

        self.assertEqual(self.fixtures[0], original)

    def test_invalid_first_score_does_not_modify_fixture(self):
        original = self.fixtures[0].copy()
    
        with self.assertRaises(ValueError):
            record_result(self.fixtures, "FX001", -1, 2)

        self.assertEqual(self.fixtures[0], original)


if __name__ == "__main__":
    unittest.main()