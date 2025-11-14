from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from agrilink_sindh.extensions import db
from agrilink_sindh.models.product_model import Product, CartItem, Order, OrderItem

shop = Blueprint('shop', __name__)

# SHOW ALL PRODUCTS
@shop.route('/marketplace')
def marketplace():
    products = Product.query.all()
    return render_template('marketplace.html', products=products)

# SELL PRODUCT
@shop.route('/sell', methods=['GET', 'POST'])
@login_required
def sell_product():
    if request.method == 'POST':
        product = Product(
            name=request.form['name'],
            price=float(request.form['price']),
            quantity=int(request.form['quantity']),
            description=request.form['description'],
            seller_id=current_user.id
        )
        db.session.add(product)
        db.session.commit()
        return redirect(url_for('shop.marketplace'))

    return render_template('sell_product.html')

# ADD TO CART
@shop.route('/cart/add/<int:product_id>')
@login_required
def add_to_cart(product_id):
    item = CartItem(product_id=product_id, user_id=current_user.id)
    db.session.add(item)
    db.session.commit()
    return redirect(url_for('shop.cart'))

# SHOW CART
@shop.route('/cart')
@login_required
def cart():
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    return render_template('cart.html', cart_items=cart_items)

# CHECKOUT
@shop.route('/checkout')
@login_required
def checkout():
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    total = 0

    for item in cart_items:
        total += item.product.price * item.quantity

    order = Order(user_id=current_user.id, total_price=total)
    db.session.add(order)
    db.session.commit()

    for item in cart_items:
        order_item = OrderItem(
            order_id=order.id,
            product_id=item.product_id,
            quantity=item.quantity,
            price=item.product.price
        )
        db.session.add(order_item)
        db.session.delete(item)

    db.session.commit()
    return redirect(url_for('shop.orders'))

# ORDER HISTORY
@shop.route('/orders')
@login_required
def orders():
    user_orders = Order.query.filter_by(user_id=current_user.id).all()
    return render_template('orders.html', orders=user_orders)
