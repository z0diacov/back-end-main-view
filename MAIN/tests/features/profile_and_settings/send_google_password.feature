Feature: Send Google password

    Scenario Outline: Sending google password
        Given <auth_token>
        When the token is valid
        Then the response status code should be <status_code>
        And the response message should be <message>

    Examples:
        | auth_token                         | status_code | message                 |
        | Google_registrated_no_pass_token   | 200         | Success                 |
        | Valid_token_family_3               | 409         | Password already exists |
        | Random_type_token                  | 401         | Invalid token           |
        | Invalid_uid_token                  | 401         | User does not exist     |
        | Expired_token                      | 401         | Expired token           |
        | Wrong_token                        | 401         | Invalid token           |
        | Nonexistent_token                  | 401         | User does not exist     |
        | None                               | 403         | Not authenticated       |
        | Invalid_iter_token                 | 403         | User must relogin       |