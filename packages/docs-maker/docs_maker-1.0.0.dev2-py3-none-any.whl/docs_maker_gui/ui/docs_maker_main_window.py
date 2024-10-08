# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'docs-maker-main-window.ui'
##
## Created by: Qt User Interface Compiler version 6.7.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QMainWindow,
    QPushButton, QScrollArea, QSizePolicy, QSpacerItem,
    QStackedWidget, QVBoxLayout, QWidget)
import docs_maker_gui.resources.resources

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(548, 406)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_5 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.main_btn = QPushButton(self.centralwidget)
        self.main_btn.setObjectName(u"main_btn")
        self.main_btn.setStyleSheet(u"QPushButton {\n"
"	margin-left: 10px;\n"
"}")
        icon = QIcon()
        icon.addFile(u":/icons/icons/home-64-blue.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.main_btn.setIcon(icon)
        self.main_btn.setIconSize(QSize(36, 36))

        self.horizontalLayout_2.addWidget(self.main_btn)

        self.menu_btn = QPushButton(self.centralwidget)
        self.menu_btn.setObjectName(u"menu_btn")
        self.menu_btn.setStyleSheet(u"QPushButton {\n"
"	margin-right: 10px;\n"
"}")
        icon1 = QIcon()
        icon1.addFile(u":/icons/icons/more-horiz-64-blue.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.menu_btn.setIcon(icon1)
        self.menu_btn.setIconSize(QSize(36, 36))

        self.horizontalLayout_2.addWidget(self.menu_btn)


        self.verticalLayout_4.addLayout(self.horizontalLayout_2)

        self.scrollArea = QScrollArea(self.centralwidget)
        self.scrollArea.setObjectName(u"scrollArea")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollArea.sizePolicy().hasHeightForWidth())
        self.scrollArea.setSizePolicy(sizePolicy)
        self.scrollArea.setStyleSheet(u"QScrollArea {\n"
"	border: none\n"
"}")
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 112, 338))
        self.verticalLayout = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.pushButton = QPushButton(self.scrollAreaWidgetContents)
        self.pushButton.setObjectName(u"pushButton")

        self.verticalLayout.addWidget(self.pushButton)

        self.pushButton_12 = QPushButton(self.scrollAreaWidgetContents)
        self.pushButton_12.setObjectName(u"pushButton_12")

        self.verticalLayout.addWidget(self.pushButton_12)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout_4.addWidget(self.scrollArea)


        self.horizontalLayout_3.addLayout(self.verticalLayout_4)

        self.mainStacked_sw = QStackedWidget(self.centralwidget)
        self.mainStacked_sw.setObjectName(u"mainStacked_sw")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.mainStacked_sw.sizePolicy().hasHeightForWidth())
        self.mainStacked_sw.setSizePolicy(sizePolicy1)
        self.mainPage_stPage = QWidget()
        self.mainPage_stPage.setObjectName(u"mainPage_stPage")
        self.verticalLayout_3 = QVBoxLayout(self.mainPage_stPage)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.mainWindow_lbl = QLabel(self.mainPage_stPage)
        self.mainWindow_lbl.setObjectName(u"mainWindow_lbl")
        font = QFont()
        font.setPointSize(24)
        self.mainWindow_lbl.setFont(font)
        self.mainWindow_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_3.addWidget(self.mainWindow_lbl)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer_2)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.mWVersion_lbl = QLabel(self.mainPage_stPage)
        self.mWVersion_lbl.setObjectName(u"mWVersion_lbl")

        self.horizontalLayout.addWidget(self.mWVersion_lbl)

        self.mWVersionValue_lbl = QLabel(self.mainPage_stPage)
        self.mWVersionValue_lbl.setObjectName(u"mWVersionValue_lbl")

        self.horizontalLayout.addWidget(self.mWVersionValue_lbl)


        self.verticalLayout_3.addLayout(self.horizontalLayout)

        self.mainStacked_sw.addWidget(self.mainPage_stPage)
        self.menuPage_stPage = QWidget()
        self.menuPage_stPage.setObjectName(u"menuPage_stPage")
        self.verticalLayout_2 = QVBoxLayout(self.menuPage_stPage)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.menu_lbl = QLabel(self.menuPage_stPage)
        self.menu_lbl.setObjectName(u"menu_lbl")
        self.menu_lbl.setFont(font)
        self.menu_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_2.addWidget(self.menu_lbl)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer_3)

        self.mainStacked_sw.addWidget(self.menuPage_stPage)

        self.horizontalLayout_3.addWidget(self.mainStacked_sw)


        self.verticalLayout_5.addLayout(self.horizontalLayout_3)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.mainStacked_sw.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Docs Maker", None))
        self.main_btn.setText("")
        self.menu_btn.setText("")
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.pushButton_12.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.mainWindow_lbl.setText(QCoreApplication.translate("MainWindow", u"main", None))
        self.mWVersion_lbl.setText(QCoreApplication.translate("MainWindow", u"Version", None))
        self.mWVersionValue_lbl.setText(QCoreApplication.translate("MainWindow", u"0.0.0", None))
        self.menu_lbl.setText(QCoreApplication.translate("MainWindow", u"menu_lbl", None))
    # retranslateUi

