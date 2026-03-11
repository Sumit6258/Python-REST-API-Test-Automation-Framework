Feature: Login API
  As a registered user
  I want to authenticate via the login endpoint
  So that I can receive a valid access token

  Background:
    Given the API base URL is configured

  @smoke @auth
  Scenario: Successful login with valid credentials
    Given I have valid login credentials
    When I send a POST request to "/login"
    Then the response status code should be 200
    And the response body should contain a "token" field
    And the token should be a non-empty string

  @auth
  Scenario: Login response conforms to schema
    Given I have valid login credentials
    When I send a POST request to "/login"
    Then the response should conform to the login success schema

  @errors @auth
  Scenario: Login fails when password is missing
    Given I have login credentials without a password
    When I send a POST request to "/login"
    Then the response status code should be 400
    And the response body should contain an "error" field

  @errors @auth
  Scenario: Login fails when email is missing
    Given I have login credentials without an email
    When I send a POST request to "/login"
    Then the response status code should be 400
    And the response body should contain an "error" field

  @errors @auth
  Scenario: Login fails with empty payload
    Given I have an empty request payload
    When I send a POST request to "/login"
    Then the response status code should be 400

  @auth
  Scenario: Successful registration with valid credentials
    Given I have valid registration credentials
    When I send a POST request to "/register"
    Then the response status code should be 200
    And the response body should contain an "id" field
    And the response body should contain a "token" field

  @errors @auth
  Scenario: Registration fails when password is missing
    Given I have registration credentials without a password
    When I send a POST request to "/register"
    Then the response status code should be 400
    And the response body should contain an "error" field
