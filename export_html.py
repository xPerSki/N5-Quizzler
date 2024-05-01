import random
from string import ascii_letters


class Export:
    def __init__(self, header: str, questions: list):
        self.header = header
        self.questions = questions

    def create_html(self):
        unique_id = random.choices(ascii_letters, k=random.randint(4, 7))
        with open(fr'exports/htmlexport_{"".join(unique_id)}.html', 'w', encoding='utf-8') as html:
            html.write(f'<h1>{self.header}</h1>\n')
            html.write('<br>\n')
            for q in self.questions:
                html.write(f'<p>{q} = </p>\n')
