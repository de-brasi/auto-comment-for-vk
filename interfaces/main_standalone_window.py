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
        MainWindow.resize(627, 628)
        MainWindow.setMinimumSize(QtCore.QSize(627, 628))
        MainWindow.setMaximumSize(QtCore.QSize(627, 628))
        MainWindow.setAutoFillBackground(False)
        MainWindow.setStyleSheet("")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setStyleSheet("")
        self.centralwidget.setObjectName("centralwidget")
        self.MainTextAboutUsage = QtWidgets.QLabel(self.centralwidget)
        self.MainTextAboutUsage.setGeometry(QtCore.QRect(20, 150, 581, 201))
        self.MainTextAboutUsage.setMouseTracking(True)
        self.MainTextAboutUsage.setStyleSheet("background-color: #ffffff")
        self.MainTextAboutUsage.setObjectName("MainTextAboutUsage")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(20, 360, 581, 61))
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
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(20, 430, 581, 71))
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
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(20, 510, 371, 111))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.TimeEntryGroup = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.TimeEntryGroup.setContentsMargins(0, 0, 0, 0)
        self.TimeEntryGroup.setObjectName("TimeEntryGroup")
        self.TimeEntryDescriptionFrame = QtWidgets.QFrame(self.verticalLayoutWidget)
        self.TimeEntryDescriptionFrame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.TimeEntryDescriptionFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.TimeEntryDescriptionFrame.setObjectName("TimeEntryDescriptionFrame")
        self.time_entry_description = QtWidgets.QLabel(self.TimeEntryDescriptionFrame)
        self.time_entry_description.setGeometry(QtCore.QRect(0, 0, 361, 51))
        self.time_entry_description.setObjectName("time_entry_description")
        self.TimeEntryFrame = QtWidgets.QFrame(self.TimeEntryDescriptionFrame)
        self.TimeEntryFrame.setGeometry(QtCore.QRect(0, 60, 359, 51))
        self.TimeEntryFrame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.TimeEntryFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.TimeEntryFrame.setLineWidth(1)
        self.TimeEntryFrame.setObjectName("TimeEntryFrame")
        self.time_entry = QtWidgets.QTimeEdit(self.TimeEntryFrame)
        self.time_entry.setGeometry(QtCore.QRect(10, 10, 161, 31))
        self.time_entry.setStyleSheet("font: 75 20pt \"Tlwg Typo\";")
        self.time_entry.setObjectName("time_entry")
        self.time_entry_button = QtWidgets.QPushButton(self.TimeEntryFrame)
        self.time_entry_button.setGeometry(QtCore.QRect(200, 10, 89, 25))
        self.time_entry_button.setObjectName("time_entry_button")
        self.TimeEntryGroup.addWidget(self.TimeEntryDescriptionFrame)
        self.start_script_button = QtWidgets.QPushButton(self.centralwidget)
        self.start_script_button.setGeometry(QtCore.QRect(430, 510, 161, 101))
        self.start_script_button.setObjectName("start_script_button")
        self.AccountsManagmentGroup = QtWidgets.QFrame(self.centralwidget)
        self.AccountsManagmentGroup.setGeometry(QtCore.QRect(20, 10, 581, 131))
        self.AccountsManagmentGroup.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.AccountsManagmentGroup.setFrameShadow(QtWidgets.QFrame.Raised)
        self.AccountsManagmentGroup.setObjectName("AccountsManagmentGroup")
        self.accounts_list_display = QtWidgets.QComboBox(self.AccountsManagmentGroup)
        self.accounts_list_display.setGeometry(QtCore.QRect(210, 10, 241, 31))
        self.accounts_list_display.setObjectName("accounts_list_display")
        self.AccountsCountAndAdding = QtWidgets.QFrame(self.AccountsManagmentGroup)
        self.AccountsCountAndAdding.setGeometry(QtCore.QRect(10, 10, 191, 111))
        self.AccountsCountAndAdding.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.AccountsCountAndAdding.setFrameShadow(QtWidgets.QFrame.Raised)
        self.AccountsCountAndAdding.setObjectName("AccountsCountAndAdding")
        self.add_account_button = QtWidgets.QPushButton(self.AccountsCountAndAdding)
        self.add_account_button.setGeometry(QtCore.QRect(10, 50, 161, 41))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../static/vk_logo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.add_account_button.setIcon(icon)
        self.add_account_button.setIconSize(QtCore.QSize(20, 20))
        self.add_account_button.setObjectName("add_account_button")
        self.accounts_frame_description = QtWidgets.QLabel(self.AccountsCountAndAdding)
        self.accounts_frame_description.setGeometry(QtCore.QRect(10, 10, 101, 31))
        self.accounts_frame_description.setObjectName("accounts_frame_description")
        self.accounts_counter = QtWidgets.QLabel(self.AccountsCountAndAdding)
        self.accounts_counter.setGeometry(QtCore.QRect(120, 10, 51, 31))
        self.accounts_counter.setStyleSheet("background-color: rgb(255, 255, 255)")
        self.accounts_counter.setText("")
        self.accounts_counter.setObjectName("accounts_counter")
        self.delete_account_button = QtWidgets.QPushButton(self.AccountsManagmentGroup)
        self.delete_account_button.setGeometry(QtCore.QRect(460, 10, 111, 41))
        self.delete_account_button.setObjectName("delete_account_button")
        self.horizontalLayoutWidget.raise_()
        self.horizontalLayoutWidget_2.raise_()
        self.MainTextAboutUsage.raise_()
        self.verticalLayoutWidget.raise_()
        self.start_script_button.raise_()
        self.AccountsManagmentGroup.raise_()
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.MainTextAboutUsage.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:12pt; font-weight:600;\">Инструкция</span>: </p><p>1) авторизуйтесь в один или несколько аккаунтов VK </p><p>2) введите ссылки на фотографии для комментирования<br/>(аналогично удалите при необходимости)</p><p>3) введите время начала коммментирования в формате час:мин </p><p>4) нажмите Старт </p><p>5) ожидайте</p></body></html>"))
        self.add_link_entry_button.setText(_translate("MainWindow", "Добавить"))
        self.delete_link_entry_button.setText(_translate("MainWindow", "Удалить"))
        self.time_entry_description.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">Введите время в формате час:мин и </p><p align=\"center\">нажмите кнопку &quot;Ввод&quot;</p></body></html>"))
        self.time_entry_button.setText(_translate("MainWindow", "Ввод"))
        self.start_script_button.setText(_translate("MainWindow", "Старт"))
        self.add_account_button.setText(_translate("MainWindow", "Добавить аккаунт"))
        self.accounts_frame_description.setText(_translate("MainWindow", " Аккаунты VK"))
        self.delete_account_button.setText(_translate("MainWindow", "Удалить \n"
"аккаунт"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
