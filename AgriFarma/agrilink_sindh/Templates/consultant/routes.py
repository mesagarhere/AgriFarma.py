from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from agrilink_sindh.extensions import db
from agrilink_sindh.models import Consultant
from agrilink_sindh.consultant.forms import ConsultantRegisterForm

consultant = Blueprint("consultant", __name__)


# ------------------------------------------------------
# CONSULTANT REGISTRATION PAGE
# ------------------------------------------------------
@consultant.route("/consultant/register", methods=["GET", "POST"])
@login_required
def consultant_register():
    form = ConsultantRegisterForm()

    # Check if user already has consultant profile
    existing = Consultant.query.filter_by(user_id=current_user.id).first()
    if existing:
        flash("You have already submitted a consultant application!", "info")
        return redirect(url_for("consultant.consultant_profile"))

    if form.validate_on_submit():
        new_profile = Consultant(
            user_id=current_user.id,
            category=form.category.data,
            expertise=form.expertise.data,
            experience_years=form.experience_years.data,
            contact=form.contact.data,
            approved=False  # Admin will approve
        )

        db.session.add(new_profile)
        db.session.commit()

        flash("Your application has been submitted. Wait for admin approval.", "success")
        return redirect(url_for("consultant.consultant_profile"))

    return render_template("consultant/consultant_register.html", form=form)


# ------------------------------------------------------
# CONSULTANT PROFILE PAGE
# ------------------------------------------------------
@consultant.route("/consultant/profile")
@login_required
def consultant_profile():
    profile = Consultant.query.filter_by(user_id=current_user.id).first()

    if not profile:
        flash("You have not applied as a consultant yet!", "warning")
        return redirect(url_for("consultant.consultant_register"))

    return render_template("consultant/consultant_profile.html", profile=profile)


# ------------------------------------------------------
# PUBLIC CONSULTANT DIRECTORY (ALL APPROVED CONSULTANTS)
# ------------------------------------------------------
@consultant.route("/consultants")
def consultant_directory():
    consultants = Consultant.query.filter_by(approved=True).all()
    return render_template("consultant/consultant_directory.html", consultants=consultants)
from .routes import consultant
