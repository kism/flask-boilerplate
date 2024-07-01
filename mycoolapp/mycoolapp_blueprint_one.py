"""Blueprints for ..."""

import logging

from flask import Blueprint, jsonify

from . import get_mycoolapp_settings

mca_sett = get_mycoolapp_settings() # Settings object

logger = logging.getLogger(__name__)

bp = Blueprint("mycoolapp", __name__)


@bp.route("/hello/", methods=["GET"])
def get_hello() -> int:
    """Hello GET Method."""
    message = {"msg": "Hello!"}
    status = 200

    return jsonify(message), status
