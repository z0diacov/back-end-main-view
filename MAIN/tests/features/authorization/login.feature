Feature: Login

    Scenario Outline: Login user with different credentials
        Given <username> and <password> are provided in query
        When the credentials are processed
        Then the response status code should be <status_code>
        And the response message should be <message>

    Examples:
        | username        | password           | status_code | message                                  |
        | root            | @Rootpassword123   | 200         | Success                                  |
        | admin           | @Adminpassword123  | 200         | Success                                  |
        | user            | @Userpassword123   | 403         | Email not verified                       |
        | user            | @Userpassword122   | 401         | Incorrect username or password           |
        | nonexistentuser | password           | 401         | Incorrect username or password           |
        | root            | wrongpassword      | 401         | Incorrect username or password           |
        | emptyuser       | emptypass          | 401         | Incorrect username or password           |
        | None            | None               | 422         | Invalid user data                        |
        | "root"          | None               | 422         | Invalid user data                        |
        | None            | "password"         | 422         | Invalid user data                        |

