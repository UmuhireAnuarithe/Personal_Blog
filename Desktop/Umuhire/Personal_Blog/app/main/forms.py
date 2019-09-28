
from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField,SelectField
from wtforms.validators import Required,Email,ValidationError
from wtforms import ValidationError
from ..models import Subscription


class BlogForm(FlaskForm):
    title = StringField('Title', validators = [Required()])
    text = TextAreaField('Blog',validators = [Required()])
    submit = SubmitField('Submit')

class UpdateProfile(FlaskForm):
    bio = TextAreaField('Tell us about you', validators = [Required()])
    submit = SubmitField('Submit')

class CommentForm(FlaskForm):
    text = TextAreaField('Add a Comment',validators = [Required()])
    submit = SubmitField('Submit Comment')

class SubscribeForm(FlaskForm):
    email = StringField('Email address', validators=[Required(), Email()])
    submit = SubmitField('Subscribe')

    def validate_email(self, email):
        email = Subscription.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError('That email is already subscribed .')