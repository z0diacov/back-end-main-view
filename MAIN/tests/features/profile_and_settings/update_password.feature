Feature: Update password

    Scenario Outline: Updating password
        Given <token>, <new_password> and <old_password>
        When the token is valid and old_password is correct
        Then the response status code should be <status_code>
        And the response message should be <message> 

    Examples:    
        | token                | new_password          | old_password          | status_code | message                                                                                                                            |
        | Valid_token_family_3 | @StrongPass123!       | @Rootpassword123      | 200         | Success                                                                                                                            |
        | Valid_token_family_3 | @StrongPass1234!      | @Rootpassword123      | 400         | Incorrect old password                                                                                                             |
        | Valid_token_family_3 | NoSpecialChar123      | @StrongPass123!       | 422         | Password must contain at least one special character (@, $, !, %, *, ?, &)                                                         |
        | Valid_token_family_3 | nouppercase123!       | @StrongPass123!       | 422         | Invalid password: password must contain at least one uppercase letter                                                              |
        | Valid_token_family_3 | NOLOWERCASE123!       | @StrongPass123!       | 422         | Invalid password: password must contain at least one lowercase letter                                                              |
        | Valid_token_family_3 | NoNumber!!            | @StrongPass123!       | 422         | Invalid password: password must contain at least one number                                                                        |
        | Random_type_token    | @StrongPass123!       | @StrongPass123!       | 401         | Invalid token                                                                                                                      |
        | Invalid_uid_token    | @StrongPass123!       | @StrongPass123!       | 401         | User does not exist                                                                                                                |
        | Expired_token        | @ValidPass123!        | @StrongPass123!       | 401         | Expired token                                                                                                                      |
        | Wrong_token          | @ValidPass123!        | @StrongPass123!       | 401         | Invalid token                                                                                                                      |
        | Valid_token_family_3 | @StrongPass123!       | @StrongPass123!       | 409         | New password must be different from the old one                                                                                    |
        | Nonexistent_token    | @NonexistentPass123!  | @StrongPass123!       | 401         | User does not exist                                                                                                                |
        | None                 | None                  | @StrongPass123!       | 403         | Not authenticated                                                                                                                  |
        | Valid_token_family_3 | None                  | @StrongPass123!       | 422         | Password field is required                                                                                                         |
        | None                 | @ValidPass123!        | @StrongPass123!       | 403         | Not authenticated                                                                                                                  |
        | Valid_token_family_3 | @Shrt1!               | @StrongPass123!       | 422         | Invalid password: password must be at least 8 characters long                                                                      |
        | Valid_token_family_3 | "   "                 | @StrongPass123!       | 422         | Invalid password: password cannot be empty                                                                                         |
        | Valid_token_family_3 | password              | @StrongPass123!       | 422         | Invalid password: password must contain at least one uppercase letter, one lowercase letter, one number, and one special character |
        | Invalid_iter_token   | @StrongPass123!       | @StrongPass123!       | 403         | User must relogin                                                                                                                  |
