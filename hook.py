import random
import export
from app import Word, app


def read_vocab_file(omit_empty: bool = False, only_hiragana: bool = False) -> list:
    with app.app_context():
        all_words = Word.query.all()

    data = []
    for word in all_words:
        if omit_empty:
            if word.kanji == '':
                continue

        if only_hiragana:
            if not check_only_hiragana(word.kana):
                continue

        data.append((word.kanji, word.kana, word.english))

    return data


def generate_vocab_sets(n: int, omit_empty: bool, only_hiragana: bool) -> list:
    if n <= 0:
        raise ValueError("'n' value must be positive")
    elif n > 100:
        raise ValueError(f"Max value of 'n' is 100")

    available_sets = read_vocab_file(omit_empty, only_hiragana)
    return random.sample(available_sets, k=n)


def generate_question_sets(vocab_sets: list, mode: int = 0) -> tuple:
    # Check if the provided mode is valid
    valid_modes: tuple = (0, 1, 2, 3)
    if mode not in valid_modes:
        raise ValueError(f'No such mode as [{mode}]')

    question_sets: list = []
    params: tuple = ()

    match mode:
        case 0:
            params = ('Kana -> English\nTranslate to English\n', 1)
        case 1:
            params = ('English -> Kana\nWrite in Kana\n', 2)
        case 2:
            params = ('Kanji -> Kana\nWrite in Kana\n', 0)
        case 3:
            params = ('Kanji -> English\nTranslate to English\n', 0)

    for index, vocab_set in enumerate(vocab_sets):
        question: str = f'{index + 1}) {vocab_set[params[1]]}'
        question_sets.append(question)

    return params[0], question_sets


def check_only_hiragana(word) -> bool:
    katakana_chars = ('アァカサタナハマヤャラワガザダバパピビヂジギヰリミヒニチシキィイウゥクスツヌフムユ'
                      'ュルグズヅブプペベデゼゲヱレメヘネテセケェエオォコソトノホモヨョロヲゴゾドボポヴッン')
    for ltr in word:
        if ltr in katakana_chars:
            return False
    return True


def generate_pdf_questions_and_answers(header: str, questions: list, dark_mode: bool = False, mode: int = -1) -> None:
    data = export.Export(header, questions, dark_mode, mode)
    data.create_questions_pdf()
    data.create_answerkey_pdf()


def cli_display_questions(title, questions: list) -> None:
    print(title)
    for q in questions:
        print(q)


def generate_answers(questions: list, mode: int, q_slice: bool = False) -> dict:
    # Delete the 1), 2), etc.
    if q_slice:
        questions = [q.split(' ', 1)[1] for q in questions]

    data: list = read_vocab_file()
    answers: dict = {q: '' for q in questions}

    # mode: (0, 1, 2) -> mode: (Kanji, Kana, English)
    mode_search = {
        0: (1, 2),
        1: (2, 1),
        2: (0, 1),
        3: (0, 2)
    }
    search_idx, answer_idx = mode_search[mode]

    answer_dict = {}
    for entry in data:
        key = entry[search_idx]
        value = entry[answer_idx]
        if key in answer_dict:
            answer_dict[key] += ', ' + value
        else:
            answer_dict[key] = value

    # Match questions with their answers
    for question in questions:
        if question in answer_dict:
            answers[question] = answer_dict[question]

    return answers
