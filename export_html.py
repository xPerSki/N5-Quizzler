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
        self.HTML_LINES = [
            '<!DOCTYPE html>\n',
            '<head>\n',
            '<meta charset="UTF-8">\n',
            '<meta name="viewport" content="width=device-width, initial-scale=1.0">\n',
            '<title>N5 Quizzler</title>\n',
            '<link rel="stylesheet" href="styles.css">\n',
            '</head>\n',
            '<body>\n',
            '<div class="quiz-container">\n',
            f'<h1>{self.header}</h1>\n',
        ]

    def create_html(self):
        try:
            os.makedirs(self.html_path)
        except FileExistsError:
            pass

        self._create_css()
        with open(fr'{self.html_path}/htmlexport_{self.filename}.html', 'w', encoding='utf-8') as html:
            html.writelines(self.HTML_LINES)
            for q in self.questions:
                html.write(f'<div class="question">{q} = </div>\n')
            html.write('</div>\n</body>\n</html>')

    def create_answers(self):
        with open(fr'{self.html_path}/htmlexport_{self.filename}_AnswerKey.html', 'w', encoding='utf-8') as html:
            html.writelines(self.HTML_LINES)

            answers = hook.generate_answers(self.questions, self.mode, q_slice=True)
            for i, (k, v) in enumerate(answers.items()):
                html.write(f'<div class="question">{i+1}) {k} = {v}</div>\n')
            html.write('</div>\n</body>\n</html>')

    def _create_css(self):
        colors = ('#212529', '#fff') if self.dark_mode else ('#fff', '#212529')
        with open(fr'{self.html_path}/styles.css', 'w') as css:
            lines = [
                '@import url("https://fonts.googleapis.com/css2?family=Josefin+Sans:ital,wght@0,100..700;1,100..700&family=Noto+Serif+JP:wght@200..900&display=swap");\n',
                f'* {{background-color: {colors[0]}; color: {colors[1]}; font-family: "Noto Serif JP", serif; font-weight: 400;}}\n',
                'h1 {font-size: 50px; text-align: center; margin-bottom: 30px;}\n',
                '.quiz-container {max-width: 800px; margin: auto;}\n',
                '.question {font-size: 24px; margin-top: 30px;}\n',
            ]
            css.writelines(lines)
