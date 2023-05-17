import click


@click.command()
@click.option('--mode', '--m', default='graphic', type=click.Choice(['graphic', 'console']),
              help='Application launch mode.')
def main(mode=None):
    if mode == 'graphic':
        init_gui()
    elif mode == 'console':
        init_command_line_interface()


def init_gui():
    from utils.gui_maker import Example
    from PyQt5 import QtWidgets

    app = QtWidgets.QApplication([])
    application = Example()
    application.show()
    app.exit(app.exec())


def init_command_line_interface():
    import utils.core_api as core_api

    # Importing map
    # main.py -> utils.gui_maker.py
    #        \    |
    #         \   |
    #        utils.core_api.py -> config.py
    #                      \----> utils.using_vk_api.py

    query = [""]
    cur_command = query[0]
    while cur_command != "STOP":
        query = input().split()
        cur_command = query[0]
        if cur_command == "add_photo":
            arg = query[1]
            core_api.add_photo(arg)
        elif cur_command == "set_time":
            h = int(query[1])
            m = int(query[2])
            s = int(query[3])
            core_api.set_time(h, m, s)
        elif cur_command == "add_vk_user":
            login = query[1]
            password = query[2]
            core_api.add_vk_user(login, password)
        elif cur_command == "delete_photo":
            pass
        elif cur_command == "set_default_time":
            pass
        elif cur_command == "get_stored_time":
            pass
        elif cur_command == "get_added_photos":
            pass
        elif cur_command == "delete_vk_user":
            pass
        elif cur_command == "main_script_start":
            core_api.main_script_start()
            print("Executed!")
        elif cur_command == "main_script_stop":
            pass


if __name__ == "__main__":
    main()
