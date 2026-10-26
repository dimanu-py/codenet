Feature: Change password
  As an authenticated account holder
  I want to change my password
  So that a compromised password stops granting access, on this and every other device

  @s1
  Scenario: Successful password change updates the password and revokes every session
    Given an account exists with password "oldpassword123"
    And the account has a valid, unexpired access token "AT1"
    And the account has valid, unexpired refresh tokens "RT1" and "RT2" from separate logins
    When a change-password request is sent with Authorization bearer "AT1", current_password "oldpassword123" and new_password "newpassword456"
    Then the response status is 200
    And the response body contains "changed": true
    And refreshing with "RT1" afterwards fails with error type "invalid_refresh_token"
    And refreshing with "RT2" afterwards fails with error type "invalid_refresh_token"

  @s2
  Scenario: The session used to change the password is revoked too
    Given an account exists with password "oldpassword123"
    And the account has a valid, unexpired access token "AT1" with refresh token "RT1"
    When a change-password request is sent with Authorization bearer "AT1", current_password "oldpassword123" and new_password "newpassword456"
    Then refreshing with "RT1" afterwards fails with error type "invalid_refresh_token"

  @s3
  Scenario: Changing the password with an incorrect current password is rejected
    Given an account exists with password "oldpassword123"
    And the account has a valid, unexpired access token "AT1"
    When a change-password request is sent with Authorization bearer "AT1", current_password "wrongpassword" and new_password "newpassword456"
    Then the response status is 401
    And the error type is "invalid_current_password"

  @s4
  Scenario: Changing the password without a valid access token is rejected
    When a change-password request is sent without an Authorization header, current_password "oldpassword123" and new_password "newpassword456"
    Then the response status is 401
    And the error type is "invalid_access_token"

  @s5
  Scenario: Changing the password with a missing new_password is rejected
    Given an account exists with password "oldpassword123"
    And the account has a valid, unexpired access token "AT1"
    When a change-password request is sent with Authorization bearer "AT1", current_password "oldpassword123" and an empty new_password
    Then the response status is 422

  @s6
  Scenario: Changing the password with a missing current_password is rejected
    Given an account exists with password "oldpassword123"
    And the account has a valid, unexpired access token "AT1"
    When a change-password request is sent with Authorization bearer "AT1", an empty current_password and new_password "newpassword456"
    Then the response status is 422

  @s7
  Scenario: Logging in again after a password change requires the new password
    Given an account exists with password "oldpassword123"
    And the account has a valid, unexpired access token "AT1"
    And a change-password request has already succeeded, setting new_password "newpassword456"
    When the account logs in with password "oldpassword123"
    Then the response status is 401
    And the error type is "invalid_credentials"
    When the account logs in with password "newpassword456"
    Then the response status is 200
