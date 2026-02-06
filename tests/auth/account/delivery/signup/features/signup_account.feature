Feature: Account and User Signup
    As a new user
    I want to create an account and a user profile
    So that I can access the codenet's features

    Scenario: Successful account and user signup
        Given I have filled in the signup form with valid information
        When I submit the signup form
        Then I should have an account and a user profile created