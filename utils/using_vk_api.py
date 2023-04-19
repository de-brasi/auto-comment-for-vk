import vk_api
import re
import time
import datetime
from datetime import datetime

from collections import namedtuple

from typing import List
from typing import Tuple


def create_session(login: str, password: str, application_id: int) -> vk_api.VkApi:
    # создать сессию ВК (для одного пользователя по логину и паролю)
    session = vk_api.VkApi(
        login=login,
        password=password,
        app_id=application_id
    )
    return session


def start_with_delay(session: vk_api.VkApi, queries_arguments: List[str], time_to_start: Tuple[int, int, int]):
    PhotoInfo = namedtuple("PhotoInfo", ['owner', 'photo'])

    def parse_photo(photo_url: str) -> PhotoInfo:
        """
        Вычленяет из URL фотографии 2 значения - id хозяина фотографии, id фотографии.
        Согласно документации VK API к методу createComment,
        (https://dev.vk.com/method/photos.createComment)
        нужно разделять хозяев-сообществ и хозяев-пользователей.
        Пользовательский id - просто id,
        id группы - (-1) * id.

        :param photo_url: URL ВК-фотографии, которая будет парситься
        :return: None
        """

        res = re.search(r"photo(-*[0-9]+)_([0-9]+)", photo_url)
        owner_id = res.groups()[0]
        photo_id = res.groups()[1]
        try:
            owner_id = int(owner_id)
            photo_id = int(photo_id)
        except ValueError:
            raise ValueError(f"Error when trying to cast string representation of "
                             f"owner_id(={owner_id}) and photo_id(={photo_id}) "
                             f"to integer value inside {parse_photo.__name__} function")

        return PhotoInfo(owner_id, photo_id)

    def can_be_commented(to_check: PhotoInfo) -> bool:
        # https: // dev.vk.com / method / photos.getById
        response = session.method(
            'photos.getById', {
                'photos': str(to_check.owner) + '_' + str(to_check.photo),
                'extended': 1
            })
        return bool(response[0]['can_comment'])

    def create_comment(owner_id: int, photo_id: int, msg: str):
        # todo: в документации https://vk.com/faq4156 написано,
        #  что вызов метода могут проигнорить при превышении частоты обращений,
        #  либо при однотипных методах
        session.method('photos.createComment', {'owner_id': owner_id,
                                                'photo_id': photo_id,
                                                'message': msg})

    parsed_photo = [parse_photo(url) for url in queries_arguments]

    hour = 0
    minute = 1
    second = 2

    # TODO: пока наивная реализация, посмотреть использование модуля longpool и VkRequestsPool
    message = "example"                                         # todo: choice and random
    preparation_time_in_seconds = 1
    time_to_start_in_seconds = datetime.time(
            time_to_start[hour], time_to_start[minute], time_to_start[second]
        ).second
    delay_in_seconds = max(time_to_start_in_seconds - datetime.now().second - preparation_time_in_seconds, 0)
    time.sleep(delay_in_seconds)

    while True:
        if can_be_commented(parsed_photo[0]):
            # todo:
            #       При таком решении комментирование начнется как только будет доступна первая фотография,
            #       однако же если автор будет в разное время открывать фотографии,
            #       либо надо будет комментировать фотки в разных альбомах (или от разных людей),
            #       можно словить большое и ненужное ожидание на одной самой "долгой" фотке.
            #       Тут, вероятно, пригодится asyncio
            for photo_info in parsed_photo:
                create_comment(photo_info.owner, photo_info.photo, message)
