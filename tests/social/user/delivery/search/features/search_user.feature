Feature: Search Users
    As a user of the social platform
    I want to search for other users by their username or display name
    So that I can find and connect with them easily

    Scenario: Search for a user by username
        Given there are users with usernames ["alice", "bob", "big_bob"]
        When I search for users with username "bob"
        Then I should see the users with username "bob"