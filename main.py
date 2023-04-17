from utils.gui_maker import make_gui

if __name__ == "__main__":

    # TODO:
    #  для минимального использования необходимо запускать без GUI,
    #  то есть нужен аргумент из консоли с типом запуска
    #  (как консольное приложение, либо с интерфейсом)

    # init context: interface and stored with previous run data
    make_gui()

    # main.py -> utils.gui_maker.py -> core_api.py -> config.py
    #                                          \----> using_vk_api.py
