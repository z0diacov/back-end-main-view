from pytest_bdd import scenarios, given, when, then, parsers
from tests.tests_setup import tests_setup
from tests.database_for_tests import redis_client_sync
from security.config import ACCESS_TOKEN_EXPIRE_SECONDS

scenarios("../../features/profile_and_settings/create_google_password.feature")

not_decoded_jwts = tests_setup.create_not_decoded_jwts("google_add_password")
not_decoded_auth_jwts = tests_setup.create_not_decoded_iter_jwts("access")

@given(parsers.parse("{auth_token}, {token} and {new_password}"))
def step_given_add_google_password(auth_token, token, new_password, data):
    data['auth_token'] = None if auth_token == "None" else tests_setup.create_token(not_decoded_auth_jwts[auth_token])
    data['token'] = None if token == "None" else tests_setup.create_token(not_decoded_jwts[token])
    data['new_password'] = None if new_password == "None" else new_password

@when("the token is valid and new_password is correct")
def step_when_reset_password(client, data, response_fixture):
    json_data = {
        'new_password': data['new_password'],
        'token': data['token']
    }

    redis_client_sync.set("whitelist:2", 1, ACCESS_TOKEN_EXPIRE_SECONDS)
    redis_client_sync.set("whitelist:3", 1, ACCESS_TOKEN_EXPIRE_SECONDS)
    redis_client_sync.set("whitelist:5", 1, ACCESS_TOKEN_EXPIRE_SECONDS)

    if data['auth_token'] == None:
        response = client.post("/google/password", json=json_data)
    else:
        response = client.post("/google/password", json=json_data, headers={"Authorization": f"Bearer {data['auth_token']}"})

    response_fixture['response'] = response

@then(parsers.parse("the response status code should be {status_code}"))
def step_then_status_code(response_fixture, status_code) -> None:
    response = response_fixture['response']
    assert response.status_code == int(status_code)

@then(parsers.parse("the response message should be {message}"))
def step_then_message(response_fixture, message) -> None:
    response = response_fixture['response']

    if response.status_code == 201:
        pass
    elif response.status_code == 422:
        assert "detail" in response.json()
        details = response.json()["detail"]
        assert isinstance(details, list)
        for error in details:
            assert "loc" in error
            assert "msg" in error
            assert "type" in error
    else:
        assert response.json()["detail"] == message