from docs_maker_gui.ui.docs_maker_main_window import Ui_MainWindow

class PageSwitcher():
    def __init__(self, ui: Ui_MainWindow):
        self.__ui = ui

    @property
    def ui(self):
        return self.__ui

    def setMainPage(self):
        self.ui.mainStacked_sw.setCurrentWidget(self.ui.mainPage_stPage)

    def setMenuPage(self):
        self.ui.mainStacked_sw.setCurrentWidget(self.ui.menuPage_stPage)