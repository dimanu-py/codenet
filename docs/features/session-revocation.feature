Feature: Session revocation
  As an account holder
  I want to revoke a specific session or all of my sessions
  So that I can log out a device or log out everywhere

  @s1
  Scenario: Revoking a session invalidates its refresh token
    Given an account has a valid, unexpired refresh token "RT1"
    When a revoke request is sent with refresh_token "RT1"
    Then the response status is 200
    And the response body contains "revoked": true
    And refreshing with "RT1" afterwards fails with error type "invalid_refresh_token"

  @s2
  Scenario: Revoking one session does not affect the account's other sessions
    Given an account has two valid, unexpired refresh tokens "RT1" and "RT2" from separate logins
    When a revoke request is sent with refresh_token "RT1"
    Then refreshing with "RT2" afterwards still succeeds

  @s3
  Scenario: Revoking an unknown or already-revoked refresh token still reports success
    Given "RT1" does not correspond to any existing session
    When a revoke request is sent with refresh_token "RT1"
    Then the response status is 200
    And the response body contains "revoked": true

  @s4
  Scenario: Revoking without a refresh_token value is rejected
    When a revoke request is sent with an empty refresh_token
    Then the response status is 422

  @s5
  Scenario: Revoking all sessions invalidates every session's refresh token
    Given an account has two valid, unexpired refresh tokens "RT1" and "RT2" from separate logins
    And the account has a valid, unexpired access token "AT1" from one of those logins
    When a revoke-all request is sent with Authorization bearer "AT1"
    Then the response status is 200
    And the response body contains "revoked": true
    And refreshing with "RT1" afterwards fails with error type "invalid_refresh_token"
    And refreshing with "RT2" afterwards fails with error type "invalid_refresh_token"

  @s6
  Scenario: Revoking all sessions requires a valid access token
    When a revoke-all request is sent without an Authorization header
    Then the response status is 401
    And the error type is "invalid_access_token"

  @s7
  Scenario: Revoking all sessions is rejected when the access token is expired
    Given an account has an access token "AT1" that expired in the past
    When a revoke-all request is sent with Authorization bearer "AT1"
    Then the response status is 401
    And the error type is "invalid_access_token"
