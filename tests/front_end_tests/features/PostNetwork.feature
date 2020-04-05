Feature: Post Network
  Scenario: Post network
    Given Add network page is opened
    When Add layer Test_network 16 relu 1000
    And Post network
    Then Check if network exist
    And Delete network

  Scenario: Post 3 networks
    Given Add network page is opened

    When Add layer Test_network1 16 relu 1000
    And Post network
    And Add layer Test_network2 16 relu 1000
    And Post network
    And Add layer Test_network3 16 relu 1000
    And Post network

    Then Check if network exist
    And Delete network