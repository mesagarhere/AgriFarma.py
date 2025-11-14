from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from agrilink_sindh.extensions import db
from agrilink_sindh.models.product_model import Product
from agrilink_sindh.models.ecommerce import CartItem, Order, OrderItem

try:
    import pandas as pd
except Exception:
    pd = None

shop_bp = Blueprint('shop', __name__)

# Marketplace: supports simple query params ?q=&category=&sort=price_asc etc.
@shop_bp.route('/marketplace')
def marketplace():
    q = request.args.get('q', '').strip()
    category = request.args.get('category')
    sort = request.args.get('sort')  # 'price_asc', 'price_desc', 'newest'
    # basic SQLAlchemy query
    query = Product.query.filter(Product.quantity > 0)
    if q:
        query = query.filter(Product.name.ilike(f'%{q}%') | Product.description.ilike(f'%{q}%'))
    if category:
        query = query.filter_by(category=category)

    if sort == 'price_asc':
        products = query.order_by(Product.price.asc()).all()
    elif sort == 'price_desc':
        products = query.order_by(Product.price.desc()).all()
    elif sort == 'newest':
        products = query.order_by(Product.created_at.desc()).all()
    else:
        products = query.order_by(Product.id.desc()).all()

    return render_template('marketplace.html', products=products, q=q, category=category, sort=sort)

# Market advanced filtering via pandas (reads DB into DataFrame)
@shop_bp.route('/marketplace/filter', methods=['GET', 'POST'])
def marketplace_filter():
    # create DataFrame from products table using SQLAlchemy engine if pandas is available
    if pd:
        df = pd.read_sql_table('product', con=db.engine)
    else:
        # fallback: load products via SQLAlchemy and convert to list of dicts
        products = Product.query.all()
        cols = ['id','name','category','price','quantity','description','seller_id']
        import datetime
        rows = []
        for p in products:
            rows.append({
                'id': p.id,
                'name': p.name,
                'category': p.category,
                'price': p.price,
                'quantity': p.quantity,
                'description': p.description,
                'seller_id': p.seller_id,
            })
        # create a basic in-memory table representation
        class SimpleDF(list):
            def to_dict(self, orient='records'):
                return list(self)

        df = SimpleDF(rows)
    # get filters from form or query params
    min_price = request.values.get('min_price')
    max_price = request.values.get('max_price')
    cat = request.values.get('category')
    if min_price:
        try: df = df[df['price'] >= float(min_price)]
        except: pass
    if max_price:
        try: df = df[df['price'] <= float(max_price)]
        except: pass
    if cat:
        df = df[df['category'] == cat]
    # sort
    sort = request.values.get('sort')
    if sort == 'price_asc':
        df = df.sort_values('price', ascending=True)
    elif sort == 'price_desc':
        df = df.sort_values('price', ascending=False)
    results = df.to_dict(orient='records') if hasattr(df, 'to_dict') else list(df)
    return render_template('marketplace_filtered.html', products=results)

# Product detail
@shop_bp.route('/product/<int:pid>')
def product_detail(pid):
    p = Product.query.get_or_404(pid)
    return render_template('product_detail.html', product=p)

# Seller: post product for sale
@shop_bp.route('/sell', methods=['GET', 'POST'])
@login_required
def sell_product():
    if request.method == 'POST':
        name = request.form.get('name')
        category = request.form.get('category')
        price = float(request.form.get('price') or 0)
        quantity = int(request.form.get('quantity') or 0)
        description = request.form.get('description')

        p = Product(name=name, category=category, price=price,
                    quantity=quantity, description=description,
                    seller_id=current_user.id)
        db.session.add(p)
        db.session.commit()
        flash('Product posted for sale.', 'success')
        return redirect(url_for('shop.product_detail', pid=p.id))
    return render_template('sell_product.html')

# Add to cart
@shop_bp.route('/cart/add/<int:pid>', methods=['POST'])
@login_required
def add_to_cart(pid):
    qty = int(request.form.get('quantity', 1))
    product = Product.query.get_or_404(pid)
    if qty <= 0:
        flash('Invalid quantity', 'danger'); return redirect(url_for('shop.product_detail', pid=pid))
    # check if already in cart
    item = CartItem.query.filter_by(user_id=current_user.id, product_id=pid).first()
    if item:
        item.quantity += qty
    else:
        item = CartItem(user_id=current_user.id, product_id=pid, quantity=qty)
        db.session.add(item)
    db.session.commit()
    flash('Added to cart', 'success')
    return redirect(url_for('shop.cart_view'))

# View cart
@shop_bp.route('/cart')
@login_required
def cart_view():
    items = CartItem.query.filter_by(user_id=current_user.id).all()
    total = sum(i.quantity * i.product.price for i in items)
    return render_template('cart.html', items=items, total=total)

# Checkout (create order from cart)
@shop_bp.route('/checkout', methods=['POST'])
@login_required
def checkout():
    items = CartItem.query.filter_by(user_id=current_user.id).all()
    if not items:
        flash('Cart empty', 'warning'); return redirect(url_for('shop.cart_view'))

    order = Order(user_id=current_user.id, total_amount=0.0)
    db.session.add(order)
    db.session.flush()  # get order.id
    total = 0.0
    for it in items:
        if it.quantity > it.product.quantity:
            flash(f'Not enough stock for {it.product.name}', 'danger')
            db.session.rollback()
            return redirect(url_for('shop.cart_view'))
        oi = OrderItem(order_id=order.id,
                       product_id=it.product.id,
                       product_name=it.product.name,
                       unit_price=it.product.price,
                       quantity=it.quantity)
        db.session.add(oi)
        # decrement stock
        it.product.quantity -= it.quantity
        total += it.quantity * it.product.price
    order.total_amount = total
    # clear cart
    CartItem.query.filter_by(user_id=current_user.id).delete()
    db.session.commit()
    flash('Order placed successfully!', 'success')
    return redirect(url_for('shop.order_history'))

# Order history
@shop_bp.route('/orders')
@login_required
def order_history():
    orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.created_at.desc()).all()
    return render_template('orders.html', orders=orders)
