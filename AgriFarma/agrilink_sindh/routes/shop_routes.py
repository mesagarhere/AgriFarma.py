from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from agrilink_sindh.models.product_model import Product
from agrilink_sindh.extensions import db

shop = Blueprint("shop", __name__)

# Marketplace page
@shop.route("/marketplace")
@login_required
def marketplace():
    products = Product.query.all()
    return render_template("marketplace.html", products=products)

# Product detail page
@shop.route("/product/<int:id>")
@login_required
def product_detail(id):
    product = Product.query.get_or_404(id)
    return render_template("product_detail.html", product=product)

# Add product (sell)
@shop.route("/sell", methods=["GET", "POST"])
@login_required
def sell_product():
    if request.method == "POST":
        name = request.form.get("name")
        category = request.form.get("category")
        price = request.form.get("price")
        quantity = request.form.get("quantity")
        description = request.form.get("description")

        product = Product(
            name=name,
            category=category,
            price=float(price),
            quantity=int(quantity),
            description=description,
            seller_id=current_user.id
        )

        db.session.add(product)
        db.session.commit()

        return redirect(url_for("shop.marketplace"))

    return render_template("sell_product.html")
