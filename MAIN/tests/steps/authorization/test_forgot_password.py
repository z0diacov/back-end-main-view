from pytest_bdd import scenarios, given, when, then, parsers

scenarios("../../features/authorization/forgot_password.feature")

@given(parsers.parse('{email} is provided in the request body'))
def step_given_email(email, data: dict[str, str | int | bool]) -> None:
    data['email'] = None if email == "None" else email

@when("the email is processed")
def step_when_email_processed(client, data: dict[str, str | int | bool], response_fixture: dict) -> None:
    json_data = {
        'email': data['email']
    }
    response = client.post("/forgot-password", json=json_data)
    response_fixture['response'] = response

@then(parsers.parse("the response status code should be {status_code}"))
def step_then_status_code(response_fixture, status_code) -> None:
    response = response_fixture['response']
    assert response.status_code == int(status_code)

@then(parsers.parse("the response message should be {message}"))
def step_then_message(response_fixture, message) -> None:
    response = response_fixture['response']
    
    if response.status_code != 422:
        assert response.json()["detail"] == message
    else:
        assert "detail" in response.json()
        details = response.json()["detail"]
        assert isinstance(details, list)
        for error in details:
            assert "loc" in error
            assert "msg" in error
            assert "type" in error

