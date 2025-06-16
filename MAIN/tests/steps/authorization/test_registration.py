from pytest_bdd import scenarios, given, when, then, parsers

scenarios("../../features/authorization/registration.feature")

@given(parsers.parse("{username}, {password}, {email} and {name} are provided in the request"))
def step_given_registration_data(username, password, email, name, data) -> None:
    data['username'] = None if username == "None" else username
    data['password'] = None if password == "None" else password
    data['email'] = None if email == "None" else email
    data['name'] = None if name == "None" else name


@when("the registration data is processed")
def step_when_registration_processed(client, data, response_fixture) -> None:
    json_data = {
        'username': data['username'],
        'password': data['password'],
        'email': data['email'],
        'name': data['name']
    }
    response = client.post("/register", json=json_data)
    response_fixture['response'] = response


@then(parsers.parse("the response status code should be {status_code}"))
def step_then_status_code(response_fixture, status_code) -> None:
    response = response_fixture['response']
    assert response.status_code == int(status_code)

@then(parsers.parse("the response message should be {message}"))
def step_then_message(response_fixture, message , data) -> None:
    response = response_fixture['response']

    if response.status_code == 201:
        assert response.json() == {
            "username": data["username"],
            "email": data["email"],
            "name": data["name"]
        }
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