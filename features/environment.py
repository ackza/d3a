import contextlib
import shutil
import os

"""
before_step(context, step), after_step(context, step)
    These run before and after every step.
    The step passed in is an instance of Step.
before_scenario(context, scenario), after_scenario(context, scenario)
    These run before and after each scenario is run.
    The scenario passed in is an instance of Scenario.
before_feature(context, feature), after_feature(context, feature)
    These run before and after each feature file is exercised.
    The feature passed in is an instance of Feature.
before_tag(context, tag), after_tag(context, tag)
"""

# -- SETUP: Use cfparse as default matcher
# from behave import use_step_matcher
# step_matcher("cfparse")


def before_scenario(context, scenario):
    context.simdir = "./d3a-simulation/integration_tests/"
    os.makedirs(context.simdir, exist_ok=True)
    context.resource_manager = contextlib.ExitStack()


def after_scenario(context, scenario):
    shutil.rmtree(context.simdir)
    context.resource_manager.close()


def before_all(context):
    context.config.setup_logging()