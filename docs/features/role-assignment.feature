Feature: Role assignment
  As a system managing authorization
  I want to assign roles to accounts, unassign them, and list an account's current roles
  So that access can be granted and revoked permanently

  @s1
  Scenario: Assigning an existing role to an existing account succeeds
    Given an account exists with id "account-1"
    And a role exists with id "role-1" and name "account_admin"
    When a role is assigned to "account-1" for role "role-1"
    Then the response status is 202
    And the response body contains "accepted": true
    And listing roles for "account-1" includes "account_admin"

  @s2
  Scenario: Assigning a role that does not exist is rejected
    Given an account exists with id "account-1"
    When a role is assigned to "account-1" for a role id that does not exist
    Then the response status is 404
    And the error type is "not_found_error"

  @s3
  Scenario: Assigning a role to an account that does not exist is rejected
    Given a role exists with id "role-1" and name "account_admin"
    When a role is assigned to an account id that does not exist for role "role-1"
    Then the response status is 404
    And the error type is "not_found_error"

  @s4
  Scenario: Assigning an already-assigned role again is idempotent
    Given an account exists with id "account-1"
    And a role exists with id "role-1" and name "account_admin"
    And role "role-1" is already assigned to "account-1"
    When a role is assigned to "account-1" for role "role-1"
    Then the response status is 202
    And listing roles for "account-1" includes "account_admin" exactly once

  @s5
  Scenario: Listing an account's roles reflects an assignment
    Given an account exists with id "account-1"
    And a role exists with id "role-1" and name "account_admin"
    And role "role-1" is already assigned to "account-1"
    When roles are listed for "account-1"
    Then the response status is 200
    And the response body contains "account_admin"

  @s6
  Scenario: Unassigning a role removes it from the account's assigned roles
    Given an account exists with id "account-1"
    And a role exists with id "role-1" and name "account_admin"
    And role "role-1" is already assigned to "account-1"
    When role "role-1" is unassigned from "account-1"
    Then the response status is 202
    And listing roles for "account-1" does not include "account_admin"

  @s7
  Scenario: Unassigning a role that isn't currently assigned still succeeds
    Given an account exists with id "account-1"
    And a role exists with id "role-1" and name "account_admin"
    When role "role-1" is unassigned from "account-1"
    Then the response status is 202
    And the response body contains "accepted": true

  @s8
  Scenario: Listing roles for an account with no assignments returns an empty list
    Given an account exists with id "account-1"
    When roles are listed for "account-1"
    Then the response status is 200
    And the response body contains an empty "roles" list
