Feature: An example #159 Flow that is set up with django-river

  . POTENTIAL PROBLEM AREAS:
  .   * Short cyclic transitions are reported to have go in an infinite loop.

  Background: some requirement of this test
    # Groups
    Given a group with name "Authorized Group"

    # Users
    Given a user with name authorized_user with group "Authorized Group"

    # Workflow
    Given a workflow with an identifier "#159 Flow"

    # Transitions
    Given a transition "Draft" -> "Awaiting 1" in "#159 Flow"
    And a transition "Awaiting 1" -> "First Approval" in "#159 Flow"
    And a transition "First Approval" -> "Second Approval" in "#159 Flow"
    And a transition "First Approval" -> "Recreate 1" in "#159 Flow"
    And a transition "Recreate 1" -> "First Approval" in "#159 Flow"
    And a transition "Second Approval" -> "Awaiting 2" in "#159 Flow"
    And a transition "Second Approval" -> "Recreate 2" in "#159 Flow"
    And a transition "Recreate 2" -> "Second Approval" in "#159 Flow"
    And a transition "Second Approval" -> "Published" in "#159 Flow"

    # Authorization Rules
    Given an authorization rule for the transition "Draft" -> "Awaiting 1" with group "Authorized Group" and priority 0
    Given an authorization rule for the transition "Awaiting 1" -> "First Approval" with group "Authorized Group" and priority 0
    Given an authorization rule for the transition "First Approval" -> "Second Approval" with group "Authorized Group" and priority 0
    Given an authorization rule for the transition "First Approval" -> "Recreate 1" with group "Authorized Group" and priority 0
    Given an authorization rule for the transition "Recreate 1" -> "First Approval" with group "Authorized Group" and priority 0
    Given an authorization rule for the transition "Second Approval" -> "Awaiting 2" with group "Authorized Group" and priority 0
    Given an authorization rule for the transition "Second Approval" -> "Recreate 2" with group "Authorized Group" and priority 0
    Given an authorization rule for the transition "Recreate 2" -> "Second Approval" with group "Authorized Group" and priority 0
    Given an authorization rule for the transition "Second Approval" -> "Published" with group "Authorized Group" and priority 0

  Scenario: Should allow multiple cyclic transitions when one of them goes through
    Given a workflow object with identifier "object 1"
    And "object 1" is jumped on state "First Approval"
    When "object 1" is attempted to be approved for next state "Recreate 1" by authorized_user
    And "object 1" is attempted to be approved for next state "First Approval" by authorized_user
    And get current state of "object 1"
    Then return current state as "First Approval"
