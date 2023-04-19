# main.py -> utils.gui_maker.py
#        \    |
#         \   |
#        utils.core_api.py -> config.py
#                      \----> utils.using_vk_api.py

import sys
import utils.core_api as core_api
from utils.gui_maker import make_gui

if __name__ == "__main__":
    # todo: -h/--help for overview

    if len(sys.argv) >= 2 and sys.argv[1] == "console":
        print("Write STOP for finish program")
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

    else:
        # init context: interface and stored with previous run data
        make_gui()
