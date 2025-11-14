from agrilink_sindh.extensions import db
from datetime import datetime

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    farmer_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    consultant_id = db.Column(db.Integer, db.ForeignKey("consultant.id"))
    message = db.Column(db.String(300))
    status = db.Column(db.String(20), default="pending")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
