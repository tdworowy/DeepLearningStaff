import json

from behave import given, when, then
import time

from ...data_classes.layer import get_layer
from ...pages.add_network import AddNetworkPage
from ...data_classes.layer import MaxPooling2DLayer, DenseLayer, Conv2DLayer
from ...pages.compile_network_page import CompileNetworkPage
from ...pages.train_network_page import TrainNetworkPage


def add_dense(add_network_page: AddNetworkPage, name: str, layer: DenseLayer):
    add_network_page.choose_layer_type(layer.type).set_name(name).set_units(
        layer.units
    ).set_activation(layer.activation).set_input_shape(layer.input_shape)

    add_network_page.click_add_layer_button()


def add_conv2d(add_network_page: AddNetworkPage, name: str, layer: Conv2DLayer):
    add_network_page.choose_layer_type(layer.type).set_name(name).set_filters(
        layer.filters
    ).set_kernel_size(layer.kernel_size).set_activation(
        layer.activation
    ).set_input_shape(
        layer.input_shape
    )

    add_network_page.click_add_layer_button()


def add_max_pooling2d(
    add_network_page: AddNetworkPage, name: str, layer: MaxPooling2DLayer
):
    add_network_page.choose_layer_type(layer.type).set_name(name).set_pool_size(
        layer.pool_size
    ).set_strides(layer.strides)

    add_network_page.click_add_layer_button()


def compile_network(compile_network_page: CompileNetworkPage, compile_data: dict):
    compile_network_page.set_optimizer(compile_data["optimizer"]).set_loss(
        compile_data["loss"]
    ).set_metrics(compile_data["metrics"]).click_compile_network_button()


def train_network(train_network_page: TrainNetworkPage, train_data: dict):
    train_network_page.set_data_set(train_data["dat_set"]).set_epochs(
        train_data["epochs"]
    ).set_batch_size(train_data["batch_size"]).set_input_shape(
        train_data["input_shape"]
    ).set_test_sample_size(
        train_data["test_sample_size"]
    ).click_train_network_button()


add_layer_functions = {
    "Dense": add_dense,
    "Conv2D": add_conv2d,
    "MaxPooling2D": add_max_pooling2d,
}


@given("Add network page is opened")
def open_main_page(context):
    context.add_network_page = AddNetworkPage(
        url=context.url,
        logger=context.scenario_logger,
        web_driver_wrapper=context.web_driver_wrapper,
    )
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
    add_layer_functions[layer_type](
        add_network_page=context.add_network_page, name=values["name"], layer=layer
    )
    time.sleep(5)


@when("Post network")
def post_network(context):
    context.add_network_page.click_add_network_button()
    context.networks.append(context.name)
    time.sleep(5)


@when("Compile network {network_json}")
def compile_network_step(context, network_json):
    values = json.loads(network_json)

    name = values["name"]
    context.compile_network_page = context.add_network_page.click_network_details(
        name=name, next_page_type="compile"
    )
    compile_network(context.compile_network_page, values["data"])
    time.sleep(2)


@when("Train network {network_json}")
def train_network_step(context, network_json):
    values = json.loads(network_json)

    name = values["name"]
    context.train_network_page = context.add_network_page.click_network_details(
        name=name, next_page_type="train"
    )
    train_network(context.train_network_page, values["data"])
    time.sleep(2)


@then("Check layers")
def check_layers(context):
    context.add_network_page.assert_layer(
        expected_name=context.name, expected_layers=context.layers
    )


@then("Check if network is compiled")
def check_if_network_is_compiled(context):
    context.compile_network_page.check_if_network_is_compiled(context.networks)


@then("Check if network is trained")
def check_if_network_is_trained(context):
    context.train_network_page.check_if_network_is_trained(context.networks)


@then("Check if network exist")
def check_network(context):
    context.add_network_page.check_networks_lists(context.networks)


@then("Clear layers")
def clear_layers(context):
    context.add_network_page.clear_layers()


@then("Delete network")
def delete_network(context):
    for network in context.networks:
        context.add_network_page.click_delete_network(network)
        time.sleep(2)
