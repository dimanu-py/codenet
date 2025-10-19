Feature: User Removal
    As an existing user
    I want to be able to remove my account
    So that I can delete my personal data from the platform

    Scenario: Not existing user attempts to remove account
        When I attempt to remove the account for non existing user
        Then I should receive an error message indicating the user does not exist
