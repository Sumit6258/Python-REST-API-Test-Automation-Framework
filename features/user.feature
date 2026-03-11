Feature: Users API
  As an API consumer
  I want to interact with the users endpoint
  So that I can manage user resources

  Background:
    Given the API base URL is configured

  # ------------------------------------------------------------------ #
  # GET single user                                                      #
  # ------------------------------------------------------------------ #

  @smoke @users
  Scenario: Retrieve an existing user by ID
    When I send a GET request to "/users/2"
    Then the response status code should be 200
    And the response body should contain a "data" field
    And the user "id" should be 2

  @users
  Scenario: Single user response conforms to schema
    When I send a GET request to "/users/2"
    Then the response should conform to the single user schema

  @errors @users
  Scenario: Retrieve a non-existent user returns 404
    When I send a GET request to "/users/9999"
    Then the response status code should be 404
    And the response body should be an empty JSON object

  # ------------------------------------------------------------------ #
  # GET user list                                                        #
  # ------------------------------------------------------------------ #

  @smoke @users
  Scenario: Retrieve list of users on page 1
    When I send a GET request to "/users" with query params "page=1"
    Then the response status code should be 200
    And the response body should contain a "data" field
    And the "data" field should be a non-empty list

  @users
  Scenario: User list response conforms to schema
    When I send a GET request to "/users" with query params "page=1"
    Then the response should conform to the user list schema

  @pagination @users
  Scenario Outline: Retrieve user list for different pages
    When I send a GET request to "/users" with query params "page=<page>"
    Then the response status code should be 200
    And the "page" field in the response should equal <page>

    Examples:
      | page |
      | 1    |
      | 2    |

  # ------------------------------------------------------------------ #
  # POST create user                                                     #
  # ------------------------------------------------------------------ #

  @regression @users
  Scenario: Create a new user successfully
    Given I have a valid user payload with name "Alice" and job "Engineer"
    When I send a POST request to "/users"
    Then the response status code should be 201
    And the response body should contain an "id" field
    And the response "name" should equal "Alice"
    And the response "job" should equal "Engineer"

  @regression @users
  Scenario: Created user response conforms to schema
    Given I have a valid user payload with name "Bob" and job "Designer"
    When I send a POST request to "/users"
    Then the response should conform to the create user schema

  # ------------------------------------------------------------------ #
  # PUT update user                                                      #
  # ------------------------------------------------------------------ #

  @regression @users
  Scenario: Update an existing user
    Given I have an update payload with name "Updated Alice" and job "Senior Engineer"
    When I send a PUT request to "/users/2"
    Then the response status code should be 200
    And the response body should contain an "updatedAt" field

  # ------------------------------------------------------------------ #
  # DELETE user                                                          #
  # ------------------------------------------------------------------ #

  @regression @users
  Scenario: Delete an existing user
    When I send a DELETE request to "/users/2"
    Then the response status code should be 204
