from flask import Flask, render_template, url_for, redirect, request
from wtforms import StringField, PasswordField, EmailField, SubmitField
from wtforms.validators import DataRequired, Length, Email
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from sqlalchemy import Integer, Float, String
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
import hook


class SimpleAnswerForm(FlaskForm):
    answer = StringField("Answer", validators=[DataRequired()])
    submit = SubmitField("Check")


class Base(DeclarativeBase):
    pass


app = Flask(__name__)
app.secret_key = "xxxxxxxxxx"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///N5_vocab.db"
db = SQLAlchemy(model_class=Base)
db.init_app(app)
bootstrap = Bootstrap5(app)


class Word(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    kanji: Mapped[str] = mapped_column(String(250), unique=False, nullable=True)
    kana: Mapped[str] = mapped_column(String(250), unique=False, nullable=False)
    english: Mapped[str] = mapped_column(String(250), unique=False, nullable=False)


with app.app_context():
    db.create_all()


@app.route('/')
def home():
    return render_template('index.html')


@app.route("/hub")
def hub():
    return render_template('hub.html')


@app.route("/flashcards")
def flashcards():
    return ''


if __name__ == "__main__":
    app.run(debug=True)
