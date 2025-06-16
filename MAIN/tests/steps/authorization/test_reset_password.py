from pytest_bdd import scenarios, given, when, then, parsers
from tests.tests_setup import tests_setup

scenarios("../../features/authorization/reset_password.feature")

not_decoded_jwts = tests_setup.create_not_decoded_jwts("reset_password")

@given(parsers.parse("{token} and {new_password}"))
def step_given_reset_password(token, new_password, data):
    data['new_password'] = None if new_password == "None" else new_password
    data['token'] = None if token == "None" else tests_setup.create_token(not_decoded_jwts[token])

@when("the email is processed")
def step_when_reset_password(client, data, response_fixture):
    json_data = {
        "token": data["token"],
        "new_password": data["new_password"]
    }

    response = client.put("/password-forgot", json=json_data)
    response_fixture['response'] = response


@then(parsers.parse("the response status code should be {status_code}"))
def step_then_status_code(response_fixture, status_code) -> None:
    response = response_fixture['response']
    assert response.status_code == int(status_code)

@then(parsers.parse("the response message should be {message}"))
def step_then_message(response_fixture, message) -> None:
    response = response_fixture['response']

    if response.status_code == 422:
        assert "detail" in response.json()
        details = response.json()["detail"]
        assert isinstance(details, list)
        for error in details:
            assert "loc" in error
            assert "msg" in error
            assert "type" in error
    else:
        assert response.json()["detail"] == message