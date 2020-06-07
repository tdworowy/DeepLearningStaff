Feature: Create Network
  Scenario Outline: Add network witch one layer
    Given Add network page is opened
    When Add layer <NetworkJson>
    Then Check layers
    And Clear layers

  Examples: Input
    |NetworkJson|
    |{"name":"Test_network", "layer":{"type":"Dense", "units":16, "activation":"relu","input_shape":"1000"}}|

  Scenario Outline: Add network witch three layers
    Given Add network page is opened
    When Add layer <NetworkJson1>
    And Add layer <NetworkJson2>
    And Add layer <NetworkJson3>
    Then Check layers
    And Clear layers

    Examples: Input
    |NetworkJson1|NetworkJson2|NetworkJson3|
    |{"name":"Test_network", "layer":{"type":"Dense", "units":16, "activation":"relu","input_shape":"1000"}}|{"name":"Test_network", "layer":{"type":"Dense", "units":15, "activation":"relu","input_shape":"1000"}}|{"name":"Test_network", "layer":{"type":"Dense", "units":1, "activation":"sigmoid","input_shape":"1000"}}|
