Feature: Forgot password

Scenario Outline: Request password reset with different email addresses
    Given <email> is provided in the request body
    When the email is processed
    Then the response status code should be <status_code>
    And the response message should be <message>

Examples:
    | email                    | status_code | message                                                   |
    | root@example.com         | 200         | Success                                                   |
    | user@example.com         | 403         | Email not verified                                        |
    | notfound@example.com     | 404         | User not found                                            |
    | emptyemail@domain.com    | 404         | User not found                                            |
    | None                     | 422         | Invalid email format                                      |
    | invalidemail@example     | 422         | Invalid email format                                      |
    | user@domain              | 422         | Invalid email format                                      |
    | user@                    | 422         | Invalid email format                                      |