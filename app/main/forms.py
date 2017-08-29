from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import Required, Length, URL
from wtforms import ValidationError


class ItemForm(FlaskForm):
    header = StringField("Your pitch here", validators=[Required()])
    body = TextAreaField("Tell me everything", validators=[Required()])
    img_url = StringField("Enter item image URL",
                          validators=[Required(), URL()])
    phone = StringField('Phone', validators=[Required(), Length(1, 20), ])
    submit = SubmitField('Submit')
