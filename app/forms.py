from flask_wtf import FlaskForm
from wtforms import BooleanField, SelectField, StringField, SubmitField
from wtforms.validators import DataRequired, Optional

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
    p2character = SelectField(
        "Enemy Character", choices=characters[1:], validators=[DataRequired()]
    )
    link = StringField("Match Link", validators=[DataRequired()])
    source = StringField("Optional Link Source", validators=[Optional()])
    submit = SubmitField("Submit VOD")


class VodSearchForm(FlaskForm):
    p1name = StringField("Player1", validators=[Optional()])
    p2name = StringField("Player2", validators=[Optional()])
    p2character = SelectField(
        "Enemy Character",
        choices=characters,
        default="Any",
        validators=[DataRequired()],
    )
    verifiedonly = BooleanField("Verified Only")
    submit = SubmitField("Search")
