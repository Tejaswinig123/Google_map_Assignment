Feature: Search for nearest Restauranbt in Google Maps
  Scenario: Get Details of the Nearest Restaurant
    Given The Google Map Application is open
    When I search for nearest Restaurant
    Then I able to select the first five Restaurants in the list
    Then I see the name,Location,Contact Number,Rating of the Restaurant
    Then I see the lattitute and longuitude of the Restaurant