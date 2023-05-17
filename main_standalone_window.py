# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_standalone_window.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(627, 518)
        MainWindow.setMinimumSize(QtCore.QSize(627, 518))
        MainWindow.setMaximumSize(QtCore.QSize(627, 518))
        MainWindow.setAutoFillBackground(False)
        MainWindow.setStyleSheet("")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setStyleSheet("")
        self.centralwidget.setObjectName("centralwidget")
        self.MainTextAboutUsage = QtWidgets.QLabel(self.centralwidget)
        self.MainTextAboutUsage.setGeometry(QtCore.QRect(40, 10, 571, 151))
        self.MainTextAboutUsage.setMouseTracking(False)
        self.MainTextAboutUsage.setStyleSheet("background-color: #ffffff")
        self.MainTextAboutUsage.setObjectName("MainTextAboutUsage")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(40, 190, 571, 61))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.AddLinkGroup = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.AddLinkGroup.setContentsMargins(0, 0, 0, 0)
        self.AddLinkGroup.setObjectName("AddLinkGroup")
        self.add_link_entry = QtWidgets.QLineEdit(self.horizontalLayoutWidget)
        self.add_link_entry.setObjectName("add_link_entry")
        self.AddLinkGroup.addWidget(self.add_link_entry)
        self.add_link_entry_button = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.add_link_entry_button.setObjectName("add_link_entry_button")
        self.AddLinkGroup.addWidget(self.add_link_entry_button)
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(40, 280, 571, 71))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.DeleteLinkGroup = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.DeleteLinkGroup.setContentsMargins(0, 0, 0, 0)
        self.DeleteLinkGroup.setObjectName("DeleteLinkGroup")
        self.delete_link_entry = QtWidgets.QLineEdit(self.horizontalLayoutWidget_2)
        self.delete_link_entry.setObjectName("delete_link_entry")
        self.DeleteLinkGroup.addWidget(self.delete_link_entry)
        self.delete_link_entry_button = QtWidgets.QPushButton(self.horizontalLayoutWidget_2)
        self.delete_link_entry_button.setObjectName("delete_link_entry_button")
        self.DeleteLinkGroup.addWidget(self.delete_link_entry_button)
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(40, 380, 361, 111))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.TimeEntryGroup = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.TimeEntryGroup.setContentsMargins(0, 0, 0, 0)
        self.TimeEntryGroup.setObjectName("TimeEntryGroup")
        self.TimeEntryDescriptionFrame = QtWidgets.QFrame(self.verticalLayoutWidget)
        self.TimeEntryDescriptionFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.TimeEntryDescriptionFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.TimeEntryDescriptionFrame.setObjectName("TimeEntryDescriptionFrame")
        self.time_entry_description = QtWidgets.QLabel(self.TimeEntryDescriptionFrame)
        self.time_entry_description.setGeometry(QtCore.QRect(0, 0, 211, 41))
        self.time_entry_description.setObjectName("time_entry_description")
        self.TimeEntryGroup.addWidget(self.TimeEntryDescriptionFrame)
        self.TimeEntryFrame = QtWidgets.QFrame(self.verticalLayoutWidget)
        self.TimeEntryFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.TimeEntryFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.TimeEntryFrame.setObjectName("TimeEntryFrame")
        self.time_entry = QtWidgets.QTimeEdit(self.TimeEntryFrame)
        self.time_entry.setGeometry(QtCore.QRect(10, 10, 161, 31))
        self.time_entry.setStyleSheet("font: 75 20pt \"Tlwg Typo\";")
        self.time_entry.setObjectName("time_entry")
        self.time_entry_button = QtWidgets.QPushButton(self.TimeEntryFrame)
        self.time_entry_button.setGeometry(QtCore.QRect(200, 10, 89, 25))
        self.time_entry_button.setObjectName("time_entry_button")
        self.TimeEntryGroup.addWidget(self.TimeEntryFrame)
        self.start_script_button = QtWidgets.QPushButton(self.centralwidget)
        self.start_script_button.setGeometry(QtCore.QRect(428, 384, 171, 111))
        self.start_script_button.setObjectName("start_script_button")
        self.horizontalLayoutWidget.raise_()
        self.horizontalLayoutWidget_2.raise_()
        self.MainTextAboutUsage.raise_()
        self.verticalLayoutWidget.raise_()
        self.start_script_button.raise_()
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.MainTextAboutUsage.setText(_translate("MainWindow", "Какой то текст, описывающий базовый функционал"))
        self.add_link_entry_button.setText(_translate("MainWindow", "Добавить"))
        self.delete_link_entry_button.setText(_translate("MainWindow", "Удалить"))
        self.time_entry_description.setText(_translate("MainWindow", "Ввод времени, приглашение"))
        self.time_entry_button.setText(_translate("MainWindow", "Ввод"))
        self.start_script_button.setText(_translate("MainWindow", "Старт"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
