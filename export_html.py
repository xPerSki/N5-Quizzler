import random
from string import ascii_letters
import hook
import os


class Export:
    def __init__(self, header: str, questions: list, dark_mode: bool, mode: int):
        self.header = header
        self.questions = questions
        self.dark_mode = dark_mode
        self.mode = mode
        self.html_path = fr'exports/html'
        self.unique_id = random.choices(ascii_letters, k=random.randint(4, 7))
        self.filename = "".join(self.unique_id)

    def create_html(self):
        try:
            os.makedirs(self.html_path)
        except FileExistsError:
            pass

        self._create_css()
        with open(fr'{self.html_path}/htmlexport_{self.filename}.html', 'w', encoding='utf-8') as html:
            lines = [
                '<link rel="stylesheet" href="styles.css">\n',
                f'<h1>{self.header}</h1>\n'
            ]
            html.writelines(lines)
            for q in self.questions:
                html.write(f'<p>{q} = </p>\n')

    def create_answers(self):
        with open(fr'{self.html_path}/htmlexport_{self.filename}_AnswerKey.html', 'w', encoding='utf-8') as html:
            lines = [
                '<link rel="stylesheet" href="styles.css">\n',
                f'<h1>{self.header}</h1>\n'
            ]
            html.writelines(lines)

            answers = hook.generate_answers(self.questions, self.mode, q_slice=True)
            for i, (k, v) in enumerate(answers.items()):
                html.write(f'<p>{i+1}) {k} = {v[:-2]}</p>\n')

    def _create_css(self):
        colors = ('black', 'white') if self.dark_mode else ('white', 'black')
        with open(fr'{self.html_path}/styles.css', 'w') as css:
            lines: list = [
                f'* {{background-color: {colors[0]}; color: {colors[1]};}}\n',
                'h1 {font-size: 50px; text-align: center;}\n',
                'p {padding-top: 40px; font-size: 18px;}\n'
            ]
            css.writelines(lines)
