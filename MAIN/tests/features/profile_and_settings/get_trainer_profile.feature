Feature: Get trainer profile

    Scenario Outline: Getting trainer profile
        Given <user_id> is provided
        When user_id and trainer_profile are exist 
        Then the response status code should be <status_code>
        And the response message should be <message>

    Examples:    
        | user_id | status_code | message                   |
        | 1       | 200         | Success                   |
        | 2       | 404         | Trainer profile not found |
        | 3       | 404         | Trainer profile not found |
        | 9       | 404         | User does not exist       |
        | None    | 422         | Invalid uid               |
