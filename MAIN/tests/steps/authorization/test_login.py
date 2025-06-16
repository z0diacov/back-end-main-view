from pytest_bdd import scenarios, given, when, then, parsers

scenarios("../../features/authorization/login.feature")

@given(parsers.parse("{username} and {password} are provided in query"))
def step_given_username_password(username, password, data) -> None:
    data['username'] = None if username == "None" else username
    data['password'] = None if password == "None" else password

@when("the credentials are processed")
def step_when_credentials_processed(client, data, response_fixture) -> None:
    json_data = {'username': data['username'], 'password': data['password']}
    response = client.post("/login", json=json_data)
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
