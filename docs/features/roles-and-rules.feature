Feature: Roles and rules
  As a system managing authorization
  I want to define rules and compose them into roles
  So that later assignment and enforcement have a shared, reusable permission vocabulary

  @s1
  Scenario: Creating a rule succeeds
    When a create-rule request is sent with rule_id "rule-1" and name "account:create"
    Then the response status is 202
    And the response body contains "accepted": true
    And "account:create" appears when listing rules

  @s2
  Scenario: Creating a rule with a name that already exists is rejected
    Given a rule exists with name "account:create"
    When a create-rule request is sent with rule_id "rule-2" and name "account:create"
    Then the response status is 409
    And the error type is "conflict_error"

  @s3
  Scenario: Creating a rule with an empty name is rejected
    When a create-rule request is sent with rule_id "rule-1" and an empty name
    Then the response status is 422

  @s4
  Scenario: Creating a role referencing existing rules succeeds
    Given rules exist with names "account:create" and "account:read"
    When a create-role request is sent with role_id "role-1", name "account_admin" and those rule ids
    Then the response status is 202
    And the response body contains "accepted": true
    And listing roles shows "account_admin" composed of "account:create" and "account:read"

  @s5
  Scenario: Creating a role with a name that already exists is rejected
    Given a role exists with name "account_admin"
    And a rule exists with name "account:read"
    When a create-role request is sent with role_id "role-2", name "account_admin" and that rule's id
    Then the response status is 409
    And the error type is "conflict_error"

  @s6
  Scenario: Creating a role that references a rule that does not exist is rejected
    When a create-role request is sent with role_id "role-1", name "account_admin" and a rule id that does not exist
    Then the response status is 404
    And the error type is "not_found_error"
    And "account_admin" does not appear when listing roles

  @s7
  Scenario: Creating a role with no rule ids is rejected
    When a create-role request is sent with role_id "role-1", name "account_admin" and an empty rule id list
    Then the response status is 422

  @s8
  Scenario: Listing rules when none exist returns an empty list
    When rules are listed
    Then the response status is 200
    And the response body contains an empty "rules" list

  @s9
  Scenario: Listing roles when none exist returns an empty list
    When roles are listed
    Then the response status is 200
    And the response body contains an empty "roles" list
