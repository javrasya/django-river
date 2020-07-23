Feature: An example #162 Flow that is set up with django-river (https://github.com/javrasya/django-river/issues/162)

  Background: some requirement of this test
    # Groups
    Given a group with name "Authorized Group"

    # Users
    Given a user with name authorized_user with group "Authorized Group"

    # Workflow
    Given a workflow with an identifier "#162 Flow"

    # Transitions
    Given a transition "Draft" -> "Issued" in "#162 Flow"
    And a transition "Issued" -> "Part Received" in "#162 Flow"
    And a transition "Part Received" -> "Received" in "#162 Flow"
    And a transition "Issued" -> "Received" in "#162 Flow"
    And a transition "Received" -> "Issued" in "#162 Flow"
    And a transition "Received" -> "Closed" in "#162 Flow"

    # Authorization Rules
    Given an authorization rule for the transition "Draft" -> "Issued" with group "Authorized Group" and priority 0
    Given an authorization rule for the transition "Issued" -> "Part Received" with group "Authorized Group" and priority 0
    Given an authorization rule for the transition "Part Received" -> "Received" with group "Authorized Group" and priority 0
    Given an authorization rule for the transition "Issued" -> "Received" with group "Authorized Group" and priority 0
    Given an authorization rule for the transition "Received" -> "Issued" with group "Authorized Group" and priority 0
    Given an authorization rule for the transition "Received" -> "Closed" with group "Authorized Group" and priority 0

  Scenario: Should allow the state to transit all the way to Closed
    Given a workflow object with identifier "object 1"
    When "object 1" is attempted to be approved for next state "Issued" by authorized_user
    And "object 1" is attempted to be approved for next state "Part Received" by authorized_user
    And "object 1" is attempted to be approved for next state "Received" by authorized_user
    And "object 1" is attempted to be approved for next state "Closed" by authorized_user
    And get current state of "object 1"
    Then return current state as "Closed"
