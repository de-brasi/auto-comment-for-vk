# todo: photos - list of str urls or pair(photo_id, owner_id)?
# todo: extend with settings field (window size, enabled Captcha reader, etc.)
"""
Context description:
- "vk_users" - list of tuples (login and password) for every saved user
- "photos" - list of urls (type == str)
- "time" - tuple(hour, minute, second)
"""

from typing import Dict

import pathlib
import json
import csv

LOGIN = 0
PASSWORD = 1
# this fix problem with relative path after importing module
current_file_path = str(pathlib.Path(__file__).parent)


def restore_context() -> Dict[str, list | tuple]:
    """
    draft
    """
    def not_contained_accounts(_context: Dict[str, list | tuple]):
        return (not _context) or ("vk_users" not in _context) or (not _context["vk_users"])

    def restore_accounts(context_storage: Dict):
        with open(current_file_path + '/cached_data/accounts.csv', 'r', newline='') as saved_accounts:
            all_records = csv.reader(saved_accounts)
            for record in all_records:
                assert len(record) == len(["login", "password"])
                context_storage["vk_users"].append((record[LOGIN], record[PASSWORD]))

    previous_context = dict()
    try:
        # todo: add logging
        with open(current_file_path + '/cached_data/last_session.json') as latest_context:
            previous_context = json.load(latest_context)
    except json.decoder.JSONDecodeError:
        latest_context = open(current_file_path + '/cached_data/last_session.json', 'w')
        latest_context.truncate(0)
        latest_context.write("{}")
        latest_context.close()
    except Exception as error:
        print("Unexpected exception: " + repr(error))

    if not_contained_accounts(previous_context):
        previous_context["vk_users"] = []
        restore_accounts(previous_context)

    return previous_context


context = restore_context()       # execute when importing
