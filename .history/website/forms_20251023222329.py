from flask_wtf import FlaskForm
from wtforms import (
    StringField, PasswordField, SubmitField, TextAreaField,
    SelectField, DateField, TimeField, FileField, IntegerField
)
from wtforms.validators import InputRequired, Length, Email, EqualTo, DataRequired, Optional, NumberRange
from flask_wtf.file import FileAllowed

# ---------- LOGIN FORM ----------
class LoginForm(FlaskForm):
    user_name = StringField("User Name", validators=[InputRequired("Enter user name")])
    password = PasswordField("Password", validators=[InputRequired("Enter user password")])
    submit = SubmitField("Login")

# ---------- REGISTER FORM ----------
class RegisterForm(FlaskForm):
    user_name = StringField(
        "User Name", 
        validators=[
            InputRequired("Username is required"),
            Length(min=3, max=20, message="Username must be between 3 and 20 characters"),
        ]
    )
    email = StringField(
        "Email Address", 
        validators=[
            InputRequired("Email is required"),
            Email("Please enter a valid email address"),
            Length(max=120, message="Email must be less than 120 characters")
        ]
    )
    password = PasswordField(
        "Password",
        validators=[
            InputRequired("Password is required"),
            Length(min=8, max=128, message="Password must be between 8 and 128 characters"),
            EqualTo("confirm", message="Passwords must match")
        ],
    )
    confirm = PasswordField(
        "Confirm Password",
        validators=[InputRequired("Please confirm your password")]
    )
    submit = SubmitField("Register")

# ---------- EVENT FORM ----------
class EventForm(FlaskForm):
    title = StringField("Tournament Title", validators=[InputRequired(), Length(max=140)])

    # Tier / Category
    category = SelectField(
        "Category / Tier",
        choices=[
            ("", "Select tier..."),
            ("Community", "Community"),
            ("Amateur", "Amateur"),
            ("College", "College/Student"),
            ("Pro", "Professional"),
        ],
        validators=[InputRequired()],
    )

    # Venue / Region 
    region = SelectField(
        "Venue / Server Region",
        choices=[
            ("OCE", "OCE — Oceania"),
            ("NA-Central", "NA-Central"),
            ("NA-East", "NA-East"),
            ("EU", "EU — Europe"),
            ("ASIA", "ASIA"),
            ("LAN", "LAN / In-person"),
        ],
        validators=[InputRequired()],
    )

    # Split date/time like the reference
    date = DateField("Date", format="%Y-%m-%d", validators=[InputRequired()])
    time = TimeField("Start Time", format="%H:%M", validators=[InputRequired()])

    team_size = SelectField(
        "Team Size",
        choices=[("Solo", "Solo"), ("Duo", "Duo"), ("Trio", "Trio"), ("Squad", "Squad")],
        validators=[InputRequired()],
    )
    mode = SelectField(
        "Game Mode",
        choices=[("Battle Royale", "Battle Royale"), ("Zero Build", "Zero Build"), ("Reload", "Reload"), ("Creative", "Creative")],
        validators=[InputRequired()],
    )

    prize = StringField("Prize Pool", validators=[Optional(), Length(max=64)])

    description = TextAreaField("Description & Format", validators=[Length(max=2000)])

    # Banner (either upload or URL)
    banner_url = StringField("Banner Image URL", validators=[Optional(), Length(max=255)])
    banner_upload = FileField("Or Upload Banner", validators=[FileAllowed(["jpg", "jpeg", "png"], "Images only!")])

    submit = SubmitField("Save Tournament")

class BookingForm(FlaskForm):
    quantity = IntegerField('Quantity', validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField('Confirm Booking')
