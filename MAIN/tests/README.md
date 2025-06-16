# Unit Testing

All commands below should be run from the MAIN directory.

## How to run:

1. First, create a virtual environment by running one of the following scripts:
   - scripts/createvenv.ps1 (for PowerShell)
   - scripts/createvenv.bat (for Command Prompt)

2. Then, run unit tests using one of these:
   - scripts/tests.ps1
   - scripts/tests.bat

If you don’t want to run all tests, you can specify the test file like this:
   scripts/tests.bat authorization/test_login.py

All paths are relative to the tests/steps directory.
If you want to run all tests in a specific block/folder, use:
   scripts/tests.bat authorization

# Run all tests
- scripts/tests.bat

# Run all authorization tests
- scripts/tests.bat authorization

# Run specific test files from authorization
- scripts/tests.bat authorization/test_login.py
- scripts/tests.bat authorization/test_logout.py
- scripts/tests.bat authorization/test_refresh.py
- scripts/tests.bat authorization/test_registration.py
- scripts/tests.bat authorization/test_reset_password.py
- scripts/tests.bat authorization/test_verify_email.py
- scripts/tests.bat authorization/test_verify_email_link.py
- scripts/tests.bat authorization/test_forgot_password.py

# Run all profile_and_settings tests
- scripts/tests.bat profile_and_settings

# Run specific test files from profile_and_settings
- scripts/tests.bat profile_and_settings/test_update_name.py
- scripts/tests.bat profile_and_settings/test_update_password.py
- scripts/tests.bat profile_and_settings/test_update_username.py

# Run all sessions tests
- scripts/tests.bat sessions

# Run specific test files from sessions
- scripts/tests.bat sessions/test_close_session.py
- scripts/tests.bat sessions/test_close_sessions.py
- scripts/tests.bat sessions/test_my_active_sessions.py