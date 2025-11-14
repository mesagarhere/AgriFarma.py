from flask import Blueprint, render_template
from agrilink_sindh.models.consultant import Consultant

consultant_bp = Blueprint('consultant', __name__)

@consultant_bp.route('/consultants')
def consultant_directory():
    consultants = Consultant.query.filter_by(approved=True).all()
    return render_template("consultant/directory.html", consultants=consultants)
