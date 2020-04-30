Feature: Train Network
  Scenario Outline: Train network
    Given Add network page is opened
    When Add layer <NetworkJson1>
    And Add layer <NetworkJson2>
    And Add layer <NetworkJson3>
    And Post network
    And Compile network <CompileJson>
    And Train network <TrainJson>

    Then Check if network exist
    And Check if network is compiled
    And Check if network is trained
    And Delete network

    Examples: Input
    |NetworkJson1|NetworkJson2|NetworkJson3|CompileJson|TrainJson|
    |{"name":"Test_network_train", "layer":{"type":"Dense", "units":16, "activation":"relu","input_shape":"10000"}}|{"name":"Test_network_train", "layer":{"type":"Dense", "units":16, "activation":"relu","input_shape":"10000"}}|{"name":"Test_network_train", "layer":{"type":"Dense", "units":1, "activation":"sigmoid","input_shape":"10000"}}|{"name":"Test_network_train", "data":{"optimizer":"rmsprop", "loss":"binary_crossentropy", "metrics":"acc"}}|{"name":"Test_network_train", "data":{"dat_set":"imdb", "epochs":10, "batch_size":512,"input_shape":10000,"test_sample_size":10000}}|




