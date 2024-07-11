"""Flask webapp mycoolapp."""

from flask import Flask, render_template

from . import config, logger

mca_sett = config.MyCoolAppConfig()  # Create the default config object


def create_app(test_config: dict | None = None, instance_path: str | None = None) -> Flask:
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True, instance_path=instance_path)

    logger.setup_logger(app, mca_sett["logging"])  # Setup logger per defaults

    if test_config:  # For Python testing we will often pass in a flask config
        mca_sett.load_config_from_dictionary(test_config)  # Loads app config from dict provided
    else:
        mca_sett.load_config_from_disk(app.instance_path)  # Loads app config from disk

    logger.setup_logger(app, mca_sett["logging"])  # Setup logger per config

    app.config.from_mapping(mca_sett["flask"])  # Flask config config, separate

    # Do some debug logging of config
    mca_sett.log_config()
    app_config_str = f">>>\nFlask object loaded app.config:\n{app.config.items()}"
    app.logger.debug(app_config_str)

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


def get_mycoolapp_config() -> dict:
    """Return the config object to whatever needs it."""
    return mca_sett
