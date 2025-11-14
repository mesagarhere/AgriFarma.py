# append to agrilink_sindh/models.py

from datetime import datetime
from agrilink_sindh.extensions import db

# Product model
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    category = db.Column(db.String(80), nullable=True)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, default=0)
    description = db.Column(db.Text, nullable=True)
    seller_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)  # optional
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    seller = db.relationship("User", backref="products")

# CartItem model (simple per-user cart)
class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    added_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User", backref="cart_items")
    product = db.relationship("Product")

# Order + OrderItem
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    total_amount = db.Column(db.Float, nullable=False, default=0.0)
    status = db.Column(db.String(30), default='pending')  # pending, confirmed, shipped, completed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User", backref="orders")
    items = db.relationship("OrderItem", backref="order", cascade="all, delete-orphan")

class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    product_name = db.Column(db.String(150), nullable=False)
    unit_price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
