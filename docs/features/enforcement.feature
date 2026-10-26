Feature: Authorization enforcement
  As a system enforcing deny-by-default access control
  I want protected iam actions to require a specific granted rule
  So that only accounts holding the right permission can perform them

  @s1
  Scenario: Calling a protected endpoint without an access token is rejected
    When a create-rule request is sent without an Authorization header
    Then the response status is 401
    And the error type is "invalid_access_token"

  @s2
  Scenario: Calling a protected endpoint without the required rule is rejected
    Given an account has a valid, unexpired access token "AT1"
    And that account holds no role granting "iam:manage"
    When a create-rule request is sent with Authorization bearer "AT1"
    Then the response status is 403
    And the response body contains "missing_rule": "iam:manage"

  @s3
  Scenario: Calling a protected endpoint with the required rule succeeds
    Given an account has a valid, unexpired access token "AT1"
    And that account holds an active role granting "iam:manage"
    When a create-rule request is sent with Authorization bearer "AT1"
    Then the response status is 202

  @s4
  Scenario: An expired grant of the required rule is treated as not held
    Given an account has a valid, unexpired access token "AT1"
    And that account's only role granting "iam:manage" has expired
    When a create-rule request is sent with Authorization bearer "AT1"
    Then the response status is 403
    And the response body contains "missing_rule": "iam:manage"

  @s5
  Scenario: Listing the rule catalog requires no access token
    When rules are listed without an Authorization header
    Then the response status is 200

  @s6
  Scenario: Listing the role catalog requires no access token
    When roles are listed without an Authorization header
    Then the response status is 200

  @s7
  Scenario: Assigning a role is also gated by the required rule
    Given an account exists with id "account-1"
    And a role exists with id "role-1" and name "account_admin"
    And the caller's account holds no role granting "iam:manage"
    And the caller has a valid, unexpired access token "AT1"
    When a role is assigned to "account-1" for role "role-1" with Authorization bearer "AT1"
    Then the response status is 403
    And the response body contains "missing_rule": "iam:manage"

  @s8
  Scenario: Unassigning a role is also gated by the required rule
    Given an account exists with id "account-1"
    And a role exists with id "role-1" and name "account_admin"
    And the caller's account holds no role granting "iam:manage"
    And the caller has a valid, unexpired access token "AT1"
    When role "role-1" is unassigned from "account-1" with Authorization bearer "AT1"
    Then the response status is 403
    And the response body contains "missing_rule": "iam:manage"

  @s9
  Scenario: Listing an account's assigned roles is also gated by the required rule
    Given an account exists with id "account-1"
    And the caller's account holds no role granting "iam:manage"
    And the caller has a valid, unexpired access token "AT1"
    When roles are listed for "account-1" with Authorization bearer "AT1"
    Then the response status is 403
    And the response body contains "missing_rule": "iam:manage"
