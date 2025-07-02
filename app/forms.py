from flask_wtf import FlaskForm
from wtforms import BooleanField, SelectField, StringField, SubmitField
from wtforms.validators import DataRequired

characters = [
    "Any",
    "Sol",
    "Ky",
    "May",
    "Millia",
    "Zato-1",
    "Potemkin",
    "Chipp",
    "Faust",
    "Axl",
    "Venom",
    "Slayer",
    "I-No",
    "Bedman",
    "Ramlethal",
    "Sin",
    "Elphelt",
    "Leo",
    "Johnny",
    "Jack-O",
    "Jam",
    "Haehyun",
    "Raven",
    "Dizzy",
    "Baiken",
    "Answer",
]


class VodSubmitForm(FlaskForm):
    p1name = StringField("Player1", validators=[DataRequired()])
    p2name = StringField("Player2", validators=[DataRequired()])
    p2character = SelectField("Enemy Character", choices=characters[1:])
    link = StringField("Match Link", validators=[DataRequired()])
    source = StringField("Link Source")
    submit = SubmitField("Submit VOD")


class VodSearchForm(FlaskForm):
    p1name = StringField("Player1")
    p2name = StringField("Player2")
    p2character = SelectField("Enemy Character", choices=characters, default="Any")
    verifiedonly = BooleanField("Verified Only")
    submit = SubmitField("Search")
