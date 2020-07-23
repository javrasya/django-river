Feature: An example shipping flow that is set up with django-river

  . POTENTIAL PROBLEM AREAS:
  .   * The workflow creation with all the components like states, transitions, authorization rules may have unexpected problems
  .   * Authorized person may not be able to approve the transition
  .   * What is going on with one shipping may be affecting another shipping.
  .   * Recursive transitions may be working as expected

  Background: some requirement of this test
    # Groups
    Given a group with name "Warehouse Attendant"
    And a group with name "Delivery Person"
    And a group with name "Courier Company Attendant"
    And a group with name "Finance Person"

    # Users
    Given a user with name warehouse_attendant_1 with group "Warehouse Attendant"
    And a user with name delivery_person_1 with group "Delivery Person"
    And a user with name courier_company_attendant_1 with group "Courier Company Attendant"
    And a user with name finance_person_1 with group "Finance Person"

    # Workflow
    Given a workflow with an identifier "Shipping Flow"

    # Transitions
    Given a transition "Initialized" -> "Shipped" in "Shipping Flow"
    And a transition "Shipped" -> "Arrived" in "Shipping Flow"
    And a transition "Arrived" -> "Closed" in "Shipping Flow"
    And a transition "Arrived" -> "Return Initialized" in "Shipping Flow"
    And a transition "Return Initialized" -> "Returned" in "Shipping Flow"
    And a transition "Returned" -> "Re-Initialized" in "Shipping Flow"
    And a transition "Returned" -> "Refunded" in "Shipping Flow"
    And a transition "Refunded" -> "Closed" in "Shipping Flow"
    And a transition "Re-Initialized" -> "Shipped" in "Shipping Flow"

    # Authorization Rules
    Given an authorization rule for the transition "Initialized" -> "Shipped" with group "Warehouse Attendant" and priority 0
    And an authorization rule for the transition "Initialized" -> "Shipped" with group "Courier Company Attendant" and priority 1

    Given an authorization rule for the transition "Shipped" -> "Arrived" with group "Delivery Person" and priority 0
    And an authorization rule for the transition "Shipped" -> "Arrived" with group "Courier Company Attendant" and priority 1

    Given an authorization rule for the transition "Arrived" -> "Closed" with group "Finance Person" and priority 0

    Given an authorization rule for the transition "Arrived" -> "Return Initialized" with group "Courier Company Attendant" and priority 0

    Given an authorization rule for the transition "Return Initialized" -> "Returned" with group "Warehouse Attendant" and priority 0

    Given an authorization rule for the transition "Returned" -> "Re-Initialized" with group "Warehouse Attendant" and priority 0

    Given an authorization rule for the transition "Re-Initialized" -> "Shipped" with group "Warehouse Attendant" and priority 0
    And an authorization rule for the transition "Re-Initialized" -> "Shipped" with group "Courier Company Attendant" and priority 1

    Given an authorization rule for the transition "Returned" -> "Refunded" with group "Finance Person" and priority 0

    Given an authorization rule for the transition "Refunded" -> "Closed" with group "Finance Person" and priority 0

  Scenario: Should initialize the shipping
    Given a workflow object with identifier "MacBook Pro 15"
    When get current state of "MacBook Pro 15"
    Then return current state as "Initialized"

  Scenario: Should isolate one shipping lifecycle from another one
    Given a workflow object with identifier "MacBook Pro 15"
    And a workflow object with identifier "iPhone 11"
    When "MacBook Pro 15" is attempted to be approved by warehouse_attendant_1
    And "MacBook Pro 15" is attempted to be approved by courier_company_attendant_1
    And get current state of "iPhone 11"
    Then return current state as "Initialized"

  # Initialized -> Shipped
  Scenario: Should wait for the confirmation of that it has been shipped before a courier company attendant approves it even though the warehouse attendant approves it
    Given a workflow object with identifier "MacBook Pro 15"
    When "MacBook Pro 15" is attempted to be approved by warehouse_attendant_1
    And get current state of "MacBook Pro 15"
    Then return current state as "Initialized"

  # Initialized -> Shipped
  Scenario: Should confirm that it has been shipped when the courier company attendant approves it after the warehouse attendant approves it.
    Given a workflow object with identifier "MacBook Pro 15"
    When "MacBook Pro 15" is attempted to be approved by warehouse_attendant_1
    And "MacBook Pro 15" is attempted to be approved by courier_company_attendant_1
    And get current state of "MacBook Pro 15"
    Then return current state as "Shipped"

  # Shipped -> Arrived
  Scenario: Should wait for the confirmation of the shipping before a courier company attendant approves it even though the delivery person approves it
    Given a workflow object with identifier "MacBook Pro 15"
    And "MacBook Pro 15" is jumped on state "Shipped"
    When "MacBook Pro 15" is attempted to be approved by delivery_person_1
    And get current state of "MacBook Pro 15"
    Then return current state as "Shipped"

  # Shipped -> Arrived
  Scenario: Should confirm the arrival of the sipping when the courier company attendant approves it after the delivery person approves it.
    Given a workflow object with identifier "MacBook Pro 15"
    And "MacBook Pro 15" is jumped on state "Shipped"
    When "MacBook Pro 15" is attempted to be approved by delivery_person_1
    And "MacBook Pro 15" is attempted to be approved by courier_company_attendant_1
    And get current state of "MacBook Pro 15"
    Then return current state as "Arrived"

  # Arrived -> Closed
  Scenario: Should close the shipping when everything is good and the finance person approves it.
    Given a workflow object with identifier "MacBook Pro 15"
    And "MacBook Pro 15" is jumped on state "Arrived"
    When "MacBook Pro 15" is attempted to be approved by finance_person_1
    And get current state of "MacBook Pro 15"
    Then return current state as "Closed"

  # Arrived -> Return Initialized
  Scenario: Should initialize th return of the sipping after the courier company attendant approves it.
    Given a workflow object with identifier "MacBook Pro 15"
    And "MacBook Pro 15" is jumped on state "Arrived"
    When "MacBook Pro 15" is attempted to be approved by courier_company_attendant_1
    And get current state of "MacBook Pro 15"
    Then return current state as "Return Initialized"

  # Return Initialized -> Returned
  Scenario: Should confirm the return after the warehouse attendant approves it
    Given a workflow object with identifier "MacBook Pro 15"
    And "MacBook Pro 15" is jumped on state "Return Initialized"
    When "MacBook Pro 15" is attempted to be approved by warehouse_attendant_1
    And get current state of "MacBook Pro 15"
    Then return current state as "Returned"

  # Returned -> Re-Initialized
  Scenario: Should re-initialize it when the warehouse attendant approves it
    Given a workflow object with identifier "MacBook Pro 15"
    And "MacBook Pro 15" is jumped on state "Returned"
    When "MacBook Pro 15" is attempted to be approved by warehouse_attendant_1
    And get current state of "MacBook Pro 15"
    Then return current state as "Re-Initialized"

  # Re-Initialized -> Shipped
  Scenario: Should wait for the confirmation of that it has been re-shipped before a courier company attendant approves it even though the warehouse attendant approves it
    Given a workflow object with identifier "MacBook Pro 15"
    And "MacBook Pro 15" is jumped on state "Re-Initialized"
    When "MacBook Pro 15" is attempted to be approved by warehouse_attendant_1
    And get current state of "MacBook Pro 15"
    Then return current state as "Re-Initialized"

  # Re-Initialized -> Shipped
  Scenario: Should confirm that it has been shipped when the courier company attendant approves it after the warehouse attendant approves it.
    Given a workflow object with identifier "MacBook Pro 15"
    And "MacBook Pro 15" is jumped on state "Re-Initialized"
    When "MacBook Pro 15" is attempted to be approved by warehouse_attendant_1
    And "MacBook Pro 15" is attempted to be approved by courier_company_attendant_1
    And get current state of "MacBook Pro 15"
    Then return current state as "Shipped"

  # Returned -> Refunded
  Scenario: Should refund the returned shipment with an approval of a finance person
    Given a workflow object with identifier "MacBook Pro 15"
    And "MacBook Pro 15" is jumped on state "Returned"
    When "MacBook Pro 15" is attempted to be approved by finance_person_1
    And get current state of "MacBook Pro 15"
    Then return current state as "Refunded"

  # Refunded -> Closed
  Scenario: Should close the refunded shipment with an approval of a finance person
    Given a workflow object with identifier "MacBook Pro 15"
    And "MacBook Pro 15" is jumped on state "Refunded"
    When "MacBook Pro 15" is attempted to be approved by finance_person_1
    And get current state of "MacBook Pro 15"
    Then return current state as "Closed"
