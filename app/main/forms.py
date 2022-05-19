from wtforms import TextAreaField,SubmitField,SelectField
from wtforms.validators import InputRequired
from flask_wtf import FlaskForm


class UpdateProfile(FlaskForm):
    bio = TextAreaField('Tell us about you.',validators = [InputRequired()])
    submit = SubmitField('Submit')

class PitchForm(FlaskForm):
    category = SelectField('Pitch category',choices=[('Promotion','Promotion'),('Interview','Interview'),('Product','Product'),('Business','Business')],validators = [InputRequired()])
    pitch_title = TextAreaField('Pitch title',validators = [InputRequired()])
    content = TextAreaField('Pitch content',validators = [InputRequired()])
    
    submit = SubmitField('Submit')

class CommentForm(FlaskForm):
    comment = TextAreaField('What do you think?',validators = [InputRequired()])
    submit = SubmitField('Submit')