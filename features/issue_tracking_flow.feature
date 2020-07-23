Feature: An example issue tracking flow that is set up with django-river

  . POTENTIAL PROBLEM AREAS:
  .   * The workflow creation with all the components like states, transitions, authorization rules may have unexpected problems
  .   * Authorized person may not be able to approve the transition
  .   * What is going on with one issue may be affecting another issue.
  .   * Recursive transitions may be working as expected

  Background: some requirement of this test
    # Groups
    Given a group with name "Developer"
    And a group with name "Team Leader"
    And a group with name "Tester"

    # Users
    Given a user with name developer_1 with group "Developer"
    And a user with name team_leader_1 with group "Team Leader"
    And a user with name tester_1 with group "Tester"

    # Workflow
    Given a workflow with an identifier "Issue Tracking Flow"

    # Transitions
    Given a transition "Open" -> "In Progress" in "Issue Tracking Flow"
    Given a transition "In Progress" -> "Resolved" in "Issue Tracking Flow"
    Given a transition "Resolved" -> "Closed" in "Issue Tracking Flow"
    Given a transition "Resolved" -> "Re-Opened" in "Issue Tracking Flow"
    Given a transition "Re-Opened" -> "In Progress" in "Issue Tracking Flow"

    # Authorization Rules
    Given an authorization rule for the transition "Open" -> "In Progress" with group "Developer" and priority 0

    Given an authorization rule for the transition "In Progress" -> "Resolved" with group "Developer" and priority 0

    Given an authorization rule for the transition "Resolved" -> "Closed" with group "Team Leader" and priority 0
    And an authorization rule for the transition "Resolved" -> "Closed" with group "Tester" and priority 1

    Given an authorization rule for the transition "Resolved" -> "Re-Opened" with groups "Team Leader or Tester" and priority 0

    Given an authorization rule for the transition "Re-Opened" -> "In Progress" with group "Developer" and priority 0

  Scenario: Should initialize the shipping
    Given a bug "Fix button look on the home page" identifier "the bug"
    When get current state of "the bug"
    Then return current state as "Open"

  Scenario: Should isolate one issue lifecycle from another one
    Given a bug "Fix button look on the home page" identifier "the bug"
    And a bug "Send an email after a user signs up" identifier "the story"
    When "the bug" is attempted to be approved by developer_1
    And get current state of "the story"
    Then return current state as "Open"

  # Open -> In Progress
  Scenario: Should start working on the bug when the developer approves it
    Given a bug "Fix button look on the home page" identifier "the bug"
    When "the bug" is attempted to be approved by developer_1
    And get current state of "the bug"
    Then return current state as "In Progress"
    
  # In Progress -> Resolved
  Scenario: Should resolve the bug when the developer approves it
    Given a bug "Fix button look on the home page" identifier "the bug"
    And "the bug" is jumped on state "In Progress"
    When "the bug" is attempted to be approved by developer_1
    And get current state of "the bug"
    Then return current state as "Resolved"

  # Resolved -> Closed
  Scenario: Should wait for the confirmation of that it has been closed before a tester approves it even though the team leader approves it
    Given a bug "Fix button look on the home page" identifier "the bug"
    And "the bug" is jumped on state "Resolved"
    When "the bug" is attempted to be closed by team_leader_1
    And get current state of "the bug"
    Then return current state as "Resolved"

  # Resolved -> Closed
  Scenario: Should confirm that it has been closed when the tester approves it after the team leader approves it.
    Given a bug "Fix button look on the home page" identifier "the bug"
    And "the bug" is jumped on state "Resolved"
    When "the bug" is attempted to be closed by team_leader_1
    And "the bug" is attempted to be closed by tester_1
    And get current state of "the bug"
    Then return current state as "Closed"

  # Resolved -> Re-Opened
  Scenario: Should re-open the bug when approved by a team leader.
    Given a bug "Fix button look on the home page" identifier "the bug"
    And "the bug" is jumped on state "Resolved"
    When "the bug" is attempted to be re-opened by team_leader_1
    And get current state of "the bug"
    Then return current state as "Re-Opened"

  # Resolved -> Re-Opened
  Scenario: Should re-open the bug when approved by a tester.
    Given a bug "Fix button look on the home page" identifier "the bug"
    And "the bug" is jumped on state "Resolved"
    When "the bug" is attempted to be re-opened by tester_1
    And get current state of "the bug"
    Then return current state as "Re-Opened"

  # Re-Opened -> In Progress
  Scenario: Should start working on the bug again when the developer approves it
    Given a bug "Fix button look on the home page" identifier "the bug"
    And "the bug" is jumped on state "Re-Opened"
    When "the bug" is attempted to be approved by developer_1
    And get current state of "the bug"
    Then return current state as "In Progress"