from pytest_bdd import scenarios, given, when, then, parsers
from tests.tests_setup import tests_setup

scenarios("../../features/authorization/verify_email.feature")

not_decoded_jwts = tests_setup.create_not_decoded_jwts("verify_email")

@given(parsers.parse("{token} is provided"))
def step_given_reset_password(token, data) -> None:
    data['token'] = None if token == "None" else tests_setup.create_token(not_decoded_jwts[token])

@when("the verification link is accessed")
def step_when_reset_password(client, data, response_fixture) -> None:
    url = f"/verify-email?token={data['token']}"
    response = client.post(url)
    response_fixture['response'] = response

@then(parsers.parse("the response status code should be {status_code}"))
def step_then_status_code(response_fixture, status_code) -> None:
    response = response_fixture['response']
    assert response.status_code == int(status_code)

@then(parsers.parse("the response message should be {message}"))
def step_then_message(response_fixture, message) -> None:
    response = response_fixture['response']
    assert response.json()["detail"] == message