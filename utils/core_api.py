# TODO:
#  1) нужно добавить возможность редактировать список необходимых фоток в рантайме
#       (то есть пока время не пришло где-то в отдельном потоке ждет скрпит для запуска,
#       а разделяемая между потоками память/файл редактируется)
#  2)


from typing import List
import vk_api

import json
import sys
import pathlib

import config

# Warning! Path of directory that contains a path need to be added to PATH before importing using_vk_api!
parents_path = str(pathlib.Path(__file__).parent)
sys.path.append(parents_path)

import using_vk_api


def add_photo(photo_url: str) -> None:
    # todo: добавление фоток происходит не пачкой - то время,
    #  пока пользователь копипастит ссылки можно использовать на парсинг,
    #  либо на тяжелые работы с коллекциями
    #  (слайсинг листа при удалении, линейный поиск и тд)

    if photo_url not in config.context[config.CONTEXT_FIELD_PHOTOS]:
        # todo: подумать над использованием более оптимального
        #       с точки зрения асимптотики алгоритма
        config.context[config.CONTEXT_FIELD_PHOTOS].append(photo_url)


def delete_photo(to_delete_photo_url: str) -> None:
    # todo: проверять наличие этой фотки
    # todo: выбрать нужную коллекцию дял фоток
    #   (для малого количества фото пройдет простое нарезание и копирование списка)

    # todo: добавление фоток происходит не пачкой - то время,
    #  пока пользователь копипастит ссылки можно использовать на парсинг,
    #  либо на тяжелые работы с коллекциями
    #  (слайсинг листа при удалении, линейный поиск и тд)

    after_deleting = []
    for photo in config.context[config.CONTEXT_FIELD_PHOTOS]:
        # пока наивное решение - линейный поиск + копирование
        if photo != to_delete_photo_url:
            after_deleting.append(photo)
    config.context[config.CONTEXT_FIELD_PHOTOS] = after_deleting


def get_added_photos(with_copy: bool = False) -> List[str]:
    res = config.context[config.CONTEXT_FIELD_PHOTOS]
    if with_copy:
        res = res.copy()
    return res


def set_time(hour: int = 0, minute: int = 0, second: int = 0) -> None:
    assert 0 <= hour <= 23
    assert 0 <= minute <= 59
    assert 0 <= second <= 59
    config.context[config.CONTEXT_FIELD_START_TIME] = [hour, minute, second]


def set_default_time() -> None:
    set_time()


def get_stored_time():
    return config.context[config.CONTEXT_FIELD_START_TIME]


def add_vk_user(login: str, password: str) -> None:
    if [login, password] not in config.context[config.CONTEXT_FIELD_VK_USERS]:
        # todo: подумать над использованием более оптимального
        #       с точки зрения асимптотики алгоритма
        config.context[config.CONTEXT_FIELD_VK_USERS].append((login, password))


def delete_vk_user():
    # TODO: low priority
    pass


def main_script_start() -> None:
    def save_context():
        with open(parents_path + "/../cached_data/last_session.json", 'w') as cached_session:
            json.dump(config.context, cached_session)

    def captcha_handler(captcha):
        """ При возникновении капчи вызывается эта функция и ей передается объект
            капчи. Через метод get_url можно получить ссылку на изображение.
            Через метод try_again можно попытаться отправить запрос с кодом капчи
        """

        key = input("Enter captcha code {0}: ".format(captcha.get_url())).strip()

        # Пробуем снова отправить запрос с капчей
        return captcha.try_again(key)

    # запускает выполнение программы:
    # начинается ожидание нужного времени:
    #   решить, будет какая-то отсрочка или лонгпулы пока не откроются комментарии.
    # Вероятно надо будет 2 мода ввести (для запуска по времени, либо как только откроются комменты)

    save_context()
    sessions = []

    for vk_login, vk_password in config.context["vk_users"]:
        new_session = using_vk_api.create_session(vk_login, vk_password, config.APP_ID)
        # todo: процесс создания аутентификации сессии может проходить очень долго, надо как то параллелить этот процесс
        try:
            # todo: обработать капчу(как ошибки, выдача пользователю, капча хэндлером) и ошибки
            # vk_api.exceptions.AuthError: Unknown error (AUTH; no sid) without token_only=True
            new_session.auth(token_only=True)
        except vk_api.exceptions.Captcha as captcha_ex:
            captcha_handler(captcha_ex)
        sessions.append(new_session)
    config.sessions = sessions

    # TODO: решить вопрос с типом исполнения (сколько тредов, как распределить между акками и тд)
    # TODO: разделить фотки по сессиям и выполнять их совместно - сессия + набор фото

    # todo: пока берется первая сессия и с ней происходит все выполнение
    # todo: проверять при запуске, если нет - акков сигналить пользователю
    assert len(config.sessions) > 0
    cur_session = config.sessions[0]
    cur_photos = config.context[config.CONTEXT_FIELD_PHOTOS]
    try:
        using_vk_api.start_with_delay(cur_session, cur_photos, config.context[config.CONTEXT_FIELD_START_TIME])
    except vk_api.exceptions.Captcha as captcha_ex:
        captcha_handler(captcha_ex)


def main_script_stop():
    # останавливает выполнение программы.
    # ожидается, что пользователь потом будет менять время, либо набор фоток.
    # пока не разрывать установленные сессии, разве что можно добавлять новые
    # (вообще надо будет добавить продвинутый менеджмент аккаунтов)

    # TODO: зависит от выбранного способа ускорения -
    #  если потоки, то убивать рабочие (а до этого их надо хранить)
    pass


# TODO: для определения момента комментирования использовать ВК Longpool
# TODO: для одновременных запросов использовать VkRequestsPool
# TODO: добавить docstring'и для функций
