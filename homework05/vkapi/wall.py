import re
import textwrap
import time
import typing as tp
from string import Template

import pandas as pd
import requests  # type: ignore
from pandas import json_normalize
from vkapi import config, session
from vkapi.exceptions import APIError


def get_posts_2500(
    owner_id: str = "",
    domain: str = "",
    offset: int = 0,
    count: int = 0,
    max_count: int = 2500,
    filter: str = "owner",
    extended: int = 0,
    fields: tp.Optional[tp.List[str]] = None,
) -> tp.Dict[str, tp.Any]:
    pass


def get_wall_execute(
    owner_id: str = "",
    domain: str = "",
    offset: int = 0,
    count: int = 0,
    max_count: int = 2500,
    filter: str = "owner",
    extended: int = 0,
    fields: tp.Optional[tp.List[str]] = None,
    progress=None,
) -> pd.DataFrame:
    """
    Возвращает список записей со стены пользователя или сообщества.

    @see: https://vk.com/dev/wall.get

    :param owner_id: Идентификатор пользователя или сообщества, со стены которого необходимо получить записи.
    :param domain: Короткий адрес пользователя или сообщества.
    :param offset: Смещение, необходимое для выборки определенного подмножества записей.
    :param count: Количество записей, которое необходимо получить (0 - все записи).
    :param max_count: Максимальное число записей, которое может быть получено за один запрос.
    :param filter: Определяет, какие типы записей на стене необходимо получить.
    :param extended: 1 — в ответе будут возвращены дополнительные поля profiles и groups, содержащие информацию о пользователях и сообществах.
    :param fields: Список дополнительных полей для профилей и сообществ, которые необходимо вернуть.
    :param progress: Callback для отображения прогресса.
    """
    """stopwrds = []
    f = open('stop_words.txt')
    stopwrds = [line for line in f][1:]
    stopwrds = [line.strip() for line in stopwrds]
    stopwrds.insert(0, 'а')
    f.close()"""

    vk_config = {
        "token": "27bd1a137cebd9ec6821984765a02537871e153b61a2399456a437b847ee2fab6f261f858d814f53a95b2",
        "client_id": "8094474",
        "version": "5.131",
        "domain": "https://api.vk.com/method",
    }
    dom = session.Session(vk_config["domain"])  # type: ignore
    posts = []
    for i in range((count - 1) // max_count + 1):
        try:
            code = Template(
                """
                            var k = 0;
                            var post = [];
                            while(k < $j){
                            post = post + API.wall.get({"owner_id":$owner_id,"domain":"$domain","offset":$offset + k*100,"count":"$count","filter":"$filter","extended":$extended,"fields":"$fields","v":$version})["items"];
                            k=k+1;
                            }
                            return {'count': post.length, 'items': post};
                            """
            ).substitute(
                owner_id=owner_id if owner_id else 0,
                domain=domain,
                offset=offset + max_count * i,
                j=(count - max_count * i - 1) // 100 + 1
                if count - max_count * i <= max_count
                else max_count // 100,
                count=count - max_count * i if count - max_count * i <= 100 else 100,
                filter=filter,
                extended=extended,
                fields=fields,
                version=vk_config["version"],
            )
            time.sleep(2)
            res = dom.post(
                "execute",
                data={
                    "code": code,
                    "access_token": vk_config["token"],
                    "v": vk_config["version"],
                },
            )
            for item in res.json()["response"]["items"]:
                posts.append(item)
        except:
            pass
    for item in posts:
        item["text"] = (
            re.sub(
                "[^a-zA-Zа-яА-ЯёЁ]",
                " ",
                re.sub(r"[!:]|%\((,№#.*?)\)", "", item["text"]),
            )
        ).strip()
        item["text"] = "".join([w.lower() for w in item["text"]])
    return json_normalize(posts)


if __name__ == "__main__":
    print(get_wall_execute(domain="vk", count=10, max_count=1000))
