# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'vk_login_window.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_RegistrationWindow(object):
    def setupUi(self, RegistrationWindow):
        RegistrationWindow.setObjectName("RegistrationWindow")
        RegistrationWindow.resize(393, 215)
        self.login_text = QtWidgets.QLabel(RegistrationWindow)
        self.login_text.setGeometry(QtCore.QRect(20, 50, 67, 17))
        self.login_text.setObjectName("login_text")
        self.login_entry_field = QtWidgets.QLineEdit(RegistrationWindow)
        self.login_entry_field.setGeometry(QtCore.QRect(80, 50, 261, 25))
        self.login_entry_field.setObjectName("login_entry_field")
        self.password_entry_field = QtWidgets.QLineEdit(RegistrationWindow)
        self.password_entry_field.setGeometry(QtCore.QRect(80, 90, 261, 25))
        self.password_entry_field.setObjectName("password_entry_field")
        self.pushButton = QtWidgets.QPushButton(RegistrationWindow)
        self.pushButton.setGeometry(QtCore.QRect(90, 150, 221, 31))
        self.pushButton.setObjectName("pushButton")
        self.password_text = QtWidgets.QLabel(RegistrationWindow)
        self.password_text.setGeometry(QtCore.QRect(20, 90, 67, 17))
        self.password_text.setObjectName("password_text")
        self.is_password_viewable_button = QtWidgets.QPushButton(RegistrationWindow)
        self.is_password_viewable_button.setGeometry(QtCore.QRect(350, 90, 21, 21))
        self.is_password_viewable_button.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../static/crossed_eye.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.is_password_viewable_button.setIcon(icon)
        self.is_password_viewable_button.setObjectName("is_password_viewable_button")

        self.retranslateUi(RegistrationWindow)
        QtCore.QMetaObject.connectSlotsByName(RegistrationWindow)

    def retranslateUi(self, RegistrationWindow):
        _translate = QtCore.QCoreApplication.translate
        RegistrationWindow.setWindowTitle(_translate("RegistrationWindow", "Form"))
        self.login_text.setText(_translate("RegistrationWindow", "Логин"))
        self.pushButton.setText(_translate("RegistrationWindow", "Войти"))
        self.password_text.setText(_translate("RegistrationWindow", "Пароль"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    RegistrationWindow = QtWidgets.QWidget()
    ui = Ui_RegistrationWindow()
    ui.setupUi(RegistrationWindow)
    RegistrationWindow.show()
    sys.exit(app.exec_())
