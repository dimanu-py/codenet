Feature: Account Authentication
    As a signed up user
    I want to be able to authenticate myself
    So that I can access protected resources

    Scenario: Successful Authentication
        Given I have a registered account with valid email and password
        When I attempt to authenticate with valid credentials
        Then I should receive an authentication token

    Scenario: Failed Authentication with Incorrect Password
        Given I have a registered account with valid email and password
        When I attempt to authenticate with wrong credentials
        Then I should receive an authentication error

    Scenario: Failed Authentication with Unregistered Email
        Given I haven't registered an account
        When I attempt to authenticate with non existing account credentials
        Then I should receive an authentication error

