Feature: User Removal
    As an existing user
    I want to be able to remove my account
    So that I can delete my personal data from the platform

    Scenario: Not existing user attempts to remove account
        When I attempt to remove the account for non existing user
        Then I should receive an error message indicating the user does not exist

    Scenario: Existing user successfully removes account
        Given I am an existing user
        When I request to remove my account
        Then my account should be successfully removed

    Scenario: Sending user id with invalid format
        Given I am an existing user
        When I attempt to remove the account with an invalid user id format
        Then I should receive an error message indicating the user id format is invalid