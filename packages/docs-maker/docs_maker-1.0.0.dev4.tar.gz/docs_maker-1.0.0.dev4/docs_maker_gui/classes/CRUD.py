from sqlalchemy.orm import Session
# from docs_maker.database.models import Configurations
from docs_maker_gui.classes.MainWIndow import Ui_MainWindow
# from docs_maker.database.services import ServiceConfigurations


class Crud:
    def __init__(self, ui: Ui_MainWindow):
        self.__ui = ui

    @property
    def ui(self):
        return self.__ui

    def applyConfig(self, session: Session):
        # ServiceConfigurations.insert_or_update_config(session, self.ui.menuDbUsername_le.objectName(),
        #                                               self.ui.menuDbUsername_le.text())
        # ServiceConfigurations.insert_or_update_config(session, self.ui.menuDbPassword_le.objectName(),
        #                                               self.ui.menuDbPassword_le.text())
        # ServiceConfigurations.insert_or_update_config(session, self.ui.menuDbPort_le.objectName(),
        #                                               self.ui.menuDbPort_le.text())
        pass

    def getConfig(self, session: Session):
        # configs = session.query(Configurations).all()
        # config_dict = {config.config_key: config.config_value for config in configs}
        # config_keys = {
        #     'db_port': self.ui.menuDbPort_le,
        #     'db_username': self.ui.menuDbName_le,
        #     'db_password': self.ui.menuDbPassword_le
        # }
        #
        # for config_key, form_widget in config_keys.items():
        #     # Проверяем, есть ли ключ в словаре
        #     value = config_dict.get(config_key)
        #     if value is not None:  # Проверка на наличие значения
        #         form_widget.setText(value)
        pass
