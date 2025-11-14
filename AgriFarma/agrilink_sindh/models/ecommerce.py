from datetime import datetime
from agrilink_sindh.extensions import db


class CartItem(db.Model):
    __tablename__ = 'cart_item'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)

    product = db.relationship('Product', backref='cart_items')


class Order(db.Model):
    __tablename__ = 'order'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    total_amount = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class OrderItem(db.Model):
    __tablename__ = 'order_item'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    product_name = db.Column(db.String(200))
    unit_price = db.Column(db.Float, default=0.0)
    quantity = db.Column(db.Integer, default=1)

    product = db.relationship('Product')
