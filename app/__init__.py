from flask import Flask

from app.config import Config
from app.services.storage import ensure_storage


def create_app(config_class=Config):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_class)

    from app.blueprints.main.routes import bp as main_bp
    from app.blueprints.bedding.routes import bp as bedding_bp
    from app.blueprints.inventory.routes import bp as inventory_bp
    from app.blueprints.reports.routes import bp as reports_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(bedding_bp)
    app.register_blueprint(inventory_bp)
    app.register_blueprint(reports_bp)

    register_cli(app)
    return app


def register_cli(app):
    @app.cli.command("init-db")
    def init_db_command():
        """Create Excel storage files for first-time local setup."""
        ensure_storage()
        print("Excel storage initialized.")
