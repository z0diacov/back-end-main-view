from pytest_bdd import scenarios, given, when, then, parsers
from tests.tests_setup import tests_setup

scenarios("../../features/profile_and_settings/get_trainer_profile.feature")

not_decoded_jwts = tests_setup.create_not_decoded_iter_jwts("access")

@given(parsers.parse("{user_id} is provided"))
def step_given_reset_password(user_id, data) -> None:
    data['user_id'] = None if user_id == "None" else int(user_id)

@when("user_id and trainer_profile are exist")
def step_when_reset_password(client, data, response_fixture) -> None:

    response = client.get("/trainer/profile", params={"user_id": data['user_id']})
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