import random
import argparse
import export_html


max_vocab: int


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('-n', '--number', type=int,
                        help=f'Number of questions to generate (1-100)', default=5)
    parser.add_argument('-m', '--mode', type=int, default=0,
                        help='[0] Kana -> English | [1] English -> Kana | [2] Kanji -> Kana | [3] Kanji -> English')
    parser.add_argument('-e', '--export',
                        help='Export result in html file', action='store_true')
    parser.add_argument('-oh', '--only-hiragana',
                        help='Generate only hiragana words', action='store_true')
    parser.add_argument('-d', '--dark',
                        help='Black background with white text', action='store_true')

    args = parser.parse_args()

    v_sets = generate_vocab_sets(n=args.number, omit_empty=True if args.mode in [2, 3] else False,
                                 only_hiragana=args.only_hiragana)
    q_sets = generate_question_sets(vocab_sets=v_sets, mode=args.mode)
    title = q_sets[0]
    questions = q_sets[1]

    if args.export:
        create_html_questions(header=title.split('\n')[1], questions=questions, dark_mode=args.dark)
        create_html_answers()
    else:
        cli_display_questions(title, questions)
        input('\nPress ENTER to show the answers')
        for i in range(len(questions)):
            questions[i] = questions[i][3:]
        answers: dict = cli_display_answers(questions, mode=args.mode)

        for i, (k, v) in enumerate(answers.items()):
            print(f'{i+1}) {k}  ->  {v[:-2]}')


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


def create_html_questions(header: str, questions: list, dark_mode: bool = False) -> None:
    html_data = export_html.Export(header, questions, dark_mode)
    html_data.create_html()


def create_html_answers() -> None:
    pass


def cli_display_questions(title, questions: list) -> None:
    print(title)
    for q in questions:
        print(q)


def cli_display_answers(questions: list, mode: int) -> dict:
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
    del data, data_answer

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


if __name__ == '__main__':
    main()
