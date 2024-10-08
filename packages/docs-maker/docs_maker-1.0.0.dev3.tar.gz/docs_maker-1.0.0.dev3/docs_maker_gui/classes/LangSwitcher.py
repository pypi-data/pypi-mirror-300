from docs_maker_gui.ui.docs_maker_main_window import Ui_MainWindow
from docs_maker.cli.version import get_version

class LangSwitcher():
    def __init__(self, ui: Ui_MainWindow):
        self.__ui = ui

    @property
    def ui(self):
        return self.__ui

    def translateSetter(self, l):
        self.ui.mainWindow_lbl.setText((l.gettext('MainPage')))
        self.ui.menu_lbl.setText(l.gettext('MenuPage'))
        self.ui.mWVersion_lbl.setText(l.gettext('Version'))
        self.ui.mWVersionValue_lbl.setText(get_version('docs_maker'))
        self.ui.menu_lbl.setText(l.gettext('menu_lbl'))
        self.ui.menuDb_lbl.setText(l.gettext('db_type'))
        self.ui.menuApply_btn.setText(l.gettext('Apply'))
        self.ui.menuDbName_lbl.setText(l.gettext('DB name'))
        self.ui.menuDbUsername_lbl.setText(l.gettext('DB user name'))
        self.ui.menuDbPassword_lbl.setText(l.gettext('DB user password'))
