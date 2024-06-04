"""Blueprints for ..."""

import logging

from flask import Blueprint, jsonify

logger = logging.getLogger(__name__)

bp = Blueprint("mycoolapp", __name__)


@bp.route("/hello/", methods=["GET"])
def get_hello() -> int:
    """Hello GET Method."""
    message = {"msg": "Hello!"}
    status = 200

    return jsonify(message), status
