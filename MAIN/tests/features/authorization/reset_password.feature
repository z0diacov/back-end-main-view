Feature: Reset password

    Scenario Outline: Resetting password
        Given <token> and <new_password>
        When the email is processed
        Then the response status code should be <status_code>
        And the response message should be <message>

    Examples:    
        | token                | new_password          | status_code | message                                                                                                                            |
        | Verify_email_token   | @StrongPass123!       | 403         | Email not verified                                                                                                                 |
        | Valid_token          | @StrongPass123!       | 200         | Success                                                                                                                            |
        | Valid_token          | @StrongPass1234!      | 401         | Already used token                                                                                                                 |
        | Valid_token          | NoSpecialChar123      | 422         | Password must contain at least one special character (@, $, !, %, *, ?, &)                                                         |
        | Valid_token          | nouppercase123!       | 422         | Invalid password: password must contain at least one uppercase letter                                                              |
        | Valid_token          | NOLOWERCASE123!       | 422         | Invalid password: password must contain at least one lowercase letter                                                              |
        | Valid_token          | NoNumber!!            | 422         | Invalid password: password must contain at least one number                                                                        |
        | Expired_token        | @ValidPass123!        | 401         | Expired token                                                                                                                      |
        | Wrong_token          | @ValidPass123!        | 401         | Invalid token                                                                                                                      |
        | Valid_token          | @StrongPass123!       | 409         | New password must be different from the old one                                                                                    |
        | Nonexistent_token    | @NonexistentPass123!  | 404         | Email not found                                                                                                                    |
        | None                 | None                  | 422         | Invalid token                                                                                                                      |
        | Valid_token          | None                  | 422         | Password field is required                                                                                                         |
        | None                 | @ValidPass123!        | 422         | Invalid token                                                                                                                      |
        | Valid_token          | @Shrt1!               | 422         | Invalid password: password must be at least 8 characters long                                                                      |
        | Valid_token          | "   "                 | 422         | Invalid password: password cannot be empty                                                                                         |
        | Valid_token          | password              | 422         | Invalid password: password must contain at least one uppercase letter, one lowercase letter, one number, and one special character |
