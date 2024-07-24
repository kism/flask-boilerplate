"""Blueprints for..."""

import logging

from flask import Blueprint, current_app, jsonify

# The current_app import is a bit special, do not use it outside of a function because
# when the parent (__init__.py create_app()) imports this module, it needs to `with app.app_context():`
# which will keep current_app in a pretty default state. Once flask is serving the app the current_app
# object will function fine... i'm pretty sure. https://flask.palletsprojects.com/en/3.0.x/appcontext/

# Modules should all setup logging like this so the log messages include the modules name.
# If you were to list all loggers with something like...
# `loggers = [logging.getLogger(name) for name in logging.root.manager.loggerDict]`
# Before creating this object, you would not see a logger with this modules name (mycoolapp.this_module_name)
logger = logging.getLogger(__name__)  # Create a logger: mycoolapp.this_module_name, inherit config from root logger

# Register this module (__name__) as available to the blueprints of mycoolapp, I think https://flask.palletsprojects.com/en/3.0.x/blueprints/
bp = Blueprint("mycoolapp", __name__)


# KISM-BOILERPLATE: This is the demo api endpoint, enough to show a basic javascript interaction.
@bp.route("/hello/", methods=["GET"])
def get_hello() -> int:
    """Hello GET Method."""
    message = {"msg": current_app.config["app"]["my_message"]}
    status = 200

    logger.debug("GET request to /hello/, returning: %s", current_app.config["app"])

    return jsonify(message), status  # Return json, not a webpage.
