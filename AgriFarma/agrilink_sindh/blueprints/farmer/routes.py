from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from agrilink_sindh.models.post_model import Post
from agrilink_sindh.models.task_model import Task
from agrilink_sindh.extensions import db

farmer_bp = Blueprint("farmer", __name__)

# -------------------------
# Farmer Dashboard Home
# -------------------------
@farmer_bp.route("/farmer/dashboard")
@login_required
def dashboard_home():
    posts = Post.query.filter_by(farmer_id=current_user.id).all()
    tasks = Task.query.filter_by(farmer_id=current_user.id).all()
    return render_template("farmer/dashboard.html", posts=posts, tasks=tasks)


# -------------------------
# Create Post
# -------------------------
@farmer_bp.route("/farmer/post/add", methods=["POST"])
@login_required
def add_post():
    title = request.form.get("title")
    description = request.form.get("description")
    p = Post(farmer_id=current_user.id, title=title, description=description)
    db.session.add(p)
    db.session.commit()
    return redirect(url_for("farmer.dashboard_home"))


# -------------------------
# Create Task
# -------------------------
@farmer_bp.route("/farmer/task/add", methods=["POST"])
@login_required
def add_task():
    title = request.form.get("title")
    t = Task(farmer_id=current_user.id, title=title)
    db.session.add(t)
    db.session.commit()
    return redirect(url_for("farmer.dashboard_home"))
