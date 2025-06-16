Feature: Get user profile

    Scenario Outline: Getting user profile
        Given <user_id> is provided
        When user_id is exist
        Then the response status code should be <status_code>
        And the response message should be <message>

    Examples:    
        | user_id | status_code | message             |
        | 1       | 200         | Success             |
        | 2       | 200         | Success             |
        | 3       | 200         | Success             |
        | 9       | 404         | User does not exist |
        | None    | 422         | Invalid uid         |
