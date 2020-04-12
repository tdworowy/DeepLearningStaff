Feature: Create Network
  Scenario: Add network witch one layer
    Given Add network page is opened
    When Add layer Test_network Dense 16 relu 1000
    Then Check layers
    And Clear layers

  Scenario: Add network witch three layers
    Given Add network page is opened
    When Add layer Test_network Dense 16 relu 1000
    And Add layer Test_network Dense 15 relu 1000
    And Add layer Test_network Dense 1 sigmoid 1000
    Then Check layers
    And Clear layers