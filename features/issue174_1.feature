Feature: An example #174 Flow that is set up with django-river (https://github.com/javrasya/django-river/issues/174)

  Background: some requirement of this test
    # Groups
    Given a group with name "Authorized Group"

    # Users
    Given a user with name authorized_user with group "Authorized Group"

    # Workflow
    Given a workflow with an identifier "#174 Flow"

    # Transitions
    Given a transition "A" -> "B" in "#174 Flow"
    And a transition "B" -> "C" in "#174 Flow"
    And a transition "C" -> "B" in "#174 Flow"

    # Authorization Rules
    Given an authorization rule for the transition "A" -> "B" with group "Authorized Group" and priority 0
    Given an authorization rule for the transition "B" -> "C" with group "Authorized Group" and priority 0
    Given an authorization rule for the transition "C" -> "B" with group "Authorized Group" and priority 0

  Scenario: Should allow the workflow
    Given a workflow object with identifier "object 1"
    When "object 1" is attempted to be approved for next state "B" by authorized_user
    And "object 1" is attempted to be approved for next state "C" by authorized_user
    And "object 1" is attempted to be approved for next state "B" by authorized_user
    And get current state of "object 1"
    Then return current state as "B"
