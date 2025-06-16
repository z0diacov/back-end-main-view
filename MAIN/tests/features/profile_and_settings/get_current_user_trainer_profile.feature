Feature: Get current user trainer profile

    Scenario Outline: Getting current user trainer profile
        Given <token> is provided
        When token is valid
        Then the response status code should be <status_code>
        And the response message should be <message>

    Examples:    
        | token                    | status_code | message                                |
        | Valid_token_family_3     | 200         | Success                                |
        | Valid_token_family_2     | 403         | User is not a trainer                  |
        | Expired_token            | 401         | Expired token                          |
        | Wrong_token              | 401         | Invalid token                          |
        | Nonexistent_token        | 401         | User does not exist                    |
        | Random_type_token        | 401         | Invalid token                          |
        | Invalid_uid_token        | 401         | User does not exist                    |
        | Invalid_iter_token       | 403         | User must relogin                      |
        | None                     | 403         | Not authenticated                      |