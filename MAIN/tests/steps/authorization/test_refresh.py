from pytest_bdd import scenarios, given, when, then, parsers
from tests.tests_setup import tests_setup
from tests.database_for_tests import redis_client_sync
from security.config import REFRESH_TOKEN_EXPIRE_SECONDS

scenarios("../../features/authorization/refresh.feature")

not_decoded_jwts = tests_setup.create_not_decoded_iter_jwts("refresh")

@given(parsers.parse("{token} is provided"))
def step_given_reset_password(token, data) -> None:
    data['token'] = None if token == "None" else tests_setup.create_token(not_decoded_jwts[token])

@when("token is valid")
def step_when_reset_password(client, data, response_fixture) -> None:
    redis_client_sync.set("whitelist:3", 1, REFRESH_TOKEN_EXPIRE_SECONDS)

    response = client.post(f"/refresh?refresh_token={data['token']}")
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
        assert "access_token" in json_response
        assert "refresh_token" in json_response
        assert json_response["token_type"] == "bearer"
    else:
        assert json_response["detail"] == message