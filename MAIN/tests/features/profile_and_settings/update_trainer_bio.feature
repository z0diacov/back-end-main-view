Feature: Update trainer bio

    Scenario Outline: Updating trainer bio
        Given <token> and <trainer_bio>
        When the token is valid and trainer_bio is correct
        Then the response status code should be <status_code>
        And the response message should be <message> 

    Examples:    
        | token                | trainer_bio                                                                                     | status_code | message                                                          |
        | Valid_token_family_3 | Certified personal trainer with 7 years of experience in strength training and rehabilitation.  | 200         | Success                                                          |
        | Valid_token_family_3 | Certified personal trainer with 7 years of experience in strength training and rehabilitation.  | 409         | New trainer_bio must be different from the old one               |
        | Valid_token_family_2 | Certified personal trainer with 7 years of experience in strength training and rehabilitation.  | 403         | You must create a trainer profile before updating your bio       |
        | Valid_token_family_3 | John123                                                                                         | 422         | Trainer bio is too short                                         |
        | Random_type_token    | Certified personal trainer with 6 years of experience in strength training and rehabilitation.  | 401         | Invalid token                                                    |
        | Invalid_uid_token    | Certified personal trainer with 6 years of experience in strength training and rehabilitation.  | 401         | User does not exist                                              |
        | Expired_token        | Certified personal trainer with 6 years of experience in strength training and rehabilitation.  | 401         | Expired token                                                    |
        | Wrong_token          | Certified personal trainer with 6 years of experience in strength training and rehabilitation.  | 401         | Invalid token                                                    |
        | Nonexistent_token    | Certified personal trainer with 6 years of experience in strength training and rehabilitation.  | 401         | User does not exist                                              |
        | None                 | Certified personal trainer with 6 years of experience in strength training and rehabilitation.  | 403         | Not authenticated                                                |
        | None                 | Certified personal trainer with 6 years of experience in strength training and rehabilitation.  | 403         | Not authenticated                                                |
        | Invalid_iter_token   | Certified personal trainer with 6 years of experience in strength training and rehabilitation.  | 403         | User must relogin                                                |
