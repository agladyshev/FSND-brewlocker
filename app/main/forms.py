from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import Required, Length, URL
from wtforms import ValidationError
from .. import images


class ItemForm(FlaskForm):
    header = StringField("Your pitch here", validators=[Required()])
    body = TextAreaField("Tell me everything", validators=[Required()])
    img = FileField('image', validators=[FileAllowed(images, 'Images only!')])
    phone = StringField('Phone', validators=[Required(), Length(1, 20), ])
    submit = SubmitField('Submit')

    # def allowed_file(self, filename):
    #     ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
    # return '.' in filename and \
    #        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS