"""Small runner script to start the agrilink_sindh Flask app.

Run with the project's virtualenv Python from the repository root.
"""
from agrilink_sindh.app import app
from agrilink_sindh.extensions import db


if __name__ == '__main__':
    # Ensure database exists and tables are created before starting the server.
    with app.app_context():
        db.create_all()

    # Run the app object defined in `agrilink_sindh/app.py`.
    app.run(debug=True, host='127.0.0.1', port=5000)
