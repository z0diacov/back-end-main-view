Feature: Verify email

    Scenario Outline: Verifying email
        Given <token> is provided
        When the verification link is accessed
        Then the response status code should be <status_code>
        And the response message should be <message>

    Examples:    
        | token                    | status_code | message                                |
        | Verify_email_token       | 200         | Success                                |
        | Expired_token            | 401         | Expired token                          |
        | Wrong_token              | 401         | Invalid token                          |
        | Already_verified         | 409         | The email has already been verified    |
        | Nonexistent_token        | 404         | User not found                         |
        | Random_type_token        | 401         | Invalid token                          |
        | Invalid_email_token      | 401         | Invalid token                          |