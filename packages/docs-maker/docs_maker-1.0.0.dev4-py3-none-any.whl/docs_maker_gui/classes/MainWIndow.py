import sys
import docs_maker_messages as dm
from docs_maker_gui.classes.PageSwitcher import PageSwitcher
from PySide6.QtWidgets import QApplication, QMainWindow
from docs_maker_gui.ui.docs_maker_main_window import Ui_MainWindow
from docs_maker_gui.classes.LangSwitcher import LangSwitcher
from docs_maker_gui.classes.SetUpWidgets import SetUpWidgets
from docs_maker_gui.classes.CRUD import Crud
from docs_maker_gui.classes.Configuration import Config


class DocsMakerMainWindow(QMainWindow):
    def __init__(self):
        super(DocsMakerMainWindow, self).__init__()

        self.dbSession = None
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.pageSwitcher = PageSwitcher(self.ui)
        self.setUpWidgets = SetUpWidgets(self.ui, self)
        self.setLanguage('ru')
        self.crud = Crud(self.ui)
        self.config = Config(self.ui)
        self.initializeUi()

    def initializeUi(self):
        self.ui.mainStacked_sw.setCurrentWidget(self.ui.mainPage_stPage)
        self.ui.main_btn.clicked.connect(self.pageSwitcher.setMainPage)
        self.ui.menu_btn.clicked.connect(self.pageSwitcher.setMenuPage)
        self.ui.menuDb_cbx.currentIndexChanged.connect(self.setUpWidgets.onMenuDbOnChange)
        self.ui.menuApply_btn.clicked.connect(self.setDbSession)
        self.ui.menuDb_cbx.setCurrentText(self.config.load_config()['database'].get('db_type'))
        self.setUpWidgets.onMenuDbOnChange()

    def setDbSession(self):
        self.dbSession = self.setUpWidgets.applyBtn()

    def setLanguage(self, lang_code):
        self.tr = dm.set_language(lang_code)
        self.setUpWidgets.tr = self.tr
        self.setWindowTitle(self.tr.gettext('App Title'))
        LangSwitcher(self.ui).translateSetter(self.tr)


def docsMakerRun():
    app = QApplication(sys.argv)
    window = DocsMakerMainWindow()
    window.show()
    sys.exit(app.exec())
