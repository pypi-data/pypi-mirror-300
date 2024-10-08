import sys
import docs_maker_messages as dm

from docs_maker_gui.classes.PageSwitcher import PageSwitcher

from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox
from docs_maker_gui.ui.docs_maker_main_window import Ui_MainWindow
from docs_maker_gui.classes.LangSwitcher import LangSwitcher
from docs_maker_gui.classes.SetUpWidgets import SetUpWidgets


class DocsMakerMainWindow(QMainWindow):
    def __init__(self):
        super(DocsMakerMainWindow, self).__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.pageSwitcher = PageSwitcher(self.ui)
        self.setUpWidgets = SetUpWidgets(self.ui, self)
        self.setLanguage('ru')
        self.initializeUi()

    def initializeUi(self):
        self.ui.mainStacked_sw.setCurrentWidget(self.ui.mainPage_stPage)
        self.ui.main_btn.clicked.connect(self.pageSwitcher.setMainPage)
        self.ui.menu_btn.clicked.connect(self.pageSwitcher.setMenuPage)
        self.ui.menuDb_cbx.currentIndexChanged.connect(self.setUpWidgets.onMenuDbOnChange)
        self.ui.menuDb_cbx.setCurrentText('SQLite3')
        self.setUpWidgets.onMenuDbOnChange(self.ui.menuDb_cbx.currentIndex())
        self.ui.menuApply_btn.clicked.connect(self.setUpWidgets.applyBtn)

    def setLanguage(self, lang_code):
        self.l = dm.set_language(lang_code)
        self.setUpWidgets.l = self.l
        self.setWindowTitle(self.l.gettext('App Title'))
        LangSwitcher(self.ui).translateSetter(self.l)

def docsMakerRun():
    app = QApplication(sys.argv)
    window = DocsMakerMainWindow()
    window.show()
    sys.exit(app.exec())
