"""Flask webapp mycoolapp."""

import os
import tomllib

from flask import Flask, render_template

from . import mycoolapp_logger

mycoolapp_logger.setup_logger()


def create_app(test_config: dict | None = None) -> Flask:
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)

    if test_config:  # For Python testing we will often pass in a flask config
        app.config.from_object(test_config)
    else:  # Otherwise we try load config from a file, instance/flask.toml
        flask_config_path = f"{app.instance_path}{os.sep}flask.toml"
        try:
            app.config.from_file("flask.toml", load=tomllib.load, text=False)
            app.logger.warning("Loaded flask config from: %s", flask_config_path)
        except FileNotFoundError:
            app.logger.info("No flask configuration file found at: %s", flask_config_path)
            app.logger.info("Using flask app.config defaults (this is not a problem).")

    flask_settings_message = "Flask Settings:\n" + "\n".join([f"{key}: {value}" for key, value in app.config.items()])
    app.logger.debug(flask_settings_message)

    # Now that we have loaded out configuration, we can import our modules
    from . import mycoolapp_blueprint_one

    # Register blueprints
    app.register_blueprint(mycoolapp_blueprint_one.bp)

    @app.route("/")
    def home() -> str:
        """Flask Home."""
        return render_template("home.html.j2", app_name=__name__)

    return app


def get_mycoolapp_settings() -> dict:
    """Return the settings object to whatever needs it."""
    return mca_sett


if __name__ == "mycoolapp":  # Is this normal? It might be, the linter doesnt complain about the imports being here.
    from . import mycoolapp_settings

    mca_sett = mycoolapp_settings.MyCoolAppSettings()  # Create the settings object

    mycoolapp_logger.setup_logger(mca_sett)  # Setup logger per settings
