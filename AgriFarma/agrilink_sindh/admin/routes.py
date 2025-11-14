from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from agrilink_sindh.extensions import db
from agrilink_sindh.models.product_model import Product

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin/products')
@login_required
def admin_products():
    products = Product.query.order_by(Product.id.desc()).all()
    return render_template('admin/products.html', products=products)

@admin_bp.route('/admin/product/add', methods=['GET', 'POST'])
@login_required
def admin_add_product():
    if request.method == 'POST':
        p = Product(
            name=request.form['name'],
            category=request.form.get('category'),
            price=float(request.form['price']),
            quantity=int(request.form['quantity']),
            description=request.form.get('description'),
            seller_id=None
        )
        db.session.add(p); db.session.commit()
        flash('Product added', 'success'); return redirect(url_for('admin.admin_products'))
    return render_template('admin/add_product.html')

@admin_bp.route('/admin/product/edit/<int:pid>', methods=['GET','POST'])
@login_required
def admin_edit_product(pid):
    p = Product.query.get_or_404(pid)
    if request.method == 'POST':
        p.name = request.form['name']; p.category = request.form.get('category')
        p.price = float(request.form['price']); p.quantity = int(request.form['quantity'])
        p.description = request.form.get('description')
        db.session.commit(); flash('Product updated','success'); return redirect(url_for('admin.admin_products'))
    return render_template('admin/edit_product.html', product=p)

@admin_bp.route('/admin/product/delete/<int:pid>')
@login_required
def admin_delete_product(pid):
    p = Product.query.get_or_404(pid)
    db.session.delete(p); db.session.commit()
    flash('Product removed','info'); return redirect(url_for('admin.admin_products'))
