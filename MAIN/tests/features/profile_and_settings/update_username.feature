Feature: Update username

    Scenario Outline: Updating username
        Given <token>, <otp> and <username>
        When the token is valid and username is correct
        Then the response status code should be <status_code>
        And the response message should be <message> 

    Examples:    
        | token                | otp    | username   | status_code | message                                                          |
        | Valid_token_family_3 | 111111 | John 123   | 422         | Username can only contain letters, numbers, and underscores      |
        | Valid_token_family_3 | 111111 | John-Doe   | 422         | Username can only contain letters, numbers, and underscores      |
        | Valid_token_family_3 | 111111 | john.doe   | 422         | Username can only contain letters, numbers, and underscores      |
        | Valid_token_family_3 | 111111 | john@doe   | 422         | Username can only contain letters, numbers, and underscores      |
        | Valid_token_family_3 | 111111 | Джон123    | 422         | Username can only contain letters, numbers, and underscores      |
        | Valid_token_family_3 | 111111 | john#doe   | 422         | Username can only contain letters, numbers, and underscores      |
        | Valid_token_family_3 | 111111 | john$      | 422         | Username can only contain letters, numbers, and underscores      |
        | Valid_token_family_3 | 111111 | None       | 422         | Username can only contain letters, numbers, and underscores      |
        | Random_type_token    | 111111 | New_Name   | 401         | Invalid token                                                    |
        | Invalid_uid_token    | 111111 | New_Name   | 401         | User does not exist                                              |
        | Expired_token        | 111111 | New_Name   | 401         | Expired token                                                    |
        | Wrong_token          | 111111 | New_Name   | 401         | Invalid token                                                    |
        | Nonexistent_token    | 111111 | New_Name   | 401         | User does not exist                                              |
        | None                 | 111111 | New_Name   | 403         | Not authenticated                                                |
        | None                 | 111111 | New_Name   | 403         | Not authenticated                                                |
        | Invalid_iter_token   | 111111 | New_Name   | 403         | User must relogin                                                |
        | Valid_token_family_3 | 111112 | New_Name   | 401         | OTP expired or invalid                                           |
        | Valid_token_family_3 | 111111 | New_Name   | 200         | Success                                                          |
        | Valid_token_family_2 | 111111 | New_Name   | 409         | New username already exists                                      |
        