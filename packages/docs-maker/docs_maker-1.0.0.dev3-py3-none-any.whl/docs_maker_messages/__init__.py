import gettext
import os

current_dir = os.path.dirname(os.path.abspath(__file__))

def set_language(lang_code: str):
    lang = gettext.translation('messages', localedir=current_dir, languages=[lang_code])
    lang.install()

    return lang
