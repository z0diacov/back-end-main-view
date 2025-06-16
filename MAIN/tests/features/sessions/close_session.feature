Feature: Close session

    Scenario Outline: Closing session
        Given <token> and <session_id> is provided
        When token is valid
        Then the response status code should be <status_code>
        And the response message should be <message>

    Examples:    
    | token                    | session_id | status_code | message                                          |
    | Valid_token_family_2     | 3          | 401         | Invalid token                                    |
    | Valid_token_family_3     | None       | 422         | Not authenticated                                |
    | Valid_token_family_3     | 3          | 409         | This session is current, can't logout this way   |
    | Valid_token_family_3     | 2          | 200         | Success                                          |
    | Expired_token            | 1          | 401         | Expired token                                    |
    | Wrong_token              | 1          | 401         | Invalid token                                    |
    | Nonexistent_token        | 1          | 401         | User does not exist                              |
    | Random_type_token        | 1          | 401         | Invalid token                                    |
    | Invalid_uid_token        | 1          | 401         | User does not exist                              |
    | Invalid_iter_token       | 1          | 403         | User must relogin                                |
    | Valid_token_family_3     | 4          | 403         | Session does not belong to the authenticated user|
    | None                     | 1          | 403         | Not authenticated                                |


