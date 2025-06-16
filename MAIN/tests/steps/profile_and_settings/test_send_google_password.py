from pytest_bdd import scenarios, given, when, then, parsers
from tests.tests_setup import tests_setup
from tests.database_for_tests import redis_client_sync
from security.config import ACCESS_TOKEN_EXPIRE_SECONDS

scenarios("../../features/profile_and_settings/send_google_password.feature")

not_decoded_auth_jwts = tests_setup.create_not_decoded_iter_jwts("access")

@given(parsers.parse("{auth_token}"))
def step_given_auth_token(auth_token, data):
    data['auth_token'] = None if auth_token == "None" else tests_setup.create_token(not_decoded_auth_jwts[auth_token])

@when("the token is valid")
def step_when_token_is_valid(client, data, response_fixture):
    redis_client_sync.set("whitelist:3", 1, ACCESS_TOKEN_EXPIRE_SECONDS)
    redis_client_sync.set("whitelist:5", 1, ACCESS_TOKEN_EXPIRE_SECONDS)

    if data['auth_token'] == None:
        response = client.post("/google/password/send")
    else:
        response = client.post("/google/password/send", headers={"Authorization": f"Bearer {data['auth_token']}"})

    response_fixture['response'] = response


@then(parsers.parse("the response status code should be {status_code}"))
def step_then_status_code(response_fixture, status_code) -> None:
    response = response_fixture['response']
    assert response.status_code == int(status_code)

@then(parsers.parse("the response message should be {message}"))
def step_then_message(response_fixture, message) -> None:
    response = response_fixture['response']
    
    if response.status_code == 200:
        pass
    else:
        assert response.json()["detail"] == message