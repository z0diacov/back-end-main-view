Feature: Update name

    Scenario Outline: Updating name
        Given <token> and <name>
        When the token is valid and name is correct
        Then the response status code should be <status_code>
        And the response message should be <message> 

    Examples:    
        | token                | name       | status_code | message                                                          |
        | Valid_token_family_3 | None       | 200         | Success                                                          |
        | Valid_token_family_3 | New Name   | 200         | Success                                                          |
        | Valid_token_family_3 | John123    | 422         | Name can only contain letters, hyphens, apostrophes, and spaces  |
        | Valid_token_family_3 | <script>   | 422         | Name can only contain letters, hyphens, apostrophes, and spaces  |
        | Valid_token_family_3 | Мария      | 422         | Name can only contain letters, hyphens, apostrophes, and spaces  |
        | Valid_token_family_3 | John_Doe   | 422         | Name can only contain letters, hyphens, apostrophes, and spaces  |
        | Valid_token_family_3 | J          | 422         | Name can only contain letters, hyphens, apostrophes, and spaces  |
        | Random_type_token    | New Name   | 401         | Invalid token                                                    |
        | Invalid_uid_token    | New Name   | 401         | User does not exist                                              |
        | Expired_token        | New Name   | 401         | Expired token                                                    |
        | Wrong_token          | New Name   | 401         | Invalid token                                                    |
        | Valid_token_family_3 | New Name   | 409         | New name must be different from the old one                      |
        | Nonexistent_token    | New Name   | 401         | User does not exist                                              |
        | None                 | New Name   | 403         | Not authenticated                                                |
        | None                 | New Name   | 403         | Not authenticated                                                |
        | Invalid_iter_token   | New Name   | 403         | User must relogin                                                |

