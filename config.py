# todo: extend with settings field (window size, enabled Captcha reader, etc.)
# todo: возможно стоит разделить код функций и саму структуру данных конфига
"""
Context description:
- "vk_users" - list of tuples (login and password) for every saved user
- "photos" - list of urls (type == str)
- "start_time" - tuple(hour, minute, second)
"""
from __future__ import annotations

import os

from typing import Dict
from collections import namedtuple

import pathlib
import json
import csv

Description = namedtuple("Description", ["field", "default_value"])

APP_ID = 2685278
LOGIN = 0
PASSWORD = 1

CONTEXT_FIELD_VK_USERS = "vk_users"
CONTEXT_FIELD_PHOTOS = "photos"
CONTEXT_FIELD_START_TIME = "start_time"

CONTEXT_DESCRIPTION = [
    Description(CONTEXT_FIELD_VK_USERS, []),
    Description(CONTEXT_FIELD_PHOTOS, []),
    Description(CONTEXT_FIELD_START_TIME, [0, 0, 0]),
]

# this fix problem with relative path after importing module
current_file_dir_path = str(pathlib.Path(__file__).parent)


def restore_context() -> Dict[str, list]:
    """
    Restores context from last session information
    """
    # TODO: список фоток предыдущего контекста надо возвращать
    #  только если прошлая сессия крашнулась,
    #  иначе вероятнее пользователь захочет ввести по новой фотки

    previous_context = dict()
    try:
        # todo: add logging
        with open(current_file_dir_path + '/cached_data/last_session.json') as latest_context:
            previous_context = json.load(latest_context)
    except json.decoder.JSONDecodeError:
        # invalid last_session.json content
        latest_context = open(current_file_dir_path + '/cached_data/last_session.json', 'w')
        latest_context.truncate(0)
        latest_context.write("{}")
        latest_context.close()
    except Exception as error:
        print("Unexpected exception: " + repr(error))

    return previous_context


def add_missing_fields(complemented_context: Dict[str, list]) -> None:
    """
    Creates missing context fields and fills them with default values
    """
    for description in CONTEXT_DESCRIPTION:
        if description.field not in complemented_context:
            complemented_context[description.field] = description.default_value


# todo: добавить аккаунты из accounts.csv. А надо ли это делать, если сохраняется контекст прошлого запуска?


context = restore_context()       # execute when importing
add_missing_fields(context)

sessions = []
