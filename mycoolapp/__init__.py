"""Flask webapp mycoolapp."""

from flask import Flask, render_template

from . import config, logger

mca_conf = config.MyCoolAppConfig()  # Create the default config object


def create_app(test_config: dict | None = None, instance_path: str | None = None) -> Flask:
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True, instance_path=instance_path)

    app.logger.info("Instance path is: %s", instance_path)

    logger.setup_logger(app, mca_conf["logging"])  # Setup logger per defaults

    if test_config:  # For Python testing we will often pass in a config
        mca_conf.load_from_dictionary(test_config)  # Loads app config from dict provided
    else:
        mca_conf.load_from_disk(app.instance_path)  # Loads app config from disk

    logger.setup_logger(app, mca_conf["logging"])  # Setup logger per config

    app.config.from_mapping(mca_conf["flask"])  # Flask config, separate

    # Do some debug logging of config
    mca_conf.log_config()
    app_config_str = f">>>\nFlask object loaded app.config:\n{app.config.items()}"
    app.logger.debug(app_config_str)

    # Now that we have loaded out configuration, we can import our blueprints
    # KISM-BOILERPLATE: This is a demo blueprint blueprint_one.py. Rename the file
    #  and vars to make your own http endpoints and pages. Use multiple blueprints if
    #  you have functionality you can categorise.
    from . import blueprint_one

    app.register_blueprint(blueprint_one.bp)  # Register blueprint

    # Flask homepage, generally don't have this as a blueprint.
    @app.route("/")
    def home() -> str:
        """Flask home."""
        return render_template("home.html.j2", app_name=__name__)  # Return a webpage

    app.logger.info("Starting Web Server")

    return app


def get_mycoolapp_config() -> dict:
    """Return the config object to whatever needs it."""
    return mca_conf
