from flask import Flask
from agrilink_sindh.extensions import db, login_manager
try:
    from agrilink_sindh.consultant.routes import consultant
except Exception:
    consultant = None

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)
    login_manager.init_app(app)

    # Register blueprints
    from agrilink_sindh.auth.routes import auth
    from agrilink_sindh.dashboard.routes import dashboard

    app.register_blueprint(auth)
    app.register_blueprint(dashboard)
    if consultant:
        app.register_blueprint(consultant)

    return app
