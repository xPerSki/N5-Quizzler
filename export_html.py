import random
from string import ascii_letters
import os


class Export:
    def __init__(self, header: str, questions: list):
        self.header = header
        self.questions = questions
        self.html_path = fr'exports/html'
        self.unique_id = random.choices(ascii_letters, k=random.randint(4, 7))
        self.filename = "".join(self.unique_id)

    def create_html(self):
        try:
            os.makedirs(self.html_path)
        except FileExistsError:
            pass

        self.create_css()
        with open(fr'{self.html_path}/htmlexport_{self.filename}.html', 'w', encoding='utf-8') as html:
            lines = [
                '<link rel="stylesheet" href="styles.css">\n',
                f'<h1>{self.header}</h1>\n'
            ]
            html.writelines(lines)
            for q in self.questions:
                html.write(f'<p>{q} = </p>\n')

    def create_css(self):
        with open(fr'{self.html_path}/styles.css', 'w') as css:
            lines: list = [
                '* {background-color: black; color: white;}\n',
                'h1 {font-size: 60px; text-align: center;}\n',
                'p {padding-top: 50px; font-size: 20px;}\n'
            ]
            css.writelines(lines)