import requests
import sys
import io
import functools
import logging

def logger(func=None, *, handle=sys.stdout):
    """
    Простой декоратор для логирования работы функции.

    Как работает:
        - Если функция выполнилась без ошибок, записывается сообщение INFO.
        - Если произошла ошибка, записывается ERROR с типом и текстом исключения.
        - Логи отправляются либо в обычный поток (stdout, StringIO),
          либо в logging.Logger — в зависимости от параметра handle.

    Параметры:
        func: сама функция. Не указывается напрямую, если вызывается как @logger(...).
        handle: объект, в который пишутся логи.
            Поддерживаются:
                * logging.Logger (запись через .info()/.error())
                * любой объект с методом write()

    Возвращает:
        Обёрнутую функцию, которая логирует свои вызовы.
    """

    if func is None:
        return lambda f: logger(f, handle=handle)

    @functools.wraps(func)
    def wrapped(*args, **kwargs):
        name = func.__name__
        try:
            result = func(*args, **kwargs)

            msg = f"Логгер отработал успешно '{name}'"
            if isinstance(handle, logging.Logger):
                handle.info(msg)
            else:
                handle.write(f"INFO: {msg}\n")

            return result
        except Exception as e:
            err = f"Ошибка в '{name}': {type(e).__name__}: {e}"
            if isinstance(handle, logging.Logger):
                handle.error(err)
            else:
                handle.write(f"ERROR: {err}\n")
            raise

    return wrapped


@logger(handle=sys.stdout)
def get_currencies(currency_codes, url='https://www.cbr-xml-daily.ru/daily_json.js'):
    """
    Получает текущие курсы валют с открытого API Центрального Банка России.

    Параметры:
        currency_codes: список строк с кодами валют, например ['USD', 'EUR'].
        url: адрес API. По умолчанию используется ежедневный JSON ЦБ.

    Как работает:
        1. Делает GET-запрос к API.
        2. Проверяет, что ответ корректный и содержит нужные данные.
        3. Достаёт курсы указанных валют.
        4. Возвращает словарь вида:
            {
                "USD": 93.25,
                "EUR": 101.7
            }

    Возвращает:
        dict: ключ — код валюты, значение — её курс к рублю.

    Возможные исключения:
        ConnectionError — не удалось подключиться к API.
        ValueError — полученный JSON повреждён или не читается.
        KeyError — нет ключа "Valute" или отсутствует нужная валюта.
        TypeError — тип значения валюты не float/int.
    """

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise ConnectionError(f"Ошибка подключения к API: {e}") from e

    try:
        data = response.json()
    except ValueError as e:
        raise ValueError(f"Ошибка парсинга JSON: {e}") from e

    if "Valute" not in data:
        raise KeyError("В ответе API отсутствует ключ 'Valute'")

    result = {}

    for code in currency_codes:
        if code not in data["Valute"]:
            raise KeyError(f"Валюта '{code}' отсутствует в данных API")

        value = data["Valute"][code].get("Value")

        if not isinstance(value, (int, float)):
            raise TypeError(f"Курс валюты '{code}' имеет неверный тип: {type(value)}")

        result[code] = float(value)

    return result


@logger(handle=sys.stdout)
def solve_quadratic(a, b, c):
    """
    Решает квадратное уравнение вида: a*x^2 + b*x + c = 0.

    Параметры:
        a (число): коэффициент.
        b (число): коэффициент
        c (число): свободный член.


    Возвращает:
        None — если корней нет.
        float — если один корень.
        tuple(float, float) — если два корня.

    Исключения:
        TypeError — если параметры не числа.
        ValueError — если уравнение не имеет решений при a=0, b=0.
    """

    if not all(isinstance(x, (int, float)) for x in (a, b, c)):
        raise TypeError("Коэффициенты должны быть числами")

    if a == 0:
        if b == 0:
            if c == 0:
                return None
            raise ValueError("Уравнение не имеет решений")
        return -c / b

    d = b*b - 4*a*c

    if d < 0:
        return None
    if d == 0:
        return -b / (2*a)

    root = d ** 0.5
    return (-b + root) / (2*a), (-b - root) / (2*a)


def setup_file_logger():
    """
    Создаёт файловый логгер, который пишет сообщения в currency.log.

    Что делает:
        - Создаёт logging.Logger с именем "currency_file".
        - Очищает старые обработчики (чтобы не было дублирующихся логов).
        - Добавляет FileHandler, который пишет в UTF-8.
        - Настраивает формат:
              дата — уровень — сообщение
        - Возвращает готовый логгер.

    Возвращает:
        logging.Logger
    """

    logger_obj = logging.getLogger("currency_file")
    logger_obj.setLevel(logging.INFO)
    logger_obj.handlers = []

    handler = logging.FileHandler("currency.log", mode="w", encoding="utf-8")
    handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
    logger_obj.addHandler(handler)

    return logger_obj
