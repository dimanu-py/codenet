Feature: Session refresh
  As an authenticated account
  I want to exchange a refresh token for a new access token
  So that I can keep using the API without logging in again when my access token expires

  @s1
  Scenario: Successful login issues an access token and a refresh token
    Given an account exists with username "johndoe" and password "strongpassword123"
    When the account logs in with valid credentials
    Then the response status is 200
    And the response body contains a non-empty "access_token"
    And the response body contains a non-empty "refresh_token"
    And a new session is persisted for the account

  @s2
  Scenario: Logging in twice creates two independent sessions
    Given an account exists with username "johndoe" and password "strongpassword123"
    And the account has already logged in once, receiving refresh token "RT1"
    When the account logs in again with valid credentials
    Then the response contains a new refresh token "RT2" different from "RT1"
    And both "RT1" and "RT2" remain valid for refreshing

  @s3
  Scenario: Refreshing with a valid refresh token issues a new token pair
    Given an account has a valid, unexpired refresh token "RT1"
    When a refresh request is sent with refresh_token "RT1"
    Then the response status is 200
    And the response body contains a new "access_token"
    And the response body contains a new "refresh_token" different from "RT1"

  @s4
  Scenario: A rotated refresh token cannot be reused
    Given an account has a valid refresh token "RT1"
    And "RT1" has already been used once to refresh successfully
    When a refresh request is sent again with refresh_token "RT1"
    Then the response status is 401
    And the error type is "invalid_refresh_token"

  @s5
  Scenario: Refreshing with an expired refresh token is rejected
    Given an account has a refresh token "RT1" that expired in the past
    When a refresh request is sent with refresh_token "RT1"
    Then the response status is 401
    And the error type is "invalid_refresh_token"

  @s6
  Scenario: Refreshing with a refresh token that was never issued is rejected
    When a refresh request is sent with refresh_token "unknown-token-value"
    Then the response status is 401
    And the error type is "invalid_refresh_token"

  @s7
  Scenario: Refreshing without a refresh_token value is rejected
    When a refresh request is sent with an empty refresh_token
    Then the response status is 422
