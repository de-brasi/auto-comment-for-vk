# TODO: 1) Необходимо добавить обработку кейса когда нет зареганных пользователей, а так же добавить регистрацию
#       2) После нажатия кнопки Старт менять ее название на Стоп (с соответствующим поведением)

import pathlib

from PyQt5 import QtWidgets
from PyQt5.QtCore import QThread, QTime
from PyQt5 import QtGui
from interfaces.main_standalone_window import Ui_MainWindow
from interfaces.vk_login_window import Ui_RegistrationWindow

import utils.core_api as core_api

# this fix problem with relative path after importing module
current_file_dir_path = str(pathlib.Path(__file__).parent)
current_file_dir_parent_path = str(pathlib.Path(__file__).parent.parent)


class RunnerWorker(QThread):
    def __init__(self):
        QThread.__init__(self)

    def run(self):
        core_api.main_script_start()


class VkRegistrationInterface(QtWidgets.QMainWindow):
    def __init__(self):
        super(VkRegistrationInterface, self).__init__()
        self.ui = Ui_RegistrationWindow()
        self.ui.setupUi(self)

        self.ui.pushButton.clicked.connect(self.get_login_info)
        self.ui.is_password_viewable_button.clicked.connect(self.change_visibility)

        self.visibility_button_icons = ['opened_eye.png', 'crossed_eye.png']
        self.password_view_mode = [QtWidgets.QLineEdit.Normal, QtWidgets.QLineEdit.Password]
        self.visibility_button_mode = 1

        self.init_ui()

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        # Rollback
        self.ui.password_entry_field.clear()
        self.ui.login_entry_field.clear()
        self.visibility_button_mode = 1

    def init_ui(self):
        self.setWindowTitle('Вход в аккаунт VK')
        self._print_visibility_button_icon()

    def change_visibility(self):
        self.visibility_button_mode += 1
        assert len(self.visibility_button_icons) == len(self.password_view_mode)
        self.visibility_button_mode %= len(self.visibility_button_icons)
        self._print_visibility_button_icon()

    def get_login_info(self):
        # TODO: проверять валидность логина и пароля,
        #       если валидно, то закрыть окно и добавить аккаунт,
        #       иначе пдсветить красным/отсигнализировать и (стереть введенные данные из полей?)
        login = self.ui.login_entry_field.text()
        password = self.ui.password_entry_field.text()

        print(login, password)

    def _print_visibility_button_icon(self):
        self.ui.is_password_viewable_button.setIcon(
            QtGui.QIcon(current_file_dir_parent_path +
                        '/static/' +
                        self.visibility_button_icons[self.visibility_button_mode])
        )
        self.ui.password_entry_field.setEchoMode(
            self.password_view_mode[self.visibility_button_mode]
        )


class Interface(QtWidgets.QMainWindow):
    def __init__(self):
        super(Interface, self).__init__()
        self.main_script_runner = RunnerWorker()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.init_ui()
        self.vk_registration_window = VkRegistrationInterface()

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        if self.vk_registration_window:
            self.vk_registration_window.close()

    def init_ui(self):
        self.setWindowTitle('Авто Коммент')
        # Icon source:
        # <a href="https://www.flaticon.com/ru/free-icons/" title="робот иконки">Робот иконки от Freepik - Flaticon</a>
        self.setWindowIcon(QtGui.QIcon(current_file_dir_parent_path + '/static/main_window_icon.png'))
        self.ui.add_link_entry.setPlaceholderText('Введите ссылку добавляемого объекта')
        self.ui.delete_link_entry.setPlaceholderText('Введите ссылку удаляемого объекта')

        # buttons
        self.ui.add_link_entry_button.clicked.connect(self.get_link_to_add)
        self.ui.delete_link_entry_button.clicked.connect(self.get_link_to_delete)
        self.ui.time_entry_button.clicked.connect(self.get_time)
        self.ui.start_script_button.clicked.connect(self.main_script_runner.start)
        self.ui.add_account_button.clicked.connect(self.add_account)

        self.ui.accounts_counter.setText(str(core_api.get_vk_users_count()))    # set count of accounts
        self.ui.time_entry.setTime(QTime(*core_api.get_stored_time()))          # set last used time

    def get_link_to_add(self):
        entry_link_value = self.ui.add_link_entry.text()
        if entry_link_value:
            self.ui.add_link_entry.clear()
            core_api.add_photo(entry_link_value)

        # todo: debug
        print(core_api.get_added_photos())

    def get_link_to_delete(self):
        # todo: выводить окно с сообщением удалено или нет
        entry_link_value = self.ui.delete_link_entry.text()
        if entry_link_value:
            self.ui.delete_link_entry.clear()
            core_api.delete_photo(entry_link_value)

        # todo: debug
        print(core_api.get_added_photos())

    def get_time(self):
        hour_value = self.ui.time_entry.time().hour()
        minute_value = self.ui.time_entry.time().minute()
        core_api.set_time(hour=hour_value, minute=minute_value)

    def add_account(self):
        # TODO: 1) если введенные данные аккаунта норм (видимо надо пробовать регистрацию в вк), то закрыть окно,
        #               а так же обновить счетчик аккаунтов и добавить аккаунт в выпадающий список
        #       2) иначе надо выдавать предупреждение типа Bad Password и оставлять окно рабочим
        #       3) а так же надо проверять не были ли введены эти данные ранее

        self.vk_registration_window.show()
        self.ui.accounts_counter.setText(str(core_api.get_vk_users_count()))

    def delete_account(self):
        pass
        self.ui.accounts_counter.setText(str(core_api.get_vk_users_count()))
