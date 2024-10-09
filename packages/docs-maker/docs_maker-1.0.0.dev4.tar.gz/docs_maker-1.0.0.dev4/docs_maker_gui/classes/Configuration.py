import os
import configparser
from docs_maker_gui.ui.docs_maker_main_window import Ui_MainWindow

CONFIG_PATH = 'config.ini'


class Config():
    def __init__(self, ui: Ui_MainWindow):
        self.__ui = ui

    @property
    def ui(self):
        return self.__ui

    def load_config(self):
        config = configparser.ConfigParser()
        if os.path.exists(CONFIG_PATH):
            config.read(CONFIG_PATH)
        else:
            config['database'] = {
                self.ui.db_type.objectName(): '',
                self.ui.db_name.objectName(): '',
                self.ui.db_host.objectName(): '',
                self.ui.db_port.objectName(): '',
                self.ui.db_username.objectName(): '',
                self.ui.db_password.objectName(): ''
            }
        with open(CONFIG_PATH, 'w', encoding='utf-8') as configfile:
            config.write(configfile)

        return config

    def save_config(self):
        config = configparser.ConfigParser()
        config['database'] = {
            self.ui.db_type.objectName(): self.ui.menuDb_cbx.currentText(),
            self.ui.db_name.objectName(): self.ui.menuDbName_le.text(),
            self.ui.db_host.objectName(): self.ui.menuDbHost_le.text(),
            self.ui.db_port.objectName(): self.ui.menuDbPort_le.text(),
            self.ui.db_username.objectName(): self.ui.menuDbUsername_le.text(),
            self.ui.db_password.objectName(): self.ui.menuDbPassword_le.text()
        }

        with open(CONFIG_PATH, 'w', encoding='utf-8') as configfile:
            config.write(configfile)
            configfile.close()
