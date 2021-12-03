"""Initialize Flask app."""

from flask import Flask


def init_app():
    """Construct core Flask application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')

    with app.app_context():
        # Import parts of our core Flask app
        # from . import train2
        # from . import chat2
        from . import routes
        from .dashboard.dashboard import init_dashboard
        from flask_login import login_required

        app, dash_app = init_dashboard(app)
        # Registrar blueprints para inicializar código y desacoplar routes.py

        for view_func in app.view_functions:
            if view_func.startswith("/dashapp"):
                app.view_functions[view_func] = login_required(app.view_functions[view_func])
        return app
