Feature: Update email

    Scenario Outline: Updating email
        Given <token>, <otp> and <email>
        When the token is valid and email is correct
        Then the response status code should be <status_code>
        And the response message should be <message> 

    Examples:    
        | token                | otp    | email                 | status_code | message                          |
        | Valid_token_family_3 | 111111 | invalidemail@         | 422         | Must be a valid email address    |
        | Valid_token_family_3 | 111111 | invalidemail          | 422         | Must be a valid email address    |
        | Valid_token_family_3 | 111111 | None                  | 422         | Must be a valid email address    |
        | Random_type_token    | 111111 | newuser@example.com   | 401         | Invalid token                    |
        | Invalid_uid_token    | 111111 | newuser@example.com   | 401         | User does not exist              |
        | Expired_token        | 111111 | newuser@example.com   | 401         | Expired token                    |
        | Wrong_token          | 111111 | newuser@example.com   | 401         | Invalid token                    |
        | Nonexistent_token    | 111111 | newuser@example.com   | 401         | User does not exist              |
        | None                 | 111111 | newuser@example.com   | 403         | Not authenticated                |
        | None                 | 111111 | newuser@example.com   | 403         | Not authenticated                |
        | Invalid_iter_token   | 111111 | newuser@example.com   | 403         | User must relogin                |
        | Valid_token_family_3 | 111112 | newuser@example.com   | 401         | OTP expired or invalid           |
        | Valid_token_family_3 | 111111 | newuser@example.com   | 200         | Success                          |
        | Valid_token_family_2 | 111111 | newuser@example.com   | 409         | New email already exists         |
        