import random
import string


def main():
    v_sets = generate_vocab_sets(n=5)
    q_sets = generate_question_sets(vocab_sets=v_sets, mode=0)
    title = q_sets[0]
    questions = q_sets[1]

    print(title)
    for q in questions:
        print(q)


def read_vocab_file(show_kanji: bool) -> list:
    with open('N5_vocab.txt', 'r', encoding='utf-8') as file:
        next(file)  # We omit the header line
        data: list = []
        for line in file.readlines():
            split_vocab = line.rstrip().split(sep='\t', maxsplit=2)
            if show_kanji:
                data.append((split_vocab[0], split_vocab[1], split_vocab[2]))
            else:
                data.append((split_vocab[1], split_vocab[2]))
    return data


def generate_vocab_sets(n: int) -> list:
    if n <= 0:
        raise ValueError("'n' value must be positive")

    available_sets = read_vocab_file(show_kanji=False)
    return random.choices(available_sets, k=n)


def generate_question_sets(vocab_sets: list, mode: int = 1 or 2) -> tuple:
    """
    :param mode: [0] Hiragana -> English | [1] English -> Hiragana
    :param vocab_sets: [(Kanji, Hiragana, English), (...)]
    """
    if len(vocab_sets) > 26:
        raise ValueError('You can use max of 26 vocabulary sets at once')

    question_sets = []
    q_letters = list(string.ascii_lowercase)

    params = ('Translate to English', 0) if mode == 0 else ('Write in Kana', 1)

    for index, vocab_set in enumerate(vocab_sets):
        question = f'{q_letters[index]}) {vocab_set[params[1]]}'
        question_sets.append(question)

    return params[0], question_sets


if __name__ == '__main__':
    main()
