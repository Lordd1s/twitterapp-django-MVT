"""Вспомогательный файл для утилит."""
import requests
from bs4 import BeautifulSoup

# from django.core.paginator import Paginator, Page
# from django.core.cache import caches
# from django.http import HttpRequest

HEADERS = "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1"


# DatabaseCache = caches["database"]
# cache = caches["default"]
# ram_cache = caches["ram_cache"]
def news():
    response = requests.get(
        url="https://vgtimes.ru/news/", headers={"User-Agent": HEADERS}
    ).text

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


# class CustomCache:
#     """Кеширование данных."""
#
#     @staticmethod
#     def caching(key: str, lambda_func: callable, timeout: int = 1) -> any:
#         """Попытка взять или записать кэш."""
#
#         data = cache.get(key)
#         if data is None:
#             data = lambda_func()
#             cache.set(key, data, timeout=timeout)
#         return data
#
#     @staticmethod
#     def clear_cache(key: str) -> any:
#         """Очистка кэша."""
#
#         cache.set(key, None, timeout=1)
#
#     @staticmethod
#     def set_cache(key: str, data: any, timeout: int = 1):
#         """."""
#
#         cache.set(key, data, timeout=timeout)
#
#
# class CustomPaginator:
#     """Постраничный вывод данных."""
#
#     @staticmethod
#     def paginate(object_list: any, request: HttpRequest, limit: int = 15) -> Page:
#         """Пагинация данных."""
#
#         _paginator = Paginator(object_list, limit)
#         _page = _paginator.get_page(
#             request.GET.get(key="page", default=1)
#         )  # http://127.0.0.1:8000/ratings/top/?page=1  # path parameter
#         return _page
#
#     @staticmethod
#     def get_page_array(num: int, max_page: int) -> list:
#         """Возвращает ограниченный массив страниц."""
#
#         # index = 5
#         # [3, 4, 5, 6, 7]
#
#         # index = 7
#         # [5, 6, 7, 8, 9]
#
#         if num <= 3:
#             return [1, 2, 3]
#         if num >= max_page - 2:
#             return [max_page - 2, max_page - 1, max_page]
#         return [x for x in range(num - 2, num + 3)]


if __name__ == "__main__":
    news()
    get_rates()
