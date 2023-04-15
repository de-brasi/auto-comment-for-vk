from utils.gui_maker import make_gui

if __name__ == "__main__":
    # init context: interface and stored with previous run data
    make_gui()

    # main.py -> utils.gui_maker.py -> core_api.py -> config.py
    #                                          \----> using_vk_api.py
