import sys
import docs_maker_messages as dm

from docs_maker_gui.classes.PageSwitcher import PageSwitcher

from PySide6.QtWidgets import QApplication, QMainWindow
from docs_maker_gui.ui.docs_maker_main_window import Ui_MainWindow
from docs_maker_gui.classes.TextSetter import TextSetter


class DocsMakerMainWindow(QMainWindow):
    def __init__(self):
        super(DocsMakerMainWindow, self).__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.pageSwitcher = PageSwitcher(self.ui)
        self.initializeUi()

    def initializeUi(self):
        self.ui.mainStacked_sw.setCurrentWidget(self.ui.mainPage_stPage)
        self.ui.main_btn.clicked.connect(self.pageSwitcher.setMainPage)
        self.ui.menu_btn.clicked.connect(self.pageSwitcher.setMenuPage)

    def setLanguage(self, lang_code):
        l = dm.set_language(lang_code)
        self.setWindowTitle(l.gettext('App Title'))
        TextSetter(self.ui).textSetter(l)

def docsMakerRun():
    app = QApplication(sys.argv)
    window = DocsMakerMainWindow()
    window.setLanguage('ru')
    window.show()
    sys.exit(app.exec())
