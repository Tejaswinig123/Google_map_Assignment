Feature: Searching for nearest restaurants and getting details
  Scenario: Search for nearest restaurants and get details
    Given User open Google map Application
    When User search for nearest Restaurants
    Then User should able to open and get the details of each Restaurant
