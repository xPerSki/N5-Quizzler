import random
import export_html


def read_vocab_file(omit_empty: bool = False, only_hiragana: bool = False) -> list:
    with open('N5_vocab.txt', 'r', encoding='utf-8') as file:
        next(file)  # We omit the header line
        data: list = []
        for line in file.readlines():
            split_vocab: list = line.rstrip().split(sep='\t', maxsplit=2)
            if omit_empty:
                if split_vocab[0] == '':
                    continue

            if only_hiragana:
                if not check_only_hiragana(split_vocab[1]):
                    continue

            data.append((split_vocab[0], split_vocab[1], split_vocab[2]))

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


def generate_html_questions_and_answers(header: str, questions: list, dark_mode: bool = False, mode: int = -1) -> None:
    html_data = export_html.Export(header, questions, dark_mode, mode)
    html_data.create_html()
    html_data.create_answers()


def cli_display_questions(title, questions: list) -> None:
    print(title)
    for q in questions:
        print(q)


def generate_answers(questions: list, mode: int, q_slice: bool = False) -> dict:
    if q_slice:
        for i in range(len(questions)):
            # Delete the 1), 2), etc.
            questions[i] = questions[i].split(' ', 1)[1]

    data: list = read_vocab_file()
    sliced_data: list = []
    search_idx: int = -1
    answer_idx: int = -1
    answers: dict = {}
    for q in questions:
        answers[q] = ''
        for data_answer in data:
            if q in data_answer:
                sliced_data.append(data_answer)
    del data, data_answer, i

    # (0, 1, 2) -> (Kanji, Kana, English)
    if mode == 0:
        search_idx = 1  # We search for Kana
        answer_idx = 2  # We search for English Translation
    elif mode == 1:
        search_idx = 2
        answer_idx = 1
    elif mode == 2:
        search_idx = 0
        answer_idx = 1
    elif mode == 3:
        search_idx = 0
        answer_idx = 2

    for question in questions:
        for data_answer in sliced_data:
            if question == data_answer[search_idx]:
                answers[question] += data_answer[answer_idx] + ', '

    return answers
