from docs_maker_gui.ui.docs_maker_main_window import Ui_MainWindow
from docs_maker.cli.version import get_version


class LangSwitcher():
    def __init__(self, ui: Ui_MainWindow):
        self.__ui = ui

    @property
    def ui(self):
        return self.__ui

    def translateSetter(self, tr):
        self.ui.mainWindow_lbl.setText((tr.gettext('MainPage')))
        self.ui.menu_lbl.setText(tr.gettext('MenuPage'))
        self.ui.mWVersion_lbl.setText(tr.gettext('Version'))
        self.ui.mWVersionValue_lbl.setText(get_version('docs_maker'))
        self.ui.menu_lbl.setText(tr.gettext('menu_lbl'))
        self.ui.db_type.setText(tr.gettext('db_type'))
        self.ui.menuApply_btn.setText(tr.gettext('Apply'))
        self.ui.db_name.setText(tr.gettext('DB name'))
        self.ui.db_host.setText(tr.gettext('DB hostname'))
        self.ui.db_port.setText(tr.gettext('DB port'))
        self.ui.db_username.setText(tr.gettext('DB user name'))
        self.ui.db_password.setText(tr.gettext('DB user password'))
