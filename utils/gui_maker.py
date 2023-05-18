# TODO: 1) Необходимо добавить обработку кейса когда нет зареганных пользователей, а так же добавить регистрацию
#       2) После нажатия кнопки Старт менять ее название на Стоп (с соответствующим поведением)

import pathlib
from PyQt5 import QtWidgets
from PyQt5.QtCore import QThread
from PyQt5.QtGui import QIcon
from main_standalone_window import Ui_MainWindow

import utils.core_api as core_api

# this fix problem with relative path after importing module
current_file_dir_path = str(pathlib.Path(__file__).parent)
current_file_dir_parent_path = str(pathlib.Path(__file__).parent.parent)


class RunnerWorker(QThread):
    def __init__(self):
        QThread.__init__(self)

    def run(self):
        core_api.main_script_start()


class Interface(QtWidgets.QMainWindow):
    def __init__(self):
        super(Interface, self).__init__()
        self.main_script_runner = RunnerWorker()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('АвтоКоммент')
        # Icon source:
        # <a href="https://www.flaticon.com/ru/free-icons/" title="робот иконки">Робот иконки от Freepik - Flaticon</a>
        self.setWindowIcon(QIcon(current_file_dir_parent_path + '/static/main_window_icon.png'))
        self.ui.add_link_entry.setPlaceholderText('Введите ссылку добавляемого объекта')
        self.ui.delete_link_entry.setPlaceholderText('Введите ссылку удаляемого объекта')

        # buttons
        self.ui.add_link_entry_button.clicked.connect(self.get_link_to_add)
        self.ui.delete_link_entry_button.clicked.connect(self.get_link_to_delete)
        self.ui.time_entry_button.clicked.connect(self.get_time)
        self.ui.start_script_button.clicked.connect(self.main_script_runner.start)

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
