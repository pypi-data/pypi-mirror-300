from gettext import GNUTranslations
from docs_maker_gui.ui.docs_maker_main_window import Ui_MainWindow
from PySide6.QtWidgets import QMessageBox
from docs_maker.database.init_db_sqlite3 import InitDbSqlite3

class SetUpWidgets():
    def __init__(self, ui: Ui_MainWindow, parent, lang: GNUTranslations = None):
        self.__ui = ui
        self.__parent = parent
        self.__l = lang

    @property
    def ui(self):
        return self.__ui

    @property
    def parent(self):
        return self.__parent

    @property
    def l(self):
        return self.__l

    @l.setter
    def l(self, data):
        self.__l = data

    def onMenuDbOnChange(self, index):
        if self.ui.menuDb_cbx.currentText() == 'SQLite3':
            self.ui.menuDbName_lbl.setText(self.l.gettext('DB name'))
            self.ui.menuDbUsername_le.setText('')
            self.ui.menuDbPassword_le.setText('')
            self.ui.menuDbUsername_le.setEnabled(False)
            self.ui.menuDbPassword_le.setEnabled(False)
        elif self.ui.menuDb_cbx.currentText() == 'PostgreSQL':
            self.ui.menuDbName_lbl.setText(self.l.gettext('JDBC'))
            self.ui.menuDbUsername_le.setEnabled(True)
            self.ui.menuDbPassword_le.setEnabled(True)

    def applyBtn(self, index):
        self.dbSqliteInitDb()
        QMessageBox.information(self.parent, self.l.gettext('Information'), self.l.gettext('Apply config'), QMessageBox.StandardButton.Ok, QMessageBox.StandardButton.Ok)

    def dbSqliteInitDb(self):
        idb = InitDbSqlite3(self.ui.menuDbName_le.text())
        idb.init()
