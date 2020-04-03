from behave import given, when, then

from front_end_tests.data_classes.layer import Layer
from front_end_tests.pages.add_network import AddNetworkPage


@given("Add network page is opened")
def open_main_page(context):
    context.add_network_page = AddNetworkPage(url=context.url,
                                              logger=context.scenario_logger,
                                              web_driver_wrapper=context.web_driver_wrapper)
    context.add_network_page.open_page()
    context.layers = []


@when("Add layer {name} {units} {activation} {input_shape}")
def add_layer(context, name, units, activation, input_shape):
    context.layers.append(
        Layer(int(units), activation, input_shape)
    )
    context.name = name
    context.add_network_page. \
        set_name(name). \
        set_units(units). \
        set_activation(activation). \
        set_input_shape(input_shape). \
        click_add_layer_button()


@then("Check layers")
def check_layers(context):
    context.add_network_page.assert_layer(expected_name=context.name,
                                          expected_layers=context.layers
                                          )


@then("Clear layers")
def check_layers(context):
    context.add_network_page.clear_layers()
