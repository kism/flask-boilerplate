"""Flask webapp mycoolapp."""

from flask import Flask, render_template

from . import logger
from .config import MyCoolAppConfig

mca_sett = MyCoolAppConfig()  # Create the settings object


def create_app(test_config: object | None = None) -> Flask:
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)

    logger.setup_logger(app)  # Setup logger per defaults

    mca_sett.load_settings_from_disk(app.instance_path)  # Loads app settings from disk

    logger.setup_logger(app, mca_sett.logging)  # Setup logger per settings

    # This is for the flask config, separate from everything in settings.py
    if test_config:  # For Python testing we will often pass in a flask config
        app.config.from_mapping(test_config)
    else:
        # Otherwise we try load config from config loaded, I use SimpleNamespace to convert the dictionary
        # to an object since Flask can't load config from a dict.
        app.config.from_mapping(mca_sett.flask)

    flask_settings_message = "Flask Settings:\n" + "\n".join([f"{key}: {value}" for key, value in app.config.items()])
    app.logger.debug(flask_settings_message)

    # Now that we have loaded out configuration, we can import our modules
    from . import blueprint_one

    # Register blueprints
    app.register_blueprint(blueprint_one.bp)

    @app.route("/")
    def home() -> str:
        """Flask Home."""
        return render_template("home.html.j2", app_name=__name__)

    app.logger.info("Starting Web Server")

    return app


def get_mycoolapp_settings() -> dict:
    """Return the settings object to whatever needs it."""
    return mca_sett
