from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField, DateTimeLocalField
from wtforms.validators import InputRequired, Length, Email, EqualTo, DataRequired

# ---------- LOGIN FORM ----------
class LoginForm(FlaskForm):
    user_name = StringField("User Name", validators=[InputRequired("Enter user name")])
    password = PasswordField("Password", validators=[InputRequired("Enter user password")])
    submit = SubmitField("Login")


# ---------- REGISTER FORM ----------
class RegisterForm(FlaskForm):
    user_name = StringField("User Name", validators=[InputRequired()])
    email = StringField("Email Address", validators=[Email("Please enter a valid email")])
    password = PasswordField(
        "Password",
        validators=[InputRequired(), EqualTo("confirm", message="Passwords should match")],
    )
    confirm = PasswordField("Confirm Password")
    submit = SubmitField("Register")


# ---------- EVENT FORM ----------
class EventForm(FlaskForm):
    title = StringField("Event Name", validators=[InputRequired(), Length(max=140)])
    region = StringField("Server Region", validators=[Length(max=64)])
    team_size = SelectField(
        "Team Size",
        choices=[("Solo", "Solo"), ("Duo", "Duo"), ("Trio", "Trio"), ("Squad", "Squad")],
        validators=[DataRequired()],
    )
    mode = StringField("Game Mode", validators=[Length(max=64)])
    prize = StringField("Prize Pool", validators=[Length(max=64)])
    start_at = DateTimeLocalField(
        "Start Date & Time",
        format="%Y-%m-%dT%H:%M",
        validators=[DataRequired()],
        description="Enter date and time in local format (YYYY-MM-DDTHH:MM)",
    )
    description = TextAreaField("Description / Rules", validators=[Length(max=2000)])
    submit = SubmitField("Create Tournament")
