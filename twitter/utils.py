"""Вспомогательный файл для утилит."""
import requests

from bs4 import BeautifulSoup
from django.core.paginator import Paginator, Page
from django.http import HttpRequest
from django.core.cache import caches
from django.http import HttpRequest

HEADERS = """Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko)Version/13.0.3 Mobile/15E148 Safari/604.1 """


def youtube_downloader():
    url = "https://youtube-to-mp315.p.rapidapi.com/download"

    querystring = {
        "url": "https://www.youtube.com/watch?v=zyG9Nh_PH38",
        "format": "mp3",
    }

    payload = {}
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": "0dfa65d3a6msh001128cf6c62649p17ad77jsn11c5482a7f03",
        "X-RapidAPI-Host": "youtube-to-mp315.p.rapidapi.com",
    }

    response = requests.post(
        url, json=payload, headers=headers, params=querystring
    ).json()

    return response["link"]


cache = caches["default"]


def news():
    response = requests.get(
        url="https://vgtimes.ru/news/", headers={"User-Agent": HEADERS}
    ).text
    response2 = requests.get(
        url="https://vgtimes.ru/news/", headers={"User-Agent": HEADERS}
    )
    print(response2.status_code)
    soup = BeautifulSoup(response, "html.parser")

    news_items = soup.find_all("div", class_="item-name")
    # print(news_items)
    result = []

    for item in news_items:
        news_data = {
            "a": item.find("a").get("href"),
            "span": item.find("span").text,
        }
        result.append(news_data)
    return result


def get_rates():
    response_rate = requests.get(
        url="https://www.mig.kz/",
        headers={"User-Agent": HEADERS},
    ).text
    soups = BeautifulSoup(response_rate, "html.parser")
    atribute = soups.find_all("td", class_="currency")
    buy = soups.find_all("td", class_="buy delta-neutral")
    sell = soups.find_all("td", class_="sell delta-neutral")
    # print("atribute: ", atribute, "/n", "buy: ", buy)
    atrs = [atr.text for atr in atribute]
    b = [buys.text for buys in buy]
    s = [sells.text for sells in sell]
    # print(atrs, type(atrs))

    results = {
        "atr": atrs,
        "buy": b,
        "sell": s,
    }

    print(results, type(results))
    return results


class CustomCache:
    """Кеширование данных."""

    @staticmethod
    def caching(key: str, lambda_func: callable, timeout: int = 1) -> any:
        """Попытка взять или записать кэш."""

        data = cache.get(key)
        if data is None:
            data = lambda_func()
            cache.set(key, data, timeout=timeout)
        return data

    @staticmethod
    def clear_cache(key: str) -> any:
        """Очистка кэша."""

        cache.set(key, None, timeout=1)

    @staticmethod
    def set_cache(key: str, data: any, timeout: int = 1):
        """."""

        cache.set(key, data, timeout=timeout)


class CustomPaginator:
    """Постраничный вывод данных."""

    @staticmethod
    def paginate(object_list: any, request: HttpRequest, limit: int = 15) -> Page:
        _paginator = Paginator(object_list, limit)
        _page = _paginator.get_page(request.GET.get(key="page", default=1))
        return _page

    @staticmethod
    def get_page_array(num: int, max_page: int) -> list:
        if num <= 3:
            return [1, 2, 3]
        if num >= max_page - 2:
            return [max_page - 2, max_page - 1, max_page]
        return [x for x in range(num - 2, num + 3)]


if __name__ == "__main__":
    # news()
    # get_rates()
    # youtube_downloader()
    ...
