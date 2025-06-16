Feature: Create password 

    Scenario Outline: Updating name
        Given <auth_token>, <token> and <new_password>
        When the token is valid and new_password is correct
        Then the response status code should be <status_code>
        And the response message should be <message> 

    Examples:
        | auth_token                         | token                              | new_password       | status_code | message                                                                       |
        | Google_registrated_no_pass_token   | Google_registrated_no_pass_token   | NoSpecialChar123   | 422         | Password must contain at least one special character (@, $, !, %, *, ?, &)    |
        | Google_registrated_no_pass_token   | Google_registrated_no_pass_token   | nouppercase123!    | 422         | Invalid password: password must contain at least one uppercase letter         |
        | Google_registrated_no_pass_token   | Google_registrated_no_pass_token   | NOLOWERCASE123!    | 422         | Invalid password: password must contain at least one lowercase letter         |
        | Google_registrated_no_pass_token   | Google_registrated_no_pass_token   | NoNumber!!         | 422         | Invalid password: password must contain at least one number                   |
        | Google_registrated_no_pass_token   | Google_registrated_no_pass_token   | None               | 422         | Password field is required                                                    |
        | Google_registrated_no_pass_token   | Google_registrated_no_pass_token   | @Newpass123        | 201         | Success                                                                       |
        | Valid_token_family_2               | Valid_token                        | @Newpass123        | 409         | Token does not belong to current user                                         |
        | Valid_token_family_3               | Valid_token                        | @Newpass123        | 409         | Password already exists                                                       |
        | Random_type_token                  | Valid_token                        | @AnotherPass456    | 401         | Invalid token                                                                 |
        | Invalid_uid_token                  | Valid_token                        | @AnotherPass456    | 401         | User does not exist                                                           |
        | Expired_token                      | Valid_token                        | @AnotherPass456    | 401         | Expired token                                                                 |
        | Wrong_token                        | Valid_token                        | @AnotherPass456    | 401         | Invalid token                                                                 |
        | Nonexistent_token                  | Valid_token                        | @AnotherPass456    | 401         | User does not exist                                                           |
        | None                               | Valid_token                        | @AnotherPass456    | 403         | Not authenticated                                                             |
        | Invalid_iter_token                 | Valid_token                        | @AnotherPass456    | 403         | User must relogin                                                             |
        | Valid_token_family_3               | Expired_token                      | @ValidPass123!     | 401         | Expired token                                                                 |
        | Valid_token_family_3               | Wrong_token                        | @ValidPass123!     | 401         | Invalid token                                                                 |
        | Valid_token_family_3               | None                               | @ValidPass123!     | 422         | Invalid token                                                                 |