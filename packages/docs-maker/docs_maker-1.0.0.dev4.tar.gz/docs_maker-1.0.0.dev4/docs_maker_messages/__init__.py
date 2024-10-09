import gettext
import os

current_dir = os.path.dirname(os.path.abspath(__file__))

def set_language(lang_code: str):
    tr = gettext.translation('messages', localedir=current_dir, languages=[lang_code])
    tr.install()

    return tr
