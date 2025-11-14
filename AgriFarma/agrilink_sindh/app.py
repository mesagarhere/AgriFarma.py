from flask import Flask
import os
from .extensions import db, bcrypt, login_manager

# Initialize Flask app
app = Flask(__name__)

# App Configuration
app.config['SECRET_KEY'] = 'supersecretkey'
# Use absolute path for SQLite DB to avoid relative-path issues
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
db_file = os.path.join(base_dir, 'instance', 'agrilink.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_file}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db.init_app(app)
bcrypt.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'

# Import Blueprints AFTER initializing extensions
from .routes.auth_routes import auth
from .routes.main_routes import main
from .routes.dashboard_routes import dashboard

# Blueprints implemented under `blueprints/`
from agrilink_sindh.blueprints.shop.routes import shop_bp
from agrilink_sindh.admin.routes import admin_bp
from agrilink_sindh.blueprints.farmer.routes import farmer_bp

# Register Blueprints
app.register_blueprint(auth)
app.register_blueprint(main)
app.register_blueprint(dashboard)
app.register_blueprint(shop_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(farmer_bp)


# Database tables are created by the runner to avoid creating DB during import

# Run Server
if __name__ == "__main__":
	app.run(debug=True)
