from pytest_bdd import scenarios, given, when, then, parsers
from tests.tests_setup import tests_setup
from tests.database_for_tests import redis_client_sync
from security.config import ACCESS_TOKEN_EXPIRE_SECONDS

scenarios("../../features/profile_and_settings/get_current_user_trainer_profile.feature")

not_decoded_jwts = tests_setup.create_not_decoded_iter_jwts("access")

@given(parsers.parse("{token} is provided"))
def step_given_reset_password(token, data) -> None:
    data['token'] = None if token == "None" else tests_setup.create_token(not_decoded_jwts[token])

@when("token is valid")
def step_when_reset_password(client, data, response_fixture) -> None:
    redis_client_sync.set("whitelist:3", 1, ACCESS_TOKEN_EXPIRE_SECONDS)
    redis_client_sync.set("whitelist:2", 1, ACCESS_TOKEN_EXPIRE_SECONDS)

    if data['token'] == None:
        response = client.get("/trainer/me/profile")
    else:
        response = client.get("/trainer/me/profile", headers={"Authorization": f"Bearer {data['token']}"})
    response_fixture['response'] = response

@then(parsers.parse("the response status code should be {status_code}"))
def step_then_status_code(response_fixture, status_code) -> None:
    response = response_fixture['response']
    assert response.status_code == int(status_code)

@then(parsers.parse("the response message should be {message}"))
def step_then_message(response_fixture, message) -> None:
    response = response_fixture['response']
    json_response = response.json()

    if response.status_code == 200:
        assert "trainer_bio" in json_response
        assert "balance" in json_response
    else:
        assert json_response["detail"] == message