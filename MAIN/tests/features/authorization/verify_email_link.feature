Feature: Create verify email link

    Scenario Outline: Creating verify email link
        Given <email> is provided
        When the email is valid
        Then the response status code should be <status_code>
        And the response message should be <message>

    Examples:   
        | email                    |status_code  | message                             |
        | user@example.com         | 200         | Success                             |
        | notfound@example.com     | 404         | User not found                      |
        | emptyemail@domain.com    | 404         | User not found                      |
        | root@example.com         | 409         | The email has already been verified |
        | None                     | 422         | Invalid email format                |
        | invalidemail@example     | 422         | Invalid email format                |
        | user@domain              | 422         | Invalid email format                |
        | user@                    | 422         | Invalid email format                |