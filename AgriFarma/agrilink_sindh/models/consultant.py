from datetime import datetime
from agrilink_sindh.extensions import db


class Consultant(db.Model):
    __tablename__ = 'consultant'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category = db.Column(db.String(100), nullable=True)
    expertise = db.Column(db.String(200), nullable=True)
    experience_years = db.Column(db.Integer, default=0)
    contact = db.Column(db.String(100), nullable=True)

    approved = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('consultant_profile', uselist=False))

    def __repr__(self):
        return f"<Consultant {self.id} - user {self.user_id}>"
