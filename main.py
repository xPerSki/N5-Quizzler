import random
import argparse


max_vocab: int


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('-n', '--number', type=int, help=f'Number of questions to generate (1-100)', default=5)
    parser.add_argument('-m', '--mode', type=int, help='[0] Kana -> English | [1] English -> Kana | [2] Kanji -> Kana | [3] Kanji -> English', default=0)

    args = parser.parse_args()

    v_sets = generate_vocab_sets(n=args.number, omit_empty=True if args.mode in [2, 3] else False)
    q_sets = generate_question_sets(vocab_sets=v_sets, mode=args.mode)
    title = q_sets[0]
    questions = q_sets[1]

    print(title)
    for q in questions:
        print(q)


def read_vocab_file(omit_empty: bool = False) -> list:
    with open('N5_vocab.txt', 'r', encoding='utf-8') as file:
        next(file)  # We omit the header line
        data: list = []
        for line in file.readlines():
            split_vocab: list = line.rstrip().split(sep='\t', maxsplit=2)
            if omit_empty:
                if split_vocab[0] == '':
                    continue

            data.append((split_vocab[0], split_vocab[1], split_vocab[2]))

    return data


def generate_vocab_sets(n: int, omit_empty: bool) -> list:
    if n <= 0:
        raise ValueError("'n' value must be positive")
    elif n > 100:
        raise ValueError(f"Max value of 'n' is 100")

    available_sets = read_vocab_file(omit_empty)
    return random.choices(available_sets, k=n)


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


if __name__ == '__main__':
    main()
