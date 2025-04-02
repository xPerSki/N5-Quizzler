from flask import Flask, render_template, url_for, redirect, request, jsonify, flash
from wtforms import StringField, PasswordField, EmailField, SubmitField, SelectField, RadioField
from wtforms.validators import DataRequired, Length, Email
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from sqlalchemy import Integer, Float, String
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
import random
import os


class SimpleAnswerForm(FlaskForm):
    answer = StringField("Answer")
    submit = SubmitField("Check")


class Base(DeclarativeBase):
    pass


app = Flask(__name__)
app.secret_key = "xxxxxxxxxx"
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DB_URI", "sqlite:///N5_vocab.db")
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


@app.route("/flashcards/select")
def flashcards_choosing():
    return render_template('flashcards.html', fs="setup")


@app.route("/flashcards/<string:mode>")
def flashcards(mode):
    import hook
    if mode == "hiragana":
        data = hook.read_vocab_file(only_hiragana=True)
    else:
        data = hook.read_vocab_file()

    return render_template('flashcards.html', data=data)


@app.route("/get_random_question/<string:mode>")
def get_random_question(mode):
    import hook
    if mode == "hiragana":
        data = hook.read_vocab_file(only_hiragana=True)
    else:
        data = hook.read_vocab_file()

    question = random.choice(data)
    return jsonify(question)


NUMBER_OF_QUESTIONS = [i for i in range(1, 100+1)]
MODE = ["0. Kana -> English", "1. English -> Kana", "2. Kanji -> Kana", "3. Kanji -> English"]
KANA = ["Only Hiragana", "Hiragana & Katakana"]
THEME = ["Light Theme", "Dark Theme"]


class QuizForm(FlaskForm):
    number_of_questions = SelectField("Number of questions", validators=[DataRequired()], choices=NUMBER_OF_QUESTIONS)
    mode = SelectField("Mode", validators=[DataRequired()], choices=MODE)
    kana = RadioField("Kana", validators=[DataRequired()], choices=KANA)
    theme = RadioField("Theme", validators=[DataRequired()], choices=THEME)
    submit = SubmitField("Create Quiz")


@app.route("/quiz", methods=["POST", "GET"])
def quiz():
    import hook
    form = QuizForm()

    if form.validate_on_submit():
        n = int(form.number_of_questions.data)
        mode = MODE.index(form.mode.data)
        omit_empty = True if form.mode.data in ["2. Kanji -> Kana", "3. Kanji -> English"] else False
        only_hiragana = True if form.kana.data == "Only Hiragana" else False
        darkmode = True if form.theme.data == "Dark Theme" else False

        v_sets = hook.generate_vocab_sets(n, omit_empty, only_hiragana)
        q_sets = hook.generate_question_sets(vocab_sets=v_sets, mode=mode)

        title, questions = q_sets[0], q_sets[1]
        hook.generate_html_questions_and_answers(header=title.split('\n')[1], questions=questions, dark_mode=darkmode, mode=mode)
        return redirect(url_for('hub'))

    form.number_of_questions.data = "10"
    form.kana.data = "Only Hiragana"
    form.theme.data = "Light Theme"
    return render_template('quiz.html', form=form)


@app.route("/practice", methods=["POST", "GET"])
def practice():
    import hook
    form = SimpleAnswerForm()
    if request.method == 'POST' and form.validate_on_submit():
        submitted_answer = form.answer.data
        correct_answer = request.form.get('correct_answer')
        if submitted_answer.strip().lower() in correct_answer.lower().replace(',', '').replace('/', '').replace('(', '').replace(')', '').split():
            flash('Correct!', 'success')
        else:
            flash(f'Incorrect. The correct answer was: {correct_answer}.', 'danger')
        return redirect(url_for('practice'))

    word = random.choice(hook.read_vocab_file())
    if random.randint(0, 1) == 0:
        # Q: JP, A: ENG
        question, answer = word[1], word[2]
        if word[0]:
            question = f"{word[1]} ({word[0]})"
    else:
        # Q: ENG, A: JP
        question, answer = word[2], word[1]
        if word[0]:
            answer = f"{word[1]} ({word[0]})"

    return render_template('practice.html', form=form, question=question, answer=answer)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
