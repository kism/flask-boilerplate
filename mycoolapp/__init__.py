"""Flask webapp mycoolapp."""

from flask import Flask, render_template

from . import config, logger


def create_app(test_config: dict | None = None, instance_path: str | None = None) -> Flask:
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True, instance_path=instance_path)

    logger.setup_logger(app, config.DEFAULT_CONFIG["logging"])

    if test_config:  # For Python testing we will often pass in a config
        if not instance_path:
            app.logger.critical("When testing supply both test_config and instance_path!")
            raise AttributeError
        mca_conf = config.MyCoolAppConfig(config=test_config, instance_path=app.instance_path)
    else:
        mca_conf = config.MyCoolAppConfig(instance_path=app.instance_path)  # Loads app config from disk

    app.logger.debug("Instance path is: %s", app.instance_path)

    logger.setup_logger(app, mca_conf["logging"])  # Setup logger

    # Flask config, at the root of the config object.
    app.config.from_mapping(mca_conf["flask"])

    # Other sections handled by config.py
    app.config["app"] = mca_conf["app"]
    app.config["logging"] = mca_conf["logging"]

    # Do some debug logging of config
    app_config_str = f">>>\nFlask config:\n{app.config.items()}"
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
