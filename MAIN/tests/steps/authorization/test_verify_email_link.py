from pytest_bdd import scenarios, given, when, then, parsers

scenarios("../../features/authorization/verify_email_link.feature")

@given(parsers.parse("{email} is provided"))
def step_given_reset_password(email, data) -> None:
    data['email'] = None if email == "None" else email

@when("the email is valid")
def step_when_reset_password(client, data, response_fixture) -> None:
    url = f"/verify-email-link?email={data['email']}"
    response = client.post(url)
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