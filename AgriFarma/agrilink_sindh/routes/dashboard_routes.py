from flask import Blueprint, redirect, url_for, render_template
from flask_login import login_required, current_user

dashboard = Blueprint('dashboard', __name__)

@dashboard.route('/dashboard')
@login_required
def dashboard_home():
    if current_user.role.lower() == 'farmer':
        return redirect(url_for('dashboard.farmer_dashboard'))
    elif current_user.role.lower() == 'consultant':
        return redirect(url_for('dashboard.consultant_dashboard'))
    else:
        return "<h3>Role not recognized</h3>"

@dashboard.route('/dashboard/farmer')
@login_required
def farmer_dashboard():
    return render_template("dashboard_farmer.html", user=current_user)

@dashboard.route('/dashboard/consultant')
@login_required
def consultant_dashboard():
    return render_template("dashboard_consultant.html", user=current_user)
