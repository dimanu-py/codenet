Feature: User Signup
    As a new user
    I want to sign up and create an account
    So that I can access codenet platform

    Scenario: Successful user signup
        Given I have filled a signup form with valid details
        When I submit the signup form
        Then I should be signed up successfully