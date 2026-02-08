Feature: Account and User Signup
    As a new user
    I want to create an account and a user profile
    So that I can access the codenet's features

    Scenario: Successful account and user signup
        Given I have filled in the signup form with valid information
        When I submit the signup form
        Then I should have an account and a user profile created

    Scenario: Signup with an already registered username
        Given I have filled in the signup form with a username that is already registered
        When I submit the signup form
        Then I should see an error message indicating the username is already in use

    Scenario: Signup with an already registered email
        Given I have filled in the signup form with an email that is already registered
        When I submit the signup form
        Then I should see an error message indicating the email is already in use