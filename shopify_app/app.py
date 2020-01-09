
from flask import Flask

from shopify_app.settings import ProdConfig
from shopify_app.extensions import db, migrate
from shopify_app.shopify_bp import shopify_bp, Shop
from shopify_app import commands
from shopify_app.exceptions import InvalidUsage

__all__ = ['create_app']

DEFAULT_BLUEPRINTS = (
    shopify_bp,
)


def create_app(config=ProdConfig):
    app = Flask(__name__.split('.')[0])
    app.url_map.strict_slashes = False
    app.config.from_object(config)
    register_extensions(app)
    register_blueprints(app)
    register_errorhandlers(app)
    register_shellcontext(app)
    register_commands(app)
    return app


def register_extensions(app):
    """Register Flask extensions."""
    db.init_app(app)
    migrate.init_app(app, db)


def register_blueprints(app):
    """Register Flask blueprints."""
    app.register_blueprint(shopify_bp)


def register_errorhandlers(app):

    def errorhandler(error):
        response = error.to_json()
        response.status_code = error.status_code
        return response

    app.errorhandler(InvalidUsage)(errorhandler)


def register_shellcontext(app):
    """Register shell context objects."""
    def shell_context():
        """Shell context objects."""
        return {
            'db': db,
            'Shop': Shop
        }

    app.shell_context_processor(shell_context)


def register_commands(app):
    """Register Click commands."""
    app.cli.add_command(commands.test)
    app.cli.add_command(commands.clean)
    app.cli.add_command(commands.urls)
