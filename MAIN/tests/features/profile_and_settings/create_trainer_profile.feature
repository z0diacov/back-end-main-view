Feature: Create trainer profile

    Scenario Outline: Creating trainer profile
        Given <token> and <trainer_bio>
        When the token is valid and trainer_bio is correct
        Then the response status code should be <status_code>
        And the response message should be <message> 

    Examples:
        | token                | trainer_bio                                                                                     | status_code | message                        |
        | Valid_token_family_3 | Certified personal trainer with 7 years of experience in strength training and rehabilitation.  | 409         | Trainer profile already exists |
        | Valid_token_family_2 | 123123                                                                                          | 422         | Trainer bio is too short       |
        | Valid_token_family_2 | None                                                                                            | 422         | Trainer bio is too short       |
        | Valid_token_family_2 | Certified personal trainer with 7 years of experience in strength training and rehabilitation.  | 201         | Success                        |
        | Random_type_token    | Certified personal trainer with 6 years of experience in strength training and rehabilitation.  | 401         | Invalid token                  |
        | Invalid_uid_token    | Certified personal trainer with 6 years of experience in strength training and rehabilitation.  | 401         | User does not exist            |
        | Expired_token        | Certified personal trainer with 6 years of experience in strength training and rehabilitation.  | 401         | Expired token                  |
        | Wrong_token          | Certified personal trainer with 6 years of experience in strength training and rehabilitation.  | 401         | Invalid token                  |
        | Nonexistent_token    | Certified personal trainer with 6 years of experience in strength training and rehabilitation.  | 401         | User does not exist            |
        | None                 | Certified personal trainer with 6 years of experience in strength training and rehabilitation.  | 403         | Not authenticated              |
        | None                 | Certified personal trainer with 6 years of experience in strength training and rehabilitation.  | 403         | Not authenticated              |
        | Invalid_iter_token   | Certified personal trainer with 6 years of experience in strength training and rehabilitation.  | 403         | User must relogin              |