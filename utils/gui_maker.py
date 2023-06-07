# TODO: 1) Необходимо добавить обработку кейса когда нет зареганных пользователей, а так же добавить форму регистрации
#       2) Форма для обработки капчи (с картинкой)
from __future__ import annotations

import pathlib
import requests

from PyQt5 import QtWidgets
from PyQt5.QtCore import QThread, QTime, pyqtSignal, pyqtSlot
from PyQt5 import QtGui, QtCore

import config
from interfaces.main_standalone_window import Ui_MainWindow
from interfaces.vk_login_window import Ui_RegistrationWindow
from interfaces.popup_result_window import Ui_MessageWindow
from interfaces.captha_handler import Ui_CapthaHandler

import utils.core_api as core_api

# this fix problem with relative path after importing module
current_file_dir_path = str(pathlib.Path(__file__).parent)
current_file_dir_parent_path = str(pathlib.Path(__file__).parent.parent)


class CaptchaHandlerWindow(QtWidgets.QWidget):
    def __init__(self):
        super(CaptchaHandlerWindow, self).__init__()
        self.ui = Ui_CapthaHandler()
        self.ui.setupUi(self)
        self.setWindowTitle('Проверка пользователя')
        self.ui.get_input_button.clicked.connect(self.get_captcha_from_entry_field)

        url = "https://api.vk.com/captcha.php?sid=547973203351&s=1"
        data = requests.get(url).content
        image = QtGui.QImage()
        image.loadFromData(data)
        pixmap = QtGui.QPixmap(image)

        # todo: scale picture
        pixmap.scaled(2, 2, QtCore.Qt.KeepAspectRatio)

        self.ui.image_field.setPixmap(pixmap)

        # todo: delete
        self.show()

    def get_captcha_from_entry_field(self) -> str:
        captcha_code = self.ui.captcha_input.text()
        self.ui.captcha_input.clear()

        if captcha_code:
            pass


class MessageWindow(QtWidgets.QWidget):
    def __init__(self):
        super(MessageWindow, self).__init__()
        self.ui = Ui_MessageWindow()
        self.ui.setupUi(self)
        self.setWindowTitle('   ')
        self.ui.button_ok.clicked.connect(self.close)

        # Default size
        self.size_default = self.size()

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.resize_to_default()

    def resize_to_default(self):
        self.resize(self.size_default)


class VkRegistrationInterface(QtWidgets.QMainWindow):
    def __init__(self, parent: Interface):
        super(VkRegistrationInterface, self).__init__()
        self.parent_window = parent
        self.ui = Ui_RegistrationWindow()
        self.ui.setupUi(self)

        self.ui.entry_button.clicked.connect(self.get_login_info)
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
        self.ui.entry_button.setIcon(QtGui.QIcon(current_file_dir_parent_path + '/static/vk_logo.png'))
        self._print_visibility_button_icon()
        self.ui.mail_icon.setPixmap(
            QtGui.QPixmap(current_file_dir_parent_path + '/static/mail.png')
        )
        self.ui.password_icon.setPixmap(
            QtGui.QPixmap(current_file_dir_parent_path + '/static/password.png')
        )

    def change_visibility(self):
        self.visibility_button_mode += 1
        assert len(self.visibility_button_icons) == len(self.password_view_mode)
        self.visibility_button_mode %= len(self.visibility_button_icons)
        self._print_visibility_button_icon()

    def get_login_info(self):
        login = self.ui.login_entry_field.text()
        password = self.ui.password_entry_field.text()

        # TODO: 1) если введенные данные аккаунта норм (видимо надо пробовать регистрацию в вк), то закрыть окно,
        #               а так же обновить счетчик аккаунтов и добавить аккаунт в выпадающий список
        #       2) иначе надо выдавать предупреждение типа Bad Password и оставлять окно рабочим
        #       3) а так же надо проверять не были ли введены эти данные ранее

        # TODO: проверять валидность логина и пароля,
        #       если валидно, то закрыть окно и добавить аккаунт,
        #       иначе пдсветить красным/отсигнализировать и (стереть введенные данные из полей?)

        self.parent_window.ui.accounts_list_display.addItem(login)
        # set last as active item
        self.parent_window.ui.accounts_list_display.setCurrentIndex(
            self.parent_window.ui.accounts_list_display.count() - 1
        )

        core_api.vk_user_add(login, password)
        core_api.context_save()

        # Print actual count
        self.parent_window.ui.accounts_counter.setText(str(core_api.vk_users_get_count()))
        print(config.context)

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
        self.main_script_runner = RunnerWorker(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.init_ui()

        ############################################################
        # Child windows
        self.child_vk_login_window = VkRegistrationInterface(self)
        self.child_result_window = MessageWindow()
        self.child_captcha_handler = CaptchaHandlerWindow()

        # Slots and signals connection
        self.
        ############################################################

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        # Close relative windows
        if self.child_vk_login_window:
            self.child_vk_login_window.close()
        if self.child_result_window:
            self.child_result_window.close()
        if self.child_captcha_handler:
            self.child_captcha_handler.close()

    def init_ui(self):
        self.setWindowTitle('Авто Коммент')
        # Icon source:
        # <a href="https://www.flaticon.com/ru/free-icons/" title="робот иконки">Робот иконки от Freepik - Flaticon</a>
        self.setWindowIcon(QtGui.QIcon(current_file_dir_parent_path + '/static/main_window_icon.png'))
        self.ui.add_link_entry.setPlaceholderText('Введите ссылку добавляемого объекта')
        self.ui.delete_link_entry.setPlaceholderText('Введите ссылку удаляемого объекта')
        self.ui.accounts_counter.setAlignment(QtCore.Qt.AlignCenter)

        for login, password in core_api.vk_users_get():
            self.add_account_to_combo_box(login)

        # buttons
        self.ui.add_link_entry_button.clicked.connect(self.get_link_to_add)
        self.ui.delete_link_entry_button.clicked.connect(self.get_link_to_delete)
        self.ui.time_entry_button.clicked.connect(self.get_time)
        self.ui.script_management_button.clicked.connect(self.run_main_script_and_set_button_to_stop_condition)
        self.ui.add_account_button.clicked.connect(self.show_login_window)
        self.ui.delete_account_button.clicked.connect(self.delete_account)

        self.ui.accounts_counter.setText(str(core_api.vk_users_get_count()))    # set count of accounts
        self.ui.time_entry.setTime(QTime(*core_api.time_get_stored()))          # set last used time

    def run_main_script_and_set_button_to_stop_condition(self):
        del self.main_script_runner
        self.main_script_runner = RunnerWorker(self)
        self.main_script_runner.setTerminationEnabled(True)
        self.main_script_runner.start()

        self.ui.script_management_button.setText('Стоп')
        self.ui.script_management_button.clicked.disconnect(self.run_main_script_and_set_button_to_stop_condition)
        self.ui.script_management_button.clicked.connect(self.stop_main_script_and_set_button_to_start_condition)

    def stop_main_script_and_set_button_to_start_condition(self):
        self.main_script_runner.stop()
        self.ui.script_management_button.setText('Старт')
        self.ui.script_management_button.clicked.disconnect(self.stop_main_script_and_set_button_to_start_condition)
        self.ui.script_management_button.clicked.connect(self.run_main_script_and_set_button_to_stop_condition)

    def handle_script_finishing(self):
        self._show_result_window(success=True)

        self.ui.script_management_button.setText('Старт')
        self.ui.script_management_button.clicked.disconnect(self.stop_main_script_and_set_button_to_start_condition)
        self.ui.script_management_button.clicked.connect(self.run_main_script_and_set_button_to_stop_condition)

    def get_link_to_add(self):
        entry_link_value = self.ui.add_link_entry.text()
        self.ui.add_link_entry.clear()

        if entry_link_value:
            if not core_api.photo_check_if_stored(entry_link_value):
                core_api.photo_add(entry_link_value)
            else:
                self._show_result_window(success=False, message="Такое фото уже сохранено")

    def get_link_to_delete(self):
        entry_link_value = self.ui.delete_link_entry.text()
        self.ui.delete_link_entry.clear()

        if entry_link_value:
            if core_api.photo_check_if_stored(entry_link_value):
                core_api.photo_delete(entry_link_value)
            else:
                self._show_result_window(success=False, message="Такое фото не сохранено")

    def get_time(self):
        hour_value = self.ui.time_entry.time().hour()
        minute_value = self.ui.time_entry.time().minute()
        core_api.time_set_value(hour=hour_value, minute=minute_value)

    def show_login_window(self):
        self.child_vk_login_window.show()

    def delete_account(self):
        mail_to_delete = self.ui.accounts_list_display.currentText()
        core_api.vk_user_delete(mail_to_delete)
        core_api.context_save()

        self.ui.accounts_list_display.removeItem(
            self.ui.accounts_list_display.currentIndex()
        )

        # print actual accounts count
        self.ui.accounts_counter.setText(str(core_api.vk_users_get_count()))

    def add_account_to_combo_box(self, mail: str) -> None:
        # todo: пробовать делать (и запоминать сессии), брать имя-фамилию и выводить ее
        self.ui.accounts_list_display.addItem(mail)


    def _show_result_window(self, success: bool, message: str = None):
        if success:
            showed_message = "Успешно!"
        else:
            showed_message = "Неудача!"

        if message:
            showed_message += message

            # resize width for message
            self.child_result_window.resize(self.child_result_window.layout().sizeHint())

        print(self.child_result_window.ui.message.text())
        self.child_result_window.ui.message.setText(showed_message)
        print(self.child_result_window.ui.message.text())

        self.child_result_window.show()


class RunnerWorker(QThread):
    def __init__(self, calling_window: Interface):
        QThread.__init__(self)

        self.calling_window = calling_window

        self.need_captcha = pyqtSignal()
        self.captcha_success = pyqtSignal()

    def run(self):
        print('Start')
        core_api.main_script_start()
        print('Done')
        self.calling_window.handle_script_finishing()

    def stop(self):
        print('Stopped!')
        self.terminate()

    def _handle_captcha(self, captcha):
        # Эта функция будет выполняться внутри параллельного QThread,
        # поэтому может быть приостановлена бесконечным циклом
        self.calling_window.child_captcha_handler.show()
        while True:
            signal <- (connect from captcha handler window)
            while not signal:
                # todo: wait signal from self.child_captcha_handler
                wait
            try:
                captcha.try_again(signal.value)
                break
            except vk_api.exceptions.Captcha:
                continue
            except vk_api.exceptions.ApiError:
                # todo: message to wait for next try
                continue
        self.calling_window.child_captcha_handler.close()

