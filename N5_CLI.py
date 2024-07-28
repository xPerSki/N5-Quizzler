import argparse
import hook

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

    v_sets = hook.generate_vocab_sets(n=args.number, omit_empty=True if args.mode in [2, 3] else False,
                                      only_hiragana=args.only_hiragana)
    q_sets = hook.generate_question_sets(vocab_sets=v_sets, mode=args.mode)
    title = q_sets[0]
    questions = q_sets[1]

    if args.export:
        hook.generate_html_questions_and_answers(header=title.split('\n')[1], questions=questions,
                                                 dark_mode=args.dark, mode=args.mode)
    else:
        hook.cli_display_questions(title, questions)
        input('\nPress ENTER to show the answers')
        answers: dict = hook.generate_answers(questions, mode=args.mode, q_slice=True)

        for i, (k, v) in enumerate(answers.items()):
            print(f'{i+1}) {k}  ->  {v[:-2]}')


if __name__ == '__main__':
    main()
