from pytest_bdd import scenarios, given, when, then, parsers
from tests.tests_setup import tests_setup
from tests.database_for_tests import redis_client_sync
from security.config import ACCESS_TOKEN_EXPIRE_SECONDS, OTP_EXPIRE_SECONDS

scenarios("../../features/profile_and_settings/update_email.feature")

not_decoded_jwts = tests_setup.create_not_decoded_iter_jwts("access")

@given(parsers.parse("{token}, {otp} and {email}"))
def step_given_reset_password(token, email, otp, data):
    data['email'] = None if email == "None" else email
    data['otp'] = None if otp == "None" else otp
    data['token'] = None if token == "None" else tests_setup.create_token(not_decoded_jwts[token])

@when("the token is valid and email is correct")
def step_when_reset_password(client, data, response_fixture):
    json_data = {
        "data": {
            "email": data['email']
        },
        "otp": {
            "otp": data['otp']
        }
        
    }

    redis_client_sync.set("whitelist:2", 1, ACCESS_TOKEN_EXPIRE_SECONDS)
    redis_client_sync.set("whitelist:3", 1, ACCESS_TOKEN_EXPIRE_SECONDS)
    redis_client_sync.set("otp:1", "111111", OTP_EXPIRE_SECONDS)

    if data['token'] == None:
        response = client.put("/email", json=json_data)
    else:
        response = client.put("/email", json=json_data, headers={"Authorization": f"Bearer {data['token']}"})
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
    elif response.status_code == 200: 
        pass
    else:
        assert response.json()["detail"] == message