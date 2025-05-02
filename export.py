import random
from string import ascii_letters
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.colors import Color
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from settings import *
import hook
import os


class Export:
    def __init__(self, header: str, questions: list, dark_mode: bool, mode: int):
        self.header = header
        self.questions = questions
        self.dark_mode = dark_mode
        self.mode = mode

        os.makedirs(EXPORT_PATH, exist_ok=True)

        _unique_id = random.choices(ascii_letters, k=random.randint(4, 7))
        self.filename = "".join(_unique_id)

    def create_questions_pdf(self):
        c = canvas.Canvas(f"{EXPORT_PATH}Quiz-{self.filename}.pdf", pagesize=A4)
        width, height = A4
        y = height - 3 * cm

        pdfmetrics.registerFont(TTFont(FONT_NAME, FONT_PATH))

        c.drawImage(BACKGROUND, 0, 0, width=width, height=height)
        c.setFillColor(Color(0, 0, 0))
        c.setFont(FONT_NAME, HEADER_FONT_SIZE)
        c.drawCentredString(width/2, height - 2 * cm, self.header)

        y -= 2 * cm

        c.setFont(FONT_NAME, CONTENT_FONT_SIZE)
        for i, question in enumerate(self.questions, 1):
            if y < cm:
                c.showPage()
                c.drawImage(BACKGROUND, 0, 0, width=width, height=height)
                c.setFillColor(Color(0, 0, 0))
                c.setFont(FONT_NAME, CONTENT_FONT_SIZE)
                y = height - 2 * cm

            c.drawString(2 * cm, y, f"{question}")
            y -= cm

        c.save()
        return self.filename

    def create_answerkey_pdf(self):
        answers = hook.generate_answers(self.questions, self.mode, q_slice=True)

        c = canvas.Canvas(f"{EXPORT_PATH}Quiz-{self.filename}-answers.pdf", pagesize=A4)
        width, height = A4
        y = height - 3 * cm

        pdfmetrics.registerFont(TTFont(FONT_NAME, FONT_PATH))

        c.drawImage(BACKGROUND, 0, 0, width=width, height=height)
        c.setFillColor(Color(0, 0, 0))
        c.setFont(FONT_NAME, HEADER_FONT_SIZE)
        c.drawCentredString(width/2, height - 2 * cm, self.header + " - Answers")

        y -= 2 * cm

        c.setFont(FONT_NAME, CONTENT_FONT_SIZE)
        for i, (question, answer) in enumerate(answers.items(), 1):
            if y < cm:
                c.showPage()
                c.drawImage(BACKGROUND, 0, 0, width=width, height=height)
                c.setFillColor(Color(0, 0, 0))
                c.setFont(FONT_NAME, CONTENT_FONT_SIZE)
                y = height - 2 * cm

            c.drawString(2 * cm, y, f"{i}) {question} -> {answer}")
            y -= cm

        c.save()
        return self.filename
