Feature: Temporary role assignment
  As a system managing authorization
  I want to assign a role to an account for a bounded amount of time
  So that access lapses automatically without a separate removal step

  @s1
  Scenario: Assigning a role with a duration creates a temporary assignment
    Given an account exists with id "account-1"
    And a role exists with id "role-1" and name "account_admin"
    When a role is assigned to "account-1" for role "role-1" with expires_in_minutes 30
    Then the response status is 202
    And listing roles for "account-1" shows "account_admin" with a non-null expiry

  @s2
  Scenario: A temporary assignment is excluded from listing once it has expired
    Given an account exists with id "account-1"
    And a role exists with id "role-1" and name "account_admin"
    And role "role-1" was assigned to "account-1" with an expiry in the past
    When roles are listed for "account-1"
    Then the response status is 200
    And the response body does not contain "account_admin"

  @s3
  Scenario: Assigning a role with an expiry of zero minutes is rejected
    Given an account exists with id "account-1"
    And a role exists with id "role-1" and name "account_admin"
    When a role is assigned to "account-1" for role "role-1" with expires_in_minutes 0
    Then the response status is 422

  @s4
  Scenario: Assigning a role with a negative expiry is rejected
    Given an account exists with id "account-1"
    And a role exists with id "role-1" and name "account_admin"
    When a role is assigned to "account-1" for role "role-1" with expires_in_minutes -5
    Then the response status is 422

  @s5
  Scenario: Re-assigning the same role temporarily resets the expiry
    Given an account exists with id "account-1"
    And a role exists with id "role-1" and name "account_admin"
    And role "role-1" is assigned to "account-1" with expires_in_minutes 5
    When a role is assigned to "account-1" for role "role-1" with expires_in_minutes 60
    Then listing roles for "account-1" shows "account_admin" expiring around 60 minutes from now, not 5

  @s6
  Scenario: Assigning a role permanently over an existing temporary assignment converts it to permanent
    Given an account exists with id "account-1"
    And a role exists with id "role-1" and name "account_admin"
    And role "role-1" is assigned to "account-1" with expires_in_minutes 5
    When a role is assigned to "account-1" for role "role-1" with no expires_in_minutes
    Then listing roles for "account-1" shows "account_admin" with a null expiry

  @s7
  Scenario: Assigning a role temporarily over an existing permanent assignment converts it to temporary
    Given an account exists with id "account-1"
    And a role exists with id "role-1" and name "account_admin"
    And role "role-1" is assigned to "account-1" permanently
    When a role is assigned to "account-1" for role "role-1" with expires_in_minutes 15
    Then listing roles for "account-1" shows "account_admin" with a non-null expiry

  @s8
  Scenario: Assigning a role after a previous temporary assignment has expired behaves as a fresh assignment
    Given an account exists with id "account-1"
    And a role exists with id "role-1" and name "account_admin"
    And role "role-1" was assigned to "account-1" with an expiry in the past
    When a role is assigned to "account-1" for role "role-1" with no expires_in_minutes
    Then the response status is 202
    And listing roles for "account-1" shows "account_admin" with a null expiry

  @s9
  Scenario: Unassigning an already-expired temporary assignment still succeeds
    Given an account exists with id "account-1"
    And a role exists with id "role-1" and name "account_admin"
    And role "role-1" was assigned to "account-1" with an expiry in the past
    When role "role-1" is unassigned from "account-1"
    Then the response status is 202
    And the response body contains "accepted": true
