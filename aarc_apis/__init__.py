"""The configs directory acts as the package that will handle the configuration of the application as a whole.

Please note that any and all configuration for the application should reside here for easier configuration.
This also includes .secrets.<config_extension> that which is ignored by gitignore.
"""
import logging
import coloredlogs

from logging.config import dictConfig
from dynaconf import settings, FlaskDynaconf


from flask import Flask

logger = logging.getLogger(__name__)
flask_conf = FlaskDynaconf()

def create_app(config_file=None):
    """
    App factory.

    Create an application instance and return it.

    :param config_file: TODO: Future usecase for a config file based app instantiation.
    :return:
    """

    app = Flask(__name__)

    # Initialize logs with custom config.
    dictConfig(settings.LOGGING_CONFIG)

    # Initialize colored logs.
    coloredlogs.install(level=logging.DEBUG)

    # Registering api blueprint. 
    from aarc_apis.routes import api
    app.register_blueprint(api, url_prefix='/api/v1')

    # Configuring dynaconf for app instance
    flask_conf.init_app(app)
    return app
