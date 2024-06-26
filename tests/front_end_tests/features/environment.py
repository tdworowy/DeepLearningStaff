import time
from os import path, makedirs
import yaml

from ..logging.logger_ import TestsLogger, take_screenshot
from ..webdriver_wapper.webdriver_wrapper import WebDriverWrapper

BEHAVE_DEBUG = True
logs_path = "logs"


def create_dir(name: str):
    if not path.exists(name):
        makedirs(name)


def read_config():
    with open("test_config.yaml") as file:
        return yaml.safe_load(file)


def before_feature(context, feature):
    config = read_config()
    context.url = config["url"]
    context.browser = config["browser"]
    create_dir(logs_path)

    context.feature_logger = TestsLogger()
    context.log_feature_file = path.join(logs_path, "%s_Log.log" % feature.name)
    context.feature_logger.add_log_file(context.log_feature_file)
    context.feature_logger.log().info("Start Feature: " + feature.name)


def before_scenario(context, scenario):
    context.scenario_logger = TestsLogger()

    context.scenario_name = scenario.name.replace(" ", "_")
    context.time_stump = str(time.strftime("%Y-%m-%d_%H_%M_%S"))
    context.logs_dir_name = path.join(
        logs_path, context.scenario_name + "_" + context.time_stump
    )
    create_dir(context.logs_dir_name)
    context.log_file = path.join(
        context.logs_dir_name,
        "%s_Log_%s.log" % (context.scenario_name, context.time_stump),
    )
    context.scenario_logger.add_log_file(context.log_file)

    context.web_driver_wrapper = WebDriverWrapper(browser=context.browser)

    context.scenario_logger.log().info("Scenario started: " + scenario.name)


def before_step(context, step):
    context.scenario_logger.log().info("Step: " + step.name)


def after_scenario(context, scenario):
    context.scenario_logger.log().info(f"Test Finished: {context.scenario_name}")
    context.scenario_logger.log().info(f"Scenario status: {str(scenario.status)}")
    context.web_driver_wrapper.tear_down()


def after_step(context, step):
    take_screenshot(
        context.web_driver_wrapper.driver, context.logs_dir_name, "%s" % step.name
    )
    context.scenario_logger.log().info(f"Step status:{str(step.status)}")
    if str(step.status) == "Status.failed":
        context.scenario_logger.log().error("STEP FAIL")
        for entry in context.web_driver_wrapper.driver.get_log("browser"):
            context.scenario_logger.log().info(entry)


def after_feature(context, feature):
    context.feature_logger.log().info(f"Feature Finished: {feature.name}")
    context.feature_logger.log().info(f"Feature status: {str(feature.status)}")
