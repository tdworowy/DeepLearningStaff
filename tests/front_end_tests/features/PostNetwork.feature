Feature: Post Network
  Scenario Outline: Post network
    Given Add network page is opened
    When Add layer <NetworkJson>
    And Post network
    Then Check if network exist
    And Delete network

    Examples: Input
    |NetworkJson|
    |{"name":"Test_network", "layer":{"type":"Dense", "units":16, "activation":"relu","input_shape":"1000"}}|

  Scenario Outline: Post 3 networks
    Given Add network page is opened

    When Add layer <NetworkJson1>
    And Post network
    And Add layer <NetworkJson2>
    And Post network
    And Add layer <NetworkJson3>
    And Post network

    Then Check if network exist
    And Delete network

    Examples: Input
    |NetworkJson1|NetworkJson2|NetworkJson3|
    |{"name":"Test_network1", "layer":{"type":"Dense", "units":16, "activation":"relu","input_shape":"1000"}}|{"name":"Test_network2", "layer":{"type":"Dense", "units":16, "activation":"relu","input_shape":"1000"}}|{"name":"Test_network3", "layer":{"type":"Dense", "units":16, "activation":"relu","input_shape":"1000"}}|