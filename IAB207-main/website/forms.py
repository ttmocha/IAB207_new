from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField, SubmitField, StringField, PasswordField
from wtforms.validators import InputRequired, Length, Email, EqualTo

# creates the login information
class LoginForm(FlaskForm):
    user_name=StringField("User Name", validators=[InputRequired('Enter user name')])
    password=PasswordField("Password", validators=[InputRequired('Enter user password')])
    submit = SubmitField("Login")

 # this is the registration form
class RegisterForm(FlaskForm):
    user_name=StringField("User Name", validators=[InputRequired()])
    email = StringField("Email Address", validators=[Email("Please enter a valid email")])
    # linking two fields - password should be equal to data entered in confirm
    password=PasswordField("Password", validators=[InputRequired(),
                  EqualTo('confirm', message="Passwords should match")])
    confirm = PasswordField("Confirm Password")

    # submit button
    submit = SubmitField("Register")

class EventForm(FlaskForm):
    title = StringField("Event Name", validators=[InputRequired(), Length(max=120)])
    image_url = StringField("Event Image (URL)", validators=[Length(max=300)])
    date = StringField("Date (YYYY-MM-DD)", validators=[InputRequired(), Length(max=20)])
    start_time = StringField("Start Time (HH:MM)", validators=[InputRequired(), Length(max=10)])
    end_time = StringField("End Time (HH:MM)", validators=[InputRequired(), Length(max=10)])
    server_region = StringField("Server Region", validators=[InputRequired(), Length(max=50)])
    team_size = StringField("Team Size (Solo/Duos/Trios/Squads)", validators=[InputRequired(), Length(max=20)])
    game_mode = StringField("Game Mode", validators=[Length(max=60)])
    buy_in = StringField("Buy In", validators=[Length(max=20)])
    prize = StringField("Prize Pool", validators=[Length(max=60)])
    match_code = StringField("Match Code / Epic ID", validators=[Length(max=60)])
    description = TextAreaField("Description / Rules", validators=[InputRequired(), Length(max=2000)])
    submit = SubmitField("Create Event")
    