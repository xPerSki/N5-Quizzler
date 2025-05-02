from os import getenv

HEADER_FONT_SIZE = 24
CONTENT_FONT_SIZE = 14
FONT_NAME = "NotoSansJP"
FONT_PATH = "fonts/NotoSerifJP.ttf"
BACKGROUND = "static/img/pdf-rose-small.png"
EXPORT_PATH = fr'export/'
LOCAL_DEPLOY: bool = getenv("LOCAL_DEPLOY", "0") == "1"
