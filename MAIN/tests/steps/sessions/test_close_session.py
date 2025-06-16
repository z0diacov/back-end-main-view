from pytest_bdd import scenarios, given, when, then, parsers
from tests.tests_setup import tests_setup
from tests.database_for_tests import redis_client_sync
from security.config import ACCESS_TOKEN_EXPIRE_SECONDS

scenarios("../../features/sessions/close_session.feature")

not_decoded_jwts = tests_setup.create_not_decoded_iter_jwts("access")

@given(parsers.parse("{token} and {session_id} is provided"))
def step_given_reset_password(token, session_id, data) -> None:
    data['token'] = None if token == "None" else tests_setup.create_token(not_decoded_jwts[token])
    data['session_id'] = None if session_id == "None" else int(session_id)

@when("token is valid")
def step_when_reset_password(client, data, response_fixture) -> None:
    redis_client_sync.set("whitelist:3", 1, ACCESS_TOKEN_EXPIRE_SECONDS)

    if data['token'] == None:
        response = client.delete("/session")
    else:
        response = client.delete(
            "/session",
            params={"session_id": data['session_id']},
            headers={"Authorization": f"Bearer {data['token']}"},
        )
    response_fixture['response'] = response

@then(parsers.parse("the response status code should be {status_code}"))
def step_then_status_code(response_fixture, status_code) -> None:
    response = response_fixture['response']
    assert response.status_code == int(status_code)

@then(parsers.parse("the response message should be {message}"))
def step_then_message(response_fixture, message) -> None:
    response = response_fixture['response']
    json_response = response.json()

    if response.status_code in {200, 409}:
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
        assert json_response["detail"] == message