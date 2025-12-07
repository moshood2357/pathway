from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,PasswordField,BooleanField, SelectField, TextAreaField, DecimalField
from wtforms.validators import Email, EqualTo, Length, DataRequired, NumberRange, Optional, URL


class RegistrationForm(FlaskForm):
    name = StringField(
        'Name',
        validators=[
            DataRequired(message="Please enter your full name."),
            Length(min=2, max=20, message="Name must be between 2 and 20 characters.")
        ]
    )

    email = StringField(
        'Email',
        validators=[
            DataRequired(message="Please provide your email address."),
            Email(message="Please enter a valid email address.")
        ]
    )

    password = PasswordField(
        'Password',
        validators=[
            DataRequired(message="Please create a password."),
            Length(min=6, message="Password must be at least 6 characters long.")
        ]
    )

    confirm_password = PasswordField(
        'Confirm Password',
        validators=[
            DataRequired(message="Please confirm your password."),
            EqualTo('password', message="Passwords do not match.")
        ]
    )

    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    email = StringField('Email',  validators=[DataRequired(),Email()])
    password = PasswordField('Password', validators =[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Login')



class ResetForm(FlaskForm):
    email = StringField('Email',  validators=[DataRequired(),Email()])
    submit = SubmitField('Submit')
    
class OtpForm(FlaskForm):
    email = StringField('OTP',  validators=[DataRequired()])
    submit = SubmitField('Submit')

class ResetPasswordForm(FlaskForm):
    email = StringField('OTP',  validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired(message="Please create a password."),Length(min=6, message="Password must be at least 6 characters long.")])
    confirm_password = PasswordField('Confirm Password',validators=[DataRequired(message="Please confirm your password."),EqualTo('password', message="Passwords do not match.")])
    submit = SubmitField('Submit')
    
class Question1(FlaskForm):
    currentrole = StringField('Current role')
    submit = SubmitField('Next')

class Question2(FlaskForm):
    currentlevel = StringField('Current level')
    submit = SubmitField('Next')


class Question4(FlaskForm):
    careergoal = StringField('Career goal')
    submit = SubmitField('Next')


class AddSkillForm(FlaskForm):
    skill_name = StringField('Skill Name', validators=[DataRequired()])
    category = SelectField('Category', choices=[('Technical','Technical'), ('Soft','Soft'), ('Other','Other')])
    submit = SubmitField('Add Skill')


class CareerForm(FlaskForm):
    career_name = StringField(
        "Career Name",
        validators=[
            DataRequired(),
            Length(min=2, max=100)
        ]
    )

    description = TextAreaField(
        "Description",
        validators=[
            DataRequired(),
            Length(min=10)
        ]
    )

    demand_level = SelectField(
        "Demand Level",
        choices=[
            ("High", "High"),
            ("Medium", "Medium"),
            ("Low", "Low")
        ],
        validators=[DataRequired()]
    )

    average_salary = DecimalField(
        "Average Salary (₦)",
        places=2,
        rounding=None,
        validators=[
            Optional(),
            NumberRange(min=0, message="Salary must be a positive number.")
        ]
    )

    submit = SubmitField("Save Career")


class ProfessionalForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    linkedin_id = StringField('LinkedIn ID')
    career_id = SelectField('Career', choices=[],coerce=int)
    submit = SubmitField('Submit')





class CommunityForm(FlaskForm):
    community_name = StringField(
        'Community Name',
        validators=[DataRequired()]
    )

    description = TextAreaField(
        'Description',
        validators=[Optional()]
    )

    career_id = SelectField(
        'Related Career',
        coerce=int,
        validators=[DataRequired()]
    )

    community_link = StringField(
    'Community Link',
    validators=[Optional(strip_whitespace=True), URL(require_tld=False, message="Please enter a valid URL")]
)

    submit = SubmitField('Add Community')
