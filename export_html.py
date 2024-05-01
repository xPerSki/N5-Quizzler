import random


class Export:
    def __init__(self, header: str, questions: list):
        self.header = header
        self.questions = questions

    def create_html(self):
        idx = random.randint(1, 9999)
        with open(f'htmlexport{idx}.html', 'w') as html:
            html.write(f'{self.header}\n\n')
            for q in self.questions:
                html.write(f'{q} = ')
