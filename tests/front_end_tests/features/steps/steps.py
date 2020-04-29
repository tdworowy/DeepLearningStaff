import json

from behave import given, when, then
import time
from front_end_tests.data_classes.layer import layer
from front_end_tests.pages.add_network import AddNetworkPage


def add_dense(add_network_page: AddNetworkPage, name: str, type: str, units: int, activation: str, input_shape: int):
    add_network_page. \
        choose_layer_type(type). \
        set_name(name). \
        set_units(units). \
        set_activation(activation). \
        set_input_shape(input_shape). \
        click_add_layer_button()


def add_conv2d(add_network_page: AddNetworkPage, name: str, type: str, filters: str, kernel_size: str, activation: str,
               input_shape: int):
    add_network_page. \
        choose_layer_type(type). \
        set_name(name). \
        set_filters(filters). \
        set_kernel_size(kernel_size). \
        set_activation(activation). \
        set_input_shape(input_shape). \
        click_add_layer_button()


def add_max_pooling2d(add_network_page: AddNetworkPage, name: str, type: str, pool_size: str, strides: str):
    add_network_page. \
        choose_layer_type(type). \
        set_name(name). \
        set_pool_size(pool_size). \
        set_strides(strides). \
        click_add_layer_button()


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
    context.layers.append(
        layer(layer_type)(**values["layer"])
    )

    context.name = values["name"]
    add_functions[layer_type](add_network_page=context.add_network_page,
                              name=values["name"],
                              **values["layer"])
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
