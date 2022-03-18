import statistics
import time
import typing as tp
from datetime import * # type: ignore

import requests # type: ignore
from vkapi.friends import get_friends


def age_predict(user_id: int) -> tp.Optional[float]:
    """
    Наивный прогноз возраста пользователя по возрасту его друзей.

    Возраст считается как медиана среди возраста всех друзей пользователя

    :param user_id: Идентификатор пользователя.
    :return: Медианный возраст пользователя.
    """
    friends_list = get_friends(user_id, fields=["bdate"])
    age, count = [], 0
    for _, item in enumerate(friends_list.items):
        if "bdate" in item: # type: ignore
            if item["bdate"].count(".") == 2: # type: ignore
                age.append(datetime.now().year - int(item["bdate"][len(item["bdate"]) - 4 :])) # type: ignore
                count += 1
    if count == 0:
        return None
    return statistics.median(age)


if __name__ == "__main__":
    print(age_predict(469126965))
