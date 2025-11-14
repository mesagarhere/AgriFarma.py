from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired

class ConsultantRegistrationForm(FlaskForm):
    category = StringField("Category", validators=[DataRequired()])
    expertise = TextAreaField("Expertise", validators=[DataRequired()])
    contact = StringField("Contact Info", validators=[DataRequired()])
    submit = SubmitField("Submit")
