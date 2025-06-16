Feature: Register

    Scenario Outline: Register user with different credentials
        Given <username>, <password>, <email> and <name> are provided in the request
        When the registration data is processed
        Then the response status code should be <status_code>
        And the response message should be <message>

    Examples:
        | username        | password           | email                 | name        | status_code | message                  |
        | newuser         | @NewUserPass123    | newuser@example.com   | John        | 201         | Successful registration  |
        | anotheruser     | @AnotherPass456    | another@example.com   | None        | 201         | Successful registration  |
        | specialuser     | @ValidPass123      | special@example.com   | Sarah       | 201         | Successful registration  |
        | edgeuser        | @123Abc!           | edge@example.com      | Alexander   | 201         | Successful registration  |
        | newuser         | @NewUserPass123    | newuser@example.com   | James       | 409         | Username already exists  |
        | shortuser       | @short             | short@example.com     | Mark        | 422         | Invalid password         |
        | invalidemailuser| @InvalidPass123    | invalidemail          | Anna        | 422         | Invalid email format     |
        | invalidemailuser| @InvalidPass123    | invalidemail@         | Anna        | 422         | Invalid email format     |
        | emptyuser       | emptypass          | None                  | Emily       | 422         | Validation error         |
        | None            | None               | None                  | None        | 422         | Validation error         |
        | "user123"       | None               | user123@example.com   | Lily        | 422         | Invalid password         |
        | None            | "password"         | user@example.com      | Emma        | 422         | Invalid username         |



