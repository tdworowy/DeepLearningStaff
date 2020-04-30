import json

from behave import given, when, then
import time
from front_end_tests.data_classes.layer import get_layer
from front_end_tests.pages.add_network import AddNetworkPage

from front_end_tests.data_classes.layer import MaxPooling2DLayer,DenseLayer,Conv2DLayer


def add_dense(add_network_page: AddNetworkPage, name: str, layer: DenseLayer):
    add_network_page. \
        choose_layer_type(layer.type). \
        set_name(name). \
        set_units(layer.units). \
        set_activation(layer.activation). \
        set_input_shape(layer.input_shape)

    add_network_page.click_add_layer_button()


def add_conv2d(add_network_page: AddNetworkPage, name: str, layer: Conv2DLayer):
    add_network_page. \
        choose_layer_type(layer.type). \
        set_name(name). \
        set_filters(layer.filters). \
        set_kernel_size(layer.kernel_size). \
        set_activation(layer.activation). \
        set_input_shape(layer.input_shape)

    add_network_page.click_add_layer_button()


def add_max_pooling2d(add_network_page: AddNetworkPage, name: str,layer: MaxPooling2DLayer):
    add_network_page. \
        choose_layer_type(layer.type). \
        set_name(name). \
        set_pool_size(layer.pool_size). \
        set_strides(layer.strides)

    add_network_page.click_add_layer_button()


add_functions = {"Dense": add_dense,
                 "Conv2D": add_conv2d,
                 "MaxPooling2D": add_max_pooling2d}


@given("Add network page is opened")
def open_main_page(context):
    context.add_network_page = AddNetworkPage(url=context.url,
                                              logger=context.scenario_logger,
                                              web_driver_wrapper=context.web_driver_wrapper)
    context.add_network_page.open_page()
    context.layers = []
    context.networks = []
    time.sleep(2)


@when("Add layer {network_json}")
def add_layer(context, network_json):
    values = json.loads(network_json)

    layer_type = values["layer"]["type"]

    layer = get_layer(layer_type)(**values["layer"])

    context.layers.append(layer)

    context.name = values["name"]
    add_functions[layer_type](add_network_page=context.add_network_page,
                              name=values["name"],
                              layer=layer)
    time.sleep(2)


@when("Post network")
def post_network(context):
    context.add_network_page.click_add_network_button()
    context.networks.append(context.name)
    time.sleep(2)


@then("Check layers")
def check_layers(context):
    context.add_network_page.assert_layer(expected_name=context.name,
                                          expected_layers=context.layers
                                          )


@then("Check if network exist")
def check_network(context):
    context.add_network_page.check_networks_lists(context.networks)


@then("Clear layers")
def check_layers(context):
    context.add_network_page.clear_layers()


@then("Delete network")
def delete_network(context):
    for network in context.networks:
        context.add_network_page.delete_network(network)
    time.sleep(2)
