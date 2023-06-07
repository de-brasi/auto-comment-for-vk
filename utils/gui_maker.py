# TODO: 1) Необходимо добавить обработку кейса когда нет зареганных пользователей, а так же добавить форму регистрации
#       2) Форма для обработки капчи (с картинкой)
from __future__ import annotations

import pathlib
import requests

from PyQt5 import QtWidgets
from PyQt5.QtCore import QThread, QTime, pyqtSignal, QMutex, QWaitCondition
from PyQt5 import QtGui, QtCore

import config

from vk_api.exceptions import Captcha
from vk_api.exceptions import ApiError

from typing import Callable

from interfaces.main_standalone_window import Ui_MainWindow
from interfaces.vk_login_window import Ui_RegistrationWindow
from interfaces.popup_result_window import Ui_MessageWindow
from interfaces.captha_handler import Ui_CapthaHandler

import utils.core_api as core_api

# this fix problem with relative path after importing module
current_file_dir_path = str(pathlib.Path(__file__).parent)
current_file_dir_parent_path = str(pathlib.Path(__file__).parent.parent)


class CaptchaHandlerWindow(QtWidgets.QWidget):
    signal_captcha_handling_interrupt = pyqtSignal()

    def __init__(self, thread_with_core_script: RunningThread):
        super(CaptchaHandlerWindow, self).__init__()

        self.thread_with_script = thread_with_core_script

        # Connect with signals
        self.thread_with_script.need_captcha_from_user.connect(self.show_captcha_handler)
        self.thread_with_script.success_captcha_got.connect(self.close)

        # Init ui
        self.ui = Ui_CapthaHandler()
        self.ui.setupUi(self)
        self.setWindowTitle('Проверка пользователя')
        self.ui.get_input_button.clicked.connect(self.take_captcha_from_entry_field)

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.signal_captcha_handling_interrupt.emit()

    def take_captcha_from_entry_field(self):
        captcha_code = self.ui.captcha_input.text()

        if not captcha_code:
            pass
        else:
            self.set_captcha_value_to_thread_with_mutex(captcha_code)

    def set_captcha_value_to_thread_with_mutex(self, value: str):
        self.thread_with_script.mutex.lock()
        self.thread_with_script.received_captcha_value = value
        self.thread_with_script.mutex.unlock()
        self.thread_with_script.captcha_waiter.wakeAll()

    def show_captcha_handler(self, captcha_url: str):
        # Update image
        data = requests.get(captcha_url).content
        image = QtGui.QImage()
        image.loadFromData(data)
        pixmap = QtGui.QPixmap(image)
        # todo: scale picture
        pixmap.scaled(2, 2, QtCore.Qt.KeepAspectRatio)
        self.ui.image_field.setPixmap(pixmap)

        if self.isHidden():
            self.show()
        else:
            # todo: сделать предыдущее решение капчи дефолтным и посдсветить красным
            previous_captcha_solution = self.ui.captcha_input.text()
            self.ui.captcha_input.clear()

            self.ui.captcha_input.setPlaceholderText(previous_captcha_solution)
            self.ui.captcha_input.setStyleSheet("QLineEdit[placeholderText] { color: red; }")


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
        self.main_script_runner = RunningThread(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.init_ui()

        ############################################################
        # Child windows
        self.child_vk_login_window = VkRegistrationInterface(self)
        self.child_result_window = MessageWindow()
        self.child_captcha_handler = CaptchaHandlerWindow(self.main_script_runner)
        ############################################################

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.close_relative_windows()

    def close_relative_windows(self):
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
        self.close_relative_windows()

        del self.main_script_runner
        self.main_script_runner = RunningThread(self)

        # Actualization of RunningThread object in CaptchaHandlerWindow obj
        del self.child_captcha_handler
        self._restore_captcha_handler_window(self.main_script_runner)

        self.ui.script_management_button.setText('Стоп')
        self.ui.script_management_button.clicked.disconnect(self.run_main_script_and_set_button_to_stop_condition)
        self.ui.script_management_button.clicked.connect(self.stop_main_script_and_set_button_to_start_condition)

        self.main_script_runner.setTerminationEnabled(True)
        self.main_script_runner.start()

    def stop_main_script_and_set_button_to_start_condition(self):
        self.close_relative_windows()

        self.main_script_runner.stop()
        self.ui.script_management_button.setText('Старт')
        self.ui.script_management_button.clicked.disconnect(self.stop_main_script_and_set_button_to_start_condition)
        self.ui.script_management_button.clicked.connect(self.run_main_script_and_set_button_to_stop_condition)

    def handle_script_finishing(self):
        self._show_result_window(success=True)

        self.ui.script_management_button.setText('Старт')
        self.ui.script_management_button.clicked.disconnect(self.stop_main_script_and_set_button_to_start_condition)
        self.ui.script_management_button.clicked.connect(self.run_main_script_and_set_button_to_stop_condition)

    def handle_captcha_interrupt(self):
        self.stop_main_script_and_set_button_to_start_condition()

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

    def _restore_captcha_handler_window(self, thread: RunningThread):
        """
        Since a new thread is created when the main script is stopped or restarted,
        it is necessary to create a new CaptchaHandlerWindow object,
        which is connected by the signal mechanism on the one hand with the new thread,
        and on the other hand with the GUI window.
        """
        self.child_captcha_handler = CaptchaHandlerWindow(thread)
        self.child_captcha_handler.signal_captcha_handling_interrupt.connect(self.handle_captcha_interrupt)


class RunningThread(QThread):
    success_captcha_got = pyqtSignal()
    need_captcha_from_user = pyqtSignal(str)

    def __init__(self, parent_window: Interface):
        QThread.__init__(self)
        self.parent_window = parent_window
        self.mutex = QMutex()
        self.captcha_waiter = QWaitCondition()
        self.received_captcha_value = ""

    def run(self):
        print('Start')
        core_api.main_script_start(captcha_handler=self.make_captcha_handler_function())
        print('Done')
        # Использовать сигналы вместо взаимных ссылок на объекты
        self.parent_window.handle_script_finishing()

    def stop(self):
        print('Stopped!')
        self.terminate()

    def make_captcha_handler_function(self) -> Callable:
        # TODO: написать что-то вроде документации к этой функции,
        #  которая поясняет как работает связь с другим окном
        #  для получения капчи (через разделяемую память)
        thread_object = self

        def handling_captcha_with_flood_control_function(captcha_exception: Captcha):
            def check_current_captcha_value_correctness(captcha_obj: Captcha) -> bool | Captcha:
                try:
                    captcha_obj.try_again(thread_object.received_captcha_value)
                    return True
                except Captcha as new_captcha_exception:
                    return new_captcha_exception

            thread_object.need_captcha_from_user.emit(captcha_exception.get_url())
            try:
                while True:
                    thread_object.mutex.lock()
                    thread_object.captcha_waiter.wait(thread_object.mutex)
                    handling_result = check_current_captcha_value_correctness(captcha_exception)
                    if handling_result is True:
                        thread_object.success_captcha_got.emit()
                        thread_object.mutex.unlock()
                        break
                    else:
                        captcha_exception = handling_result
                        thread_object.need_captcha_from_user.emit(captcha_exception.get_url())
                        thread_object.mutex.unlock()
            except ApiError:
                # vk_api.exceptions.ApiError: [9] Flood control
                # https://vk.com/faq11583

                # todo: вывести это пользователю, как то ожидать, а что ожидать????
                print("Too many requests. Try later")

            thread_object.parent_window.child_captcha_handler.close()

        return handling_captcha_with_flood_control_function

