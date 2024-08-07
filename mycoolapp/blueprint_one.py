"""Blueprint one's object..."""

import logging

from flask import Blueprint, Response, current_app, jsonify

from . import blueprint_one_object

# Modules should all setup logging like this so the log messages include the modules name.
# If you were to list all loggers with something like...
# `loggers = [logging.getLogger(name) for name in logging.root.manager.loggerDict]`
# Before creating this object, you would not see a logger with this modules name (mycoolapp.this_module_name)
logger = logging.getLogger(__name__)  # Create a logger: mycoolapp.this_module_name, inherit config from root logger

# Register this module (__name__) as available to the blueprints of mycoolapp, I think https://flask.palletsprojects.com/en/3.0.x/blueprints/
bp = Blueprint("mycoolapp", __name__)

my_cool_object = None


# KISM-BOILERPLATE:
# So regarding current_app, have a read of https://flask.palletsprojects.com/en/3.0.x/appcontext/
# This function is a bit of a silly example, but often you need to do things to initialise the module.
# You can't use the current_app object outside of a function since it behaves a bit weird, even if
#   you import the module under `with app.app_context():`
# So we call this to set globals in this module.
# You don't need to use this to set every variable as current_app will work fine in any function.
def start_blueprint_one() -> None:
    """Method to 'configure' this module. Needs to be called under `with app.app_context():` from __init__.py."""
    global my_cool_object  # noqa: PLW0603 Necessary evil as far as I can tell, could move to all objects but eh...
    my_cool_object = blueprint_one_object.MyCoolObject(current_app.config)


# KISM-BOILERPLATE: This is the demo api endpoint, enough to show a basic javascript interaction.
@bp.route("/hello/", methods=["GET"])
def get_hello() -> tuple[Response, int]:
    """Hello GET Method."""
    message = {"msg": current_app.config["app"]["my_message"]}
    status = 200

    logger.debug(
        "GET request to /hello/, returning: %s as json, due to config: %s",
        message,
        current_app.config["app"],
    )

    return jsonify(message), status  # Return json, not a webpage.


# KISM-BOILERPLATE: This is the demo api endpoint, enough to demonstrate object loading.
@bp.route("/hello_backwards/", methods=["GET"])
def get_hello_backwards() -> tuple[Response, int]:
    """Hello GET Method."""
    message = {"msg": my_cool_object.get_my_message_backwards()}
    status = 200

    logger.debug(
        "GET request to /hello_backwards/, returning: %s",
        message,
    )

    return jsonify(message), status  # Return json, not a webpage.
