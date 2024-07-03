"""Blueprints for ..."""

import logging

from flask import Blueprint, jsonify

from . import get_mycoolapp_settings

mca_sett = get_mycoolapp_settings()  # Get the settings

# This means that the logger will have the right name, loging should be done with this object
logger = logging.getLogger(__name__)

bp = Blueprint("mycoolapp", __name__)


@bp.route("/hello/", methods=["GET"])
def get_hello() -> int:
    """Hello GET Method."""
    message = {"msg": mca_sett.my_message}
    status = 200

    logger.debug("GET request to /hello/, returning: %s", mca_sett.my_message)

    return jsonify(message), status
