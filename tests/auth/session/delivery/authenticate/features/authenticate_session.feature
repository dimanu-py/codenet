Feature: Authenticate Session
  As a registered user
  I want to authenticate with my credentials
  So that I can access my account

  Background:
    Given I have a registered account with valid email and password

  Scenario: Authenticate with valid credentials
    When I attempt to authenticate with valid credentials
    Then I should receive an authentication token

  Scenario: Authenticate with wrong password
    When I attempt to authenticate with wrong credentials
    Then I should receive an authentication error

  Scenario: Authenticate with non existing account
    Given I haven't registered an account
    When I attempt to authenticate with non existing account credentials
    Then I should receive an authentication error
