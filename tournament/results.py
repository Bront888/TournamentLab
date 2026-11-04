'''
A result can only be recorded when:
1. The fixture ID exists.
2. The fixture is still pending.
3. Both scores are integers.
4. Neither score is negative.
4. Neither score is a boolean (True and False must be rejected).
'''

def validate_score(score):
    if type(score)is not int:
        raise ValueError("Score must be an Integer.")

    if score < 0:
        raise ValueError("Score cannot be negative.")

    return score

def record_result(fixtures, fixture_id, team1_score, team2_score):
    
    target_fixture = None

    for fixture in fixtures:
        if fixture["id"] == fixture_id:
            target_fixture = fixture
            break

    if target_fixture is None:
        raise ValueError("Fixture not found.")

    if target_fixture["status"] != "pending":
        raise ValueError("This fixture has already been played.")

    #validate both scores before changing the fixture.
    validate_score(team1_score)
    validate_score(team2_score)

    #Now we commit result
    target_fixture["team1_score"] = team1_score
    target_fixture["team2_score"] = team2_score
    target_fixture["status"] = "played"

    return target_fixture