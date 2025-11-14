from agrilink_sindh.extensions import db
from agrilink_sindh import create_app

app = create_app()

with app.app_context():
    db.create_all()
    print("Tables created!")
